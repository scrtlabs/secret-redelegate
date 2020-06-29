#!/usr/bin/python3
import subprocess
import json
import time
import sys

TX_DELAY 	= 10
CLI_NAME 	= 'secretcli'
COIN_UNIT 	= 'scrt'
UCOIN_UNIT 	= 'u' + COIN_UNIT

def get_account_balance(account):
	result = subprocess.run([CLI_NAME, 'query', 'account', account['address']], stdout=subprocess.PIPE)
	output = json.loads(result.stdout.decode('utf-8'))
	amount = output['value']['coins'][0]['amount']
	return int(amount)

def withdraw_rewards(account):
	# secretcli tx distribution withdraw-all-rewards --from <account_id> --gas auto --ledger --max-msgs 0
	## NOTE: max-msgs = 0 is to work around a bug where more than 5 messages (msgs = # of delegations) split the transaction and then it errors out
	result = subprocess.run([CLI_NAME, 'tx', 'distribution', 'withdraw-all-rewards', '--from', account['id'], '--gas', 'auto', '--ledger', '--max-msgs', '0'], input=b'y\n', stdout=subprocess.PIPE)
	output = json.loads(result.stdout.decode('utf-8'))
	return output

def delegate(account, validator, amount):
	# secretcli tx staking delegate <validator_address> <amount to bond>uscrt --from <account_id> --gas auto --ledger
	time.sleep(TX_DELAY)
	result = subprocess.run([CLI_NAME, 'tx', 'staking', 'delegate', validator, str(amount) + UCOIN_UNIT, '--from', account['id'], '--gas', 'auto', '--ledger'], input=b'y\n', stdout=subprocess.PIPE)
	output = json.loads(result.stdout.decode('utf-8'))
	return output

def redelegate(account, validator_list, ucoin=0):
	pre_balance = get_account_balance(account)
	output = withdraw_rewards(account)
	time.sleep(TX_DELAY)
	post_balance = get_account_balance(account)
	print(f"Withdrew rewards, txhash={output['txhash']}, pre_balance={pre_balance}, post_balance={post_balance}")

	rewards = post_balance - pre_balance
	if (ucoin):
		rewards = ucoin
	if (rewards <= 0):
		print(f'ERR: No rewards to redelegate, got {rewards}')
		return

	amount_per_validator = int(rewards/len(validator_list))
	for i in range(len(validator_list)):
		if (i == len(validator_list) - 1):
			amount_per_validator = rewards

		print(f'About to delegate {amount_per_validator} to {validator_list[i]}')
		delegate_status = False
		while (not delegate_status):
			result = delegate(account, validator_list[i], amount_per_validator)
			if 'code' in result:
				print(f'tx error: {result}')
			else:
				delegate_status = True

		print(result)
		rewards -= amount_per_validator



if __name__== "__main__":

	if (len(sys.argv) < 2):
		print(f'Usage: {sys.argv[0]} <filename> <(optional) {COIN_UNIT} to delegate>')
		exit(1)

	with open(sys.argv[1]) as validators_json:
	    data = json.load(validators_json)
	    validators = data['validators_list']
	    account = data['account']

	    if (len(sys.argv) >= 3):
	    	ucoin = int(sys.argv[2]) * 1000000
	    	print(f'Delegating custom amount of {UCOIN_UNIT}: {ucoin}')
	    	redelegate(account, validators, ucoin)
	    else:
	    	redelegate(account, validators)
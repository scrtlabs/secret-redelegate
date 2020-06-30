# secret-redelegate
A (re-)delegation script for SCRT coins (or other Cosmos SDK compatible coins) using ledger + CLI

This script will automatically withdraw all available rewards, and will equally spread them across all validators configured in the config json file (sample_json.config is an example of such file). Alternatively, the tool also accepts a custom amount to delegate, if for example, this is the first time you're trying to delegate your coins.

## CAUTION

Use at your own risk. This has NOT been thoroughly tested beyond a single OSX machine using specifically `secretcli` and a Ledger Nano S.

## Requirements

1. `secretcli` connected to a local or remote node
2. `python3` assumed to be found at `/usr/bin/python3`. Change the first line of `redelegate.py` otherwise.

## Installation

Clone this repo:
```bash
git clone https://github.com/enigmampc/secret-redelegate.git
```

Make `redelegate.py` an executable:

```bash
chmod +x redelegate.py
```

## Usage

### (Optional) Add your Ledger wallet as a local account

If you haven't done so already, you should add your Ledger wallet as a local account. If this has already been done, skip to the next step. `<account id>` refers to the local name the CLI client will use to refer to your account, whereas `<account number on your Ledger>` is the index of the address you want to choose (use `0` if you're not sure).

```bash
secretcli keys add <account id> --ledger --account <account number on your Ledger> --recover
```

### Obtain your account address

To get your account address, copy the value under "address", given by the output of the following command:

```bash
secretcli keys show <account id>
```

### Create config.json file

First, create a copy of `sample_config.json` as `config.json`:

```bash
cp sample_config.json config.json
```

Now, open `config.json` with your favorite text editor, and update account.id and account.address fields to reflect the information obtained above.

Under `validators_list`, add a list of validator addresses (see here for your options: https://explorer.cashmaney.com/validators. Each address starts with `secretvaloperXXXXX`).

### Run the script

With `config.json` set up, all that's left is running the script. The script accept the following parameters:

- `<filename>`: if you followed the tutorial to this point, you should use `config.json` here.
- OPTIONAL `<amount of scrt>`: if NOT used, then only the rewards available would be re-delegated. If used, then this overrides and uses this as the amount of SCRT to delegate.

**NOTE:** rewards are split equally between the validators set in the configuration file.

## Examples

- To delegate 1000 SCRT for the first time with a `config.json` file set up as above, use:

```bash
./redelegate.py config.json 1000
```

- To withdraw and re-delegate available rewards only, use:

```bash
./redelegate.py config.json
```


## Using with other Cosmos chains

This has not been tested in other chains, but presumably, it should work with other CLI clients as well. To try it, I suggest starting by changing the constants at the top of `redelegate.py` file, and testing it out. Pull requests are obviously welcome ;).

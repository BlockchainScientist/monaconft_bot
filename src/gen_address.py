from web3 import Web3
from web3 import Account
import os

def create_new_mnemonic_account():
    Account.enable_unaudited_hdwallet_features()
    acct, mnemonic = Account.create_with_mnemonic()
    return acct.address, acct.key.hex(), mnemonic

def store_account_json_cover(file_path, account):
    if os.path.exists(file_path):
        print('File exists! Won\'t overwrite it!')
        return
    with open(file_path, 'w') as file:
        file.write(str(account))
        file.close()

def restore_account_json(file_path):
    if not os.path.exists(file_path):
        print('File doesn\'t exist! Quit!')
        return None
    with open(file_path, 'r') as file:
        data = file.read()
        file.close()
        return eval(data)

if __name__ == '__main__':
    accounts = list()
    for i in range(1000):
        addr, key, mnemonic = create_new_mnemonic_account()
        account = {}
        account['address'] = addr
        account['privateKey'] = key
        account['mnemonic'] = mnemonic
        accounts.append(account)
        print(f"Generated address: {i}")
    store_account_json_cover('bot_accounts.txt', accounts)
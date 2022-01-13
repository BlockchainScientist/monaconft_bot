import imp
from monaconft_bot import *
from gen_address import *

from faker import Faker
import threading
import random
import string
import sys

# initialize chrome driver
platform_system = platform.system()
print(f'Current platform: {platform_system}')
if platform_system == "Windows":
    chrome_driver = "./chromedriver/chromedriver_96_win.exe"
elif platform_system == "Darwin":
    chrome_driver = "/chromedriver/chromedriver_96_mac"
else:
    print(f"Unsupported platfrom of {platform_system}, shutdown" )
    sys.exit()
extension_path = './extensions/10.8.1_0.crx'

thread_num = 2
stop_threads = threading.Event()

like_lock = threading.Lock()
follow_lock = threading.Lock()

account_lock = threading.Lock()
cur_account_idx = 0
accounts = {}
rand_follow_num = 20

fake = Faker(locale='en_US')
user_lock = threading.Lock()
users = {}

# your target valuable user id needed to be followed
target_uids = []

def restore_target_uids():
    global target_uids
    with open('target_uid.txt', 'r') as file:
        target_uids = file.read().splitlines()

def get_account():
    global cur_account_idx
    global account_lock
    global accounts
    account_lock.acquire()
    account = accounts[cur_account_idx]
    if cur_account_idx < len(accounts):
        cur_account_idx += 1
    elif cur_account_idx == len(accounts):
        sys.exit()
    else:
        cur_account_idx = 0
    account_lock.release()
    return account

def get_user():
    global user_lock
    user_lock.acquire()
    name = fake.name()
    name = name.replace(' ', '').replace('.', '')
    user_lock.release()
    if len(name) > 18:
        name = name[0:17]
    return name

def run():
    global stop_threads
    while not stop_threads.isSet():
        try:
            # follow and like your accounts
            run_one_bot()
            # randomly follow some users
            rand_follow()
        except KeyboardInterrupt:
            sys.exit()
            return

def run_one_bot():
    global post_lock
    global follow_lock
    account = get_account()
    user_name = get_user()
    user_id = user_name + ''.join(random.sample(string.digits, 2))
    bot = MonacoBot(account['address'], account['mnemonic'], '12345678', chrome_driver, extension_path)
    bot.SignUpOrIn(user_id, user_name)
    for uid in target_uids:
        time.sleep(my_random(3, 6))
        follow_lock.acquire()
        bot.follow_user(uid)
        follow_lock.release()
        bot.like_user_posts(uid, like_lock)
    bot.driver.quit()

def rand_follow():
    global post_lock
    global follow_lock
    account = get_account()
    user_name = get_user()
    user_id = user_name + ''.join(random.sample(string.digits, 2))
    bot = MonacoBot(account['address'], account['mnemonic'], '12345678', chrome_driver, extension_path)
    bot.SignUpOrIn(user_id, user_name)
    follow_list = bot.get_following_users('linglan')
    for i in range(rand_follow_num):
        if len(follow_list) == 0:
            return
        idx = random.randint(0, len(follow_list) - 1)
        time.sleep(my_random(1, 2))
        follow_lock.acquire()
        bot.follow_user(follow_list[idx])
        follow_lock.release()
        new_follow_list = bot.get_following_users(follow_list[idx])
        if len(new_follow_list) == 0:
            continue
        else:
            follow_list += new_follow_list
    bot.driver.quit()

if __name__ == "__main__":
    restore_target_uids()
    if len(target_uids) == 0:
        print('No target, exit')
        sys.exit()
    accounts = restore_account_json('./bot_accounts.txt')
    all_threads = list()
    for i in range(thread_num):
        thread = threading.Thread(target=run)
        thread.start()
        all_threads.append(thread)
    
    for i in all_threads:
        i.join()
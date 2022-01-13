# coding=UTF-8
import time
import json
import random
import platform
import datetime
import threading

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

EXTENSION_ID = 'nkbihfbeogaeaoehlefnkodbefgpgknn'
platform_system = platform.system()
if platform_system == "Windows":
    data_path_prefix = os.getcwd() + "\\bot_file\\chromedriver_96_win.exe"
else:
    data_path_prefix = './bot_file/Chrome_'

chromes = {}
domain = "https://monaconft.io/"
scroll_pages_num = 30

def open_and_switch_to_window(driver, url):
    last_handle = driver.current_window_handle
    print('Open a new blank tab')
    driver.execute_script("window.open('', '_blank');")
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)
    driver.get(url)
    time.sleep(1)
    return last_handle

class MetamaskUtil:
    home_url = 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#'
    
    def launch_chrome(self, driver_path, extension_path, data_path):
        chrome_service = Service(driver_path)
        opt = Options()
        opt.add_extension(extension_path)
        opt.add_experimental_option("excludeSwitches", ['enable-automation'])
        opt.add_argument(f'--user-data-dir={data_path}')
        opt.add_experimental_option("detach", True)
        print('Launching a chrome')
        driver = webdriver.Chrome(service=chrome_service, chrome_options=opt)
        return driver

    def init_metamask(self, driver, secret, password):
        print("initializing metamask")
        open_and_switch_to_window(driver, self.home_url)
        unlock = driver.find_elements(By.XPATH, '//button[text()="解锁"]')
        if len(unlock):
            input_box = driver.find_element(By.ID, 'password')
            input_box.click()
            time.sleep(1)
            input_box.send_keys(password)
            time.sleep(1)
            unlock[0].click()
            time.sleep(1)
        else:
            driver.find_element(By.TAG_NAME, 'button').click()
            time.sleep(1)
            driver.find_element_by_xpath('//button[text()="导入钱包"]').click()
            time.sleep(1)
            driver.find_element_by_xpath('//button[text()="不，谢谢"]').click()
            time.sleep(1)
            # input secret recovery phrase and password
            inputs = driver.find_elements_by_xpath('//input')
            inputs[0].send_keys(secret)
            inputs[1].send_keys(password)
            inputs[2].send_keys(password)
            driver.find_element_by_css_selector('.first-time-flow__terms').click()
            driver.find_element_by_xpath('//button[text()="导入"]').click()
            time.sleep(5)
            driver.find_element_by_xpath('//button[text()="全部完成"]').click()
            time.sleep(1)
            driver.find_element_by_xpath('//button[@title="关闭"]').click()
        time.sleep(1)

    def connectOrSignWebsite(self, driver):
        last_handle = driver.current_window_handle
        time.sleep(3)
        driver.execute_script("window.open('');")
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
    
        driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
        time.sleep(5)
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
        time.sleep(3)
        # Connect
        conn_btn = driver.find_elements(By.XPATH, '//button[text()="下一步"]')
        # Sign
        sign_btn = driver.find_elements(By.XPATH, '//button[text()="签名"]')
        if len(conn_btn):
            driver.find_element_by_xpath('//button[text()="下一步"]').click()
            time.sleep(1)
            driver.find_element_by_xpath('//button[text()="连接"]').click()
            time.sleep(3)
            print('Site connected to metamask')
            print(driver.window_handles)
            res = 'connect'
        elif len(sign_btn):
            driver.find_element_by_xpath('//button[text()="签名"]').click()
            time.sleep(1)
            print('Sign confirmed')
            print(driver.window_handles)
            res = 'sign'
        driver.switch_to.window(last_handle)
        time.sleep(3)
        return res

    def signConfirm(self, driver):
        last_handle = driver.current_window_handle
        print("sign")
        time.sleep(3)
        driver.execute_script("window.open('');")
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
    
        driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
        time.sleep(5)
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
        time.sleep(3)
        signs = driver.find_elements(By.XPATH, '//button[text()="签名"]')
        if len(signs):
            signs[0].click()
            time.sleep(1)
            print('Sign confirmed')
        else:
            print('No sign buttons')
        print(driver.window_handles)
        driver.switch_to.window(last_handle)
        time.sleep(3)

def my_random(x, y):
    return random.randint(x, y)

class MonacoBot:
    def __init__(self, file_id, mnemonic, password, chrome_driver, extension_path):
        print('Initializing a bot')
        self.mnemonic = mnemonic
        self.password = password
        self.running = True
        self.metamask = MetamaskUtil()
        self.init_chrome(file_id, chrome_driver, extension_path)

    def init_chrome(self, file_id, chrome_driver, extension_path):
        global chromes
        data_path = data_path_prefix + str(file_id)
        print('Launching the chrome for the bot')
        self.driver = self.metamask.launch_chrome(chrome_driver, extension_path, data_path)
        self.metamask.init_metamask(self.driver, self.mnemonic, self.password)
        chromes[str(file_id)] = self.driver
    
    def SignUpOrIn(self, user_id, user_name):
        print(f'{user_id} Sign up or sign in')
        self.driver.get('https://monaconft.io/login/wallet')
        time.sleep(2)
        btns = self.driver.find_elements(By.CLASS_NAME, 'login-bg')
        if len(btns):
            self.driver.get('https://monaconft.io/login/wallet')
            time.sleep(2)
            btn = self.driver.find_element(By.CLASS_NAME, 'metamask')
            ActionChains(self.driver).move_to_element(btn).click().perform()
            res = self.metamask.connectOrSignWebsite(self.driver)
            if res == 'connect':
                self.driver.refresh()
                time.sleep(2)
                btn = self.driver.find_element(By.CLASS_NAME, 'metamask')
                ActionChains(self.driver).move_to_element(btn).click().perform()
                self.metamask.signConfirm(self.driver)
                self.metamask.signConfirm(self.driver)
                inputs = self.driver.find_elements(By.CLASS_NAME, 'el-input__inner') 
                if len(inputs):
                    print(f'Register {user_id}.')
                    inputs[0].click()
                    time.sleep(1)
                    inputs[0].send_keys(user_name)
                    time.sleep(1)
                    inputs[1].click()
                    time.sleep(1)
                    inputs[1].send_keys(user_id)
                    time.sleep(1)
                    save = self.driver.find_element_by_xpath('//div[text()=" Save "]')
                    ActionChains(self.driver).move_to_element(save).click().perform()
                    time.sleep(1)
            else:
                time.sleep(2)
                inputs = self.driver.find_elements(By.CLASS_NAME, 'el-input__inner') 
                if len(inputs):
                    print(f'Register {user_id}.')
                    inputs[0].click()
                    time.sleep(1)
                    inputs[0].send_keys(user_name)
                    time.sleep(1)
                    inputs[1].click()
                    time.sleep(1)
                    inputs[1].send_keys(user_id)
                    time.sleep(1)
                    save = self.driver.find_element_by_xpath('//div[text()=" Save "]')
                    ActionChains(self.driver).move_to_element(save).click().perform()
                    time.sleep(1)
        else:
            return

    def get_bot_username(self):
        username = self.driver.find_element(By.CLASS_NAME, 'username')
        return username.text

    def scroll_pages(self, page_num):
        middle = self.driver.find_element(By.CLASS_NAME, 'middle-inner')
        body = self.driver.find_element(By.TAG_NAME, 'body')
        middle.click()
        for i in range(page_num):
            body.send_keys(Keys.SPACE)
            time.sleep(1)

    def follow_user(self, user_id):
        try: 
            username = ""
            self.driver.get(domain + user_id)
            time.sleep(5)
            username = self.get_bot_username()
            fo_button = self.driver.find_elements(By.CLASS_NAME, 'follow-button')
            if len(fo_button) == 0:
                print(f'- [DEV] [{username}] has follown [{user_id}]')
            else:
                self.driver.execute_script("window.onblur = function() { window.onfocus() }")
                time.sleep(my_random(5, 7))
                ActionChains(self.driver).move_to_element(fo_button[0]).click().perform()
                print(f'- [DEV] [{username}] followed [{user_id}] successfully ✅')
                time.sleep(2)
                return True
        except Exception as ex:
            print(f"- [DEV] [{username}] failed in following [{user_id}]")
            print(f"- [DEV] Exception: {ex}")
            return False
    
    def unfollow_user(self, user_id):
        try: 
            username = ""
            self.driver.get(domain + user_id)
            time.sleep(5)
            username = self.get_bot_username()
            fo_button = self.driver.find_elements(By.CLASS_NAME, 'unfollow-button')
            if len(fo_button) == 0:
                print(f'- [DEV] [{username}] has unfollown [{user_id}]')
            else:
                self.driver.execute_script("window.onblur = function() { window.onfocus() }")
                time.sleep(my_random(7, 8))
                ActionChains(self.driver).move_to_element(fo_button[0]).click().perform()
                print(f'- [DEV] [{username}] unfollowed [{user_id}] successfully ✅')
                time.sleep(2)
                return True
        except Exception as ex:
            print(f"- [DEV] [{username}] failed in unfollowing [{user_id}]")
            print(f"- [DEV] Exception: {ex}")
            return False

    def like_user_posts(self, user_id, like_lock):
        try:
            username = ""
            url = domain + user_id + '/posts'
            self.driver.get(url)
            time.sleep(6)
            username = self.get_bot_username()
            print(f'- [DEV] [{username}] is liking posts of {user_id}')
            # self.scroll_pages(scroll_pages_num)
            like_buttons = self.driver.find_elements(By.CLASS_NAME, 'icon-like')
            print(f"- [DEV] Like-buttons list num: " + str(len(like_buttons)))
            for button in like_buttons:
                time.sleep(1)
                like_lock.acquire()
                time.sleep(my_random(10, 12))
                self.driver.execute_script("window.onblur = function() { window.onfocus() }")
                ActionChains(self.driver).move_to_element(button).click().perform()
                print(f'- [DEV] [{username}] liked successfully')
                like_lock.release()
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except Exception as ex:
            print(f"- [DEV] [{username}] liked posts Error: " + str(ex))
        finally:
            if like_lock.locked():
                like_lock.release()

    def get_following_users(self, user_id):
        try: 
            api_uri = f'https://api.monaconft.io/api/user/getFollowingList?uid={user_id}'
            self.driver.get(api_uri)
            time.sleep(my_random(5, 10))
            follow_list = self.driver.find_element_by_xpath('/html/body/pre').text
            obj = json.loads(follow_list)
            if isinstance(obj, dict) and 'data' in obj:
                if isinstance(obj['data'], list) and len(obj) > 0:
                    return list(map(lambda x: x['uid'], obj['data']))
            return []
        except:
            return []
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from enum import  Enum
from bs4 import BeautifulSoup
#This Should use a POM model, but I was kinda lazy
#for the confines of this project I think this is fine
#the point of this is just to whip through my transactions
#not a large scale project

class WebParser(object):

    def __init__(self, debug):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--enable-automation")
        driver = webdriver.Chrome(r'./chromedriver', chrome_options=chrome_options)
        self.driver = driver
        self.debug = debug
        self.logged_in = False

    def open_page(self, url):
        self.driver.get(url)

    def login_td(self,input_mapping):
        try:
            self.open_page('https://authentication.td.com/uap-ui/index.html?consumer=easyweb&locale=en_CA#/login/easyweb-getting-started')
            time.sleep(9)
            user_element = self.driver.find_element_by_name('username')
            time.sleep(2)
            user_element.send_keys(input_mapping['username'])
            time.sleep(3)
            password_element = self.driver.find_element_by_id('password')
            time.sleep(2)
            password_element.send_keys(input_mapping['password'])
            time.sleep(6)
            try:
                no_thanks_close_modal = self.driver.find_element_by_xpath('//strong[contains(text(),"No thanks")]')
                no_thanks_close_modal.click()
                self.logged_in = True
                time.sleep(3)
            except NoSuchElementException:
                print('There was no No Thanks Modal ')
                try:
                    logout_element = self.driver.find_element_by_id('td-logout-button-li')
                except NoSuchElementException:
                    print("wow we didnt find a logout button either, This script sucks! ")
        except NoSuchElementException:
            print('issue with login page')
        finally:
            if not self.logged_in and not self.debug:
                self.driver.quit()

    def get_info(self, account):
        val = self.choose_account(account)
        assert val is 1
        try:
            table = self.driver.find_element_by_xpath('//table[@id="transactionsTable"]')
            self.parse_table(table.get_attribute('innerHTML'))
        except NoSuchElementException:
            print("we didnnt find the table rip")


    def choose_account(self, account):
        try:
            account_element = self.driver.find_element_by_xpath(account)
            account_element.click()
            time.sleep(4)
            try:
                self.driver.find_element_by_xpath('//h1[contains(text(),"Account Activity")]')
            except NoSuchElementException:
                print("wasnt able to find the account activity, something is fishy!")
                return 0
            return  1
        except NoSuchElementException:
            print("didnt find that account you were looking for ")
            return 0

class Account(Enum):
    credit = '//a[contains(text(),"VISA CARD")]'
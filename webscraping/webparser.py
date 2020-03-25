from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from enum import  Enum
from webscraping.htmlparse import MyHTMLParser


#This Should use a POM model, but I was kinda lazy
#for the confines of this project I think this is fine
#the point of this is just to whip through my transactions
#not a large scale project

class WebParser(object):

    def __init__(self, debug):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--enable-automation")
        driver = webdriver.Chrome(r'../chromedriver', chrome_options=chrome_options)
        self.driver = driver
        self.debug = debug
        self.logged_in = False
        self.parser = MyHTMLParser()
        self.next_count = 0

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
                     self.driver.find_element_by_xpath('//li[@id="td-logout-button-li"]')
                     self.logged_in = True
                except NoSuchElementException:
                    print("wow we didnt find a logout button either, This script sucks! ")
                    try:
                        self.driver.find_element_by_xpath('//*[@title="Got It, Thanks"]')
                        self.logged_in = True
                    except NoSuchElementException:
                        print("didnt find a got it thanks either")

        except NoSuchElementException:
            print('issue with login page')


    def get_info(self, account):
        val = self.choose_account(account)
        assert val is 1
        try:
            table = self.driver.find_element_by_xpath('//table[@id="transactionsTable"]')
            self.parser.feed_data(table.get_attribute('outerHTML'),self.next_count)
            self.next_count = self.next_count + 1
            time.sleep(2)
        except NoSuchElementException:
            print("we didnnt find the table rip")

    def click_download(self):
        try:
            select = self.driver.find_element_by_id('ExportTypeSelect')
            for option in select.find_elements_by_tag_name('option'):
                if option.text == 'csv':
                    option.click
                    break
            download_button = self.driver.find_element_by_id('download_button')
            download_button.click
            time.sleep(3)
            return 1
        except NoSuchElementException:
            print("couldnt click dlownload")
            return 0
        
    def click_next(self):
        try:
            next_button = self.driver.find_element_by_xpath('//a[contains(text(),"Previous")]')
            next_button.click()
            time.sleep(3)
            self.get_info(Account.credit)
            return 1
        except NoSuchElementException:
            print("No next button oof")
            return 0

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
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
# from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

EMAIL = "YOUR INSTAGRAM EMAIL"
PASSWORD = "YOUR INSTAGRAM PASSWORD"


class InstagramFollowerBot:

    def __init__(self):
        self.s = Service(ChromeDriverManager().install())
        self.bot = webdriver.Chrome(service=self.s)
        self.url_instagram = "https://www.instagram.com/"
        self.bot.get(self.url_instagram)
        sleep(1)

    def login_instagram(self, EMAIL, PASSWORD):
        cookie_popup = self.bot.find_element(By.XPATH, '/html/body/div[4]/div/div/button[1]')
        cookie_popup.click()
        sleep(3)
        email = self.bot.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
        email.click()
        email.send_keys(EMAIL)
        password = self.bot.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
        password.click()
        password.send_keys(PASSWORD)
        sleep(2)
        password.send_keys(Keys.ENTER)
        sleep(6)
        user_info_popup = self.bot.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button')
        user_info_popup.click()
        sleep(3)
        try:
            notifications_popup = self.bot.find_element(By.XPATH, '/html/body/div[6]/div/div/div/div[3]/button[2]')
            notifications_popup.click()
        except NoSuchElementException:
            notifications_popup = self.bot.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[3]/button[2]')
            notifications_popup.click()
        finally:
            sleep(3)

    def search_profile(self, search_term):
        search_bar1 = self.bot.find_element(By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[1]/div/span')
        search_bar1.click()
        search_bar2 = self.bot.find_element(By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
        search_bar2.send_keys(search_term)
        sleep(3)
        top_result = self.bot.find_element(By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a')
        top_result.click()
        sleep(5)
        followers = self.bot.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
        num_followers = followers.text.split(" ")[0]
        # Instagram displays followers differently depending on the number of followers
        if "m" in num_followers:
            new_num = num_followers.split("m")[0]
            follower_number = float(new_num) * 1000000
        elif "k" in num_followers:
            new_num = num_followers.split("k")[0]
            follower_number = float(new_num) * 1000
        elif "," in num_followers:
            follower_number = int(num_followers.replace(",", ""))
        else:
            follower_number = int(num_followers)
        followers.click()
        sleep(7)
        return follower_number

    def follow_everyone(self, followers):
        # Roughly 12 profiles per scroll
        followers /= 12
        for x in range(int(followers)):
            follow_list = self.bot.find_elements(By.CSS_SELECTOR, "ul div li button")
            for item in follow_list:
                try:
                    name = item.text
                    if name == "Follow":
                        try:
                            item.click()
                            sleep(3)
                            # Instagram reduces the rate of follows you can do if it detects too many, too fast
                            # This if statements helps slow down the rate (if the Follow click above didn't work)
                            if item.text == "Follow":
                                # sleep(28)
                                item.click()
                                sleep(4)
                        except NoSuchElementException:
                            pass
                    else:
                        pass
                except StaleElementReferenceException:
                    pass
                # Instagram currently employs an endless scrolling of followers, hence the Page Down and try/excepts
                if item == follow_list[-1]:
                    item.send_keys(Keys.PAGE_DOWN)
                    sleep(4)


search_term = input("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                    "\n~~~ Instagram Auto Follow Bot ~~~"
                    "\n\nWhat term would you like the bot to search for?"
                    "\nIt will auto select the top result and start following their followers"
                    "\n(so that they might follow you back!)"
                    "\n\nSearch for: ")

bot = InstagramFollowerBot()
bot.login_instagram(EMAIL, PASSWORD)
followers = bot.search_profile(search_term)
bot.follow_everyone(followers)

# Input is included here to stop window/program from closing
input("Don't Close Me")








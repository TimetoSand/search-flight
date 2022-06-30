import sys
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

CHROME_DRIVER_PATH = "Your path."


class SearchFlight:
    def __init__(self, path):
        self.s = Service(CHROME_DRIVER_PATH)
        self.opt = Options()
        self.opt.add_argument("--disable-notifications")
        self.browser = webdriver.Chrome(service=self.s, options=self.opt)
        self.count = 0

    def clear_pop_ups(self, xpath):
        try:
            self.browser.find_element(By.XPATH, xpath).click()
        except:
            pass
        try:
            alert = self.browser.switch_to.alert
            alert.accept()
        except:
            pass

    def choose_currency(self):
        url = "https://www.turna.com/en"
        self.browser.get(url)
        choose_currency = self.browser.find_element(By.XPATH, "/html/body/header/div/div[2]/ul/li[2]/label")
        choose_currency.click()
        select_euro = self.browser.find_element(By.XPATH, '/html/body/header/div/div[2]/ul/li[2]/form/ul/li[1]')
        select_euro.click()
        time.sleep(2)
        check_currency = self.browser.find_element(By.XPATH, '/html/body/header/div/div[2]/ul/li[2]')
        if 'currency-EUR' in check_currency.get_attribute('class').split():
            print('Selection is successful.')
        else:
            choose_currency_li = self.browser.find_element(By.XPATH, '/html/body/header/div/div[2]/ul/li[2]')
            choose_currency_li.click()
            select_euro = self.browser.find_element(By.XPATH, '/html/body/header/div/div[2]/ul/li[2]/form/ul/li[1]')
            select_euro.click()

        time.sleep(1)
        one_way = self.browser.find_element(By.XPATH, '//*[@id="lb-one-way"]')
        one_way.click()


    def search(self):
        result = []
        try:
            # Departure
            fly_from = self.browser.find_element(By.XPATH, '//*[@id="flight-from"]')
            fly_from.click()
            fly_from.send_keys("ANKARA")
            fly_from.send_keys(Keys.ENTER)

            # Arrival
            fly_to = self.browser.find_element(By.XPATH, '//*[@id="flight-to"]')
            fly_to.click()
            cities = ['Barcelona', 'London', 'Stuttgart', 'Florence']
            city = random.choice(cities)
            result.append(city)
            print(f"Flight prices to {city}")
            fly_to.send_keys(city)
            time.sleep(1)
            fly_to.send_keys(Keys.ENTER)
            time.sleep(3)

            # CLOSE POPUP
            try:
                path = '/html/body/div[22]/div/div[1]/span'
                self.clear_pop_ups()(path)
            except:
                pass
            # Date
            departure_date = self.browser.find_element(By.XPATH,
                                                       '/html/body/div[3]/div[2]/form/div[1]/div/div[2]/div[2]/div[1]')

            if 'calendar' in departure_date.get_attribute('class').split():
                print("Calender in class")
            else:
                departure_date = self.browser.find_element(By.CSS_SELECTOR, "div.calendar:nth-child(1)")
            departure_date.click()
            choose_date = self.browser.find_element(By.XPATH,
                                                    "//table[@class='ui-datepicker-calendar']//td[@data-year='2022'][@data-month='6']/a[@class='ui-state-default'][text()='21']")
            choose_date.click()

            search_button = self.browser.find_element(By.XPATH, '//*[@id="btnSearch"]')
            search_button.click()
        except BaseException as e:
            print("Task failing.")
            print(e)
            self.count += 1
            self.search()
            if (self.count == 5):
                print("Too many failures, task ending.")
                sys.exit()

        # switch to child window
        WebDriverWait(self.browser, 20)
        child_window = self.browser.window_handles[0]
        self.browser.switch_to.window(child_window)
        time.sleep(12)

        price = self.browser.find_element(By.XPATH, '/html/body/div[2]/div[7]/div[2]/div[3]/div[1]/div[2]/div[1]/span')
        airline = self.browser.find_element(By.XPATH,
                                            '/html/body/div[2]/div[7]/div[2]/div[3]/div[1]/div[1]/div[1]/span')

        # print(price.get_attribute('innerText'))
        print(price.text)
        # result.append(city)
        result.append(price.text)
        result.append(airline.text)
        result.append("21.07")

        for i in range(10):
            dep_date = self.browser.find_element(By.XPATH, '//*[@id="div-one-way"]')
            dep_date.click()
            choose_date = self.browser.find_element(By.XPATH,
                                                    f"//table[@class='ui-datepicker-calendar']//td[@data-year='2022'][@data-month='6']/a[@class='ui-state-default'][text()='{22 + i}']")
            choose_date.click()
            refresh_btn = self.browser.find_element(By.XPATH, '//*[@id="btnSearch"]')
            refresh_btn.click()
            WebDriverWait(self.browser, 20)
            child_window = self.browser.window_handles[0]
            self.browser.switch_to.window(child_window)
            time.sleep(10)

            price = self.browser.find_element(By.XPATH,
                                              '/html/body/div[2]/div[7]/div[2]/div[3]/div[1]/div[2]/div[1]/span')
            airline = self.browser.find_element(By.XPATH,
                                                '/html/body/div[2]/div[7]/div[2]/div[3]/div[1]/div[1]/div[1]/span')
            result.append(price.text)
            result.append(airline.text)
            result.append(f"{22 + i}.07" if i < 10 else f"{i}.08")
        print(result)
        for i in range(30):
            dep_date = self.browser.find_element(By.XPATH, '//*[@id="div-one-way"]')
            dep_date.click()
            choose_date = self.browser.find_element(By.XPATH,
                                                    f"//table[@class='ui-datepicker-calendar']//td[@data-year='2022'][@data-month='7']/a[@class='ui-state-default'][text()='{1 + i}']")
            choose_date.click()
            refresh_btn = self.browser.find_element(By.XPATH, '//*[@id="btnSearch"]')
            refresh_btn.click()
            WebDriverWait(self.browser, 20)
            child_window = self.browser.window_handles[0]
            self.browser.switch_to.window(child_window)
            time.sleep(10)

            price = self.browser.find_element(By.XPATH,
                                              '/html/body/div[2]/div[7]/div[2]/div[3]/div[1]/div[2]/div[1]/span')
            airline = self.browser.find_element(By.XPATH,
                                                '/html/body/div[2]/div[7]/div[2]/div[3]/div[1]/div[1]/div[1]/span')
            result.append(price.text)
            result.append(airline.text)
            result.append(f"{1 + i}.08")
        with open("fligths.txt", "w", encoding="utf-8") as file:
            file.write('\n'.join(result))

    def close(self):
        self.browser.close()


if __name__ == '__main__':
    seleniumWorkFlow = SearchFlight(CHROME_DRIVER_PATH)
    seleniumWorkFlow.choose_currency()
    seleniumWorkFlow.search()
    seleniumWorkFlow.close()



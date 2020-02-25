from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
import json
import time
from AppKit import NSBeep
 
URL = 'https://login.coupang.com/login/login.pang?rtnUrl=https://cart.coupang.com:443/wishInitView.pang&useTopBanner=true&isHttps=true&pcid=11514126822983006596298'
 
flag=[]
def main():
    try:
        driver = get_driver()
        driver.get(URL)
        config = get_config()
        login_naver_with_execute_script(driver, config['userId'], config['userPw'])
        time.sleep(5)
        get_cart(driver)
        
        # get_mail_list(driver.page_source)
    except Exception as e:
        print(str(e))
    else:
        print("Main process is done.")
    # finally:
        # os.system("Pause")
        # driver.quit()
 
 
def get_config():
    try:
        with open('config.json') as json_file:
            json_data = json.load(json_file)
    except Exception as e:
        print('Error in reading config file, {}'.format(e))
        return None
    else:
        return json_data
 
 
def login_naver_with_execute_script(driver, id, pw):
    script = "                                      \
    (function execute(){                            \
        document.querySelector('#login-email-input').value = '" + id + "'; \
        document.querySelector('#login-password-input').value = '" + pw + "'; \
    })();"
    driver.execute_script(script)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.login__button"))
    )
    element.click()
    return False
 
 
def get_cart(driver):
    while(1):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        div_list = soup.select("#contents > div > div.wish-content.st-wish-content > table > tbody")
        
        for div in div_list:
            soup = BeautifulSoup(str(div), "html.parser")
           
            soldout = soup.find("div", {'class':'price-info'})
            # 재고가 있는 경우
            if soldout != None:
                
                NSBeep()
                print(soldout)
         
        driver.refresh()
        time.sleep(5)

def get_driver():
    driver = webdriver.Chrome('/Users/thkim/workspace/chromeWebDriver/chromedriver')
    driver.implicitly_wait(3)
    return driver
 
 
if __name__ == '__main__':
    main()

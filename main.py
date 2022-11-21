import time

from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://2ip.ru')
time.sleep(10)
driver.close()
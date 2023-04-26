from selenium import webdriver

from utils import extracting_channel_videos


channel_url = input("Please Enter the Link of YouTube channel: ")

driver = webdriver.Chrome()
extracting_channel_videos(channel_url, driver)
driver.quit()

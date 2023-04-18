import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from utils import scroll_all_pages, extract_comments_information


driver = webdriver.Chrome()
channel_link = "https://www.youtube.com/watch?v=zghBofrKv7s&ab_channel=EhmadZubair"
driver.get(channel_link)

scroll_all_pages(driver)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

comments_info = extract_comments_information(soup)

driver.quit()

video_name = soup.title.string
file_name = f'{video_name}.csv'
data_frame = pd.DataFrame(comments_info, columns=[
    'User Name', 'Comment Text', 'Comment Time', 'Likes', 'Thumbnail URL'])
data_frame.to_csv(file_name, index=False)

print('Comments Information Successfully saved to CSV file')

import time
import os


import pandas as pd
from bs4 import BeautifulSoup


def scroll_all_pages(driver):

    last_scroll_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(7)
        new_scroll_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_scroll_height == last_scroll_height:
            break
        last_scroll_height = new_scroll_height


def extract_comments_information(soup):
    comments_container = soup.find_all('ytd-comment-thread-renderer')
    comments = []

    for comment in comments_container:
        user_info = comment.find('ytd-comment-renderer').find('a', {'id': 'author-text'})
        user_name = user_info.text.strip()
        comment_text = comment.find('yt-formatted-string', {'id': 'content-text'}).text.strip()
        likes = comment.find('span', {'id': 'vote-count-middle'}).text.strip()
        comment_time = comment.find('a', {'class': 'yt-simple-endpoint style-scope yt-formatted-string'}).text.strip()
        thumbnail_url_tag = comment.find('yt-img-shadow', {"class": "style-scope ytd-comment-renderer no-transition"})
        if thumbnail_url_tag is not None:
            thumbnail_url = thumbnail_url_tag.find('img').get('src')

        comments.append([
            user_name, comment_text, comment_time, likes, thumbnail_url
        ])

    return comments


def create_channel_directory(channel_url):
    channel_name = channel_url.split("/")[-2].replace('@', '')
    channel_dir = os.path.join(os.getcwd(), channel_name)
    if not os.path.exists(channel_dir):
        os.mkdir(channel_dir)
    return channel_dir


def extract_all_video_links(soup):
    video_links = []
    for video in soup.find_all('ytd-rich-grid-media'):
        video_url = 'https://www.youtube.com' + video.find('a', {'id': 'video-title-link'}).get('href')
        video_links.append(video_url)
    return video_links


def extract_video_comments_info(video_link, channel_dir, driver):
    driver.get(video_link)

    time.sleep(5)

    scroll_all_pages(driver)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    comments_data = extract_comments_information(soup)

    video_name = soup.title.string.split(" - YouTube")[0]
    video_title = video_name.replace('/', '-')

    file_name = video_title + '.csv'
    file_path = os.path.join(channel_dir, file_name)
    data_frame = pd.DataFrame(comments_data, columns=[
        'User Name', 'Comment Text', 'Comment Time', 'Likes', 'Thumbnail Url'
    ])
    data_frame.to_csv(file_path, index=False)
    print(f"Extract Comments of video {video_title} |saved to CSV file| {file_name}")


def extracting_channel_videos(channel_url, driver):
    channel_url += "/videos"
    driver.get(channel_url)

    time.sleep(5)

    scroll_all_pages(driver)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    channel_dir = create_channel_directory(channel_url)
    video_links = extract_all_video_links(soup)

    for video_link in video_links:
        extract_video_comments_info(video_link, channel_dir, driver)

    print("Data successfully saved to CSV files")

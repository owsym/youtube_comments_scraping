import time


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
        else:
            thumbnail_url = None
        comments.append([user_name, comment_text, comment_time, likes, thumbnail_url])
    return comments

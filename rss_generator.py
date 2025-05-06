import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

BASE_URL = "https://mabinogimobile.nexon.com"
CATEGORIES = {
    "notice": "공지사항",
    "event": "이벤트",
    "update": "업데이트"
}

def fetch_posts(category):
    url = f"{BASE_URL}/news/{category}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    posts = []

    for item in soup.select(".news_list_wrap li"):
        title = item.select_one(".news_tit").text.strip()
        link = BASE_URL + item.a['href']
        date = item.select_one(".date").text.strip()
        posts.append({
            "title": title,
            "link": link,
            "date": datetime.strptime(date, "%Y.%m.%d").strftime('%a, %d %b %Y 00:00:00 +0900')
        })
    return posts

def generate_rss(category, posts):
    rss_items = ""
    for post in posts:
        rss_items += f"""
        <item>
            <title>{post['title']}</title>
            <link>{post['link']}</link>
            <pubDate>{post['date']}</pubDate>
            <description><![CDATA[@1369387690608300114 📢 새로운 {category} 게시글이 올라왔습니다!]]></description>
        </item>
        """

    rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
    <channel>
        <title>마비노기 모바일 {CATEGORIES[category]}</title>
        <link>{BASE_URL}/news/{category}</link>
        <description>마비노기 모바일 {CATEGORIES[category]} RSS 피드</description>
        <language>ko</language>
        {rss_items}
    </channel>
    </rss>
    """
    return rss_feed

def main():
    os.makedirs("rss", exist_ok=True)
    for category in CATEGORIES:
        posts = fetch_posts(category)
        rss = generate_rss(category, posts)
        with open(f"rss/{category}.xml", "w", encoding="utf-8") as f:
            f.write(rss)

if __name__ == "__main__":
    main()


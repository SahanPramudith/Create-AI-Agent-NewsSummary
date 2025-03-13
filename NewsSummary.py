import requests
from bs4 import BeautifulSoup
import os
from groq import Groq


GROQ_API_KEY = "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"

# Initialize Groq Client
groq_client = Groq(api_key="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")

# Function to scrape Hiru News
def scrape_hiru_news():
    url = "https://www.hirunews.lk/"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching Hiru News: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    news_list = []

    # Find all articles with the class 'main-article-topic'
    articles = soup.find_all("div", class_="middle-article")
    articles1 = soup.find_all("div", class_="today-video-tittle")

    for article in articles[:5]:  # Get first 5 news articles
        # Extracting the article title and link
        title_tag = article.find("a")
        title = title_tag.text.strip() if title_tag else "No title"
        link = title_tag["href"] if title_tag else "No link"

        news_list.append({"source": "Hiru News", "title": title, "link": link})

    return news_list


# Function to scrape Lankadeepa News
def scrape_derana_news():
    url = "https://www.adaderana.lk/"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching Derana News: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    news_list = []

    # Find all articles with the class 'story-text'
    articles = soup.find_all("div", class_="hot-news news-story")

    for article in articles[:5]:  # Get first 5 news articles
        # Extracting the article title and link
        title_tag = article.find("a")
        title = title_tag.text.strip() if title_tag else "No title"
        link = "https://www.adaderana.lk/" + title_tag["href"] if title_tag else "No link"

        # Extracting the short description
        description_tag = article.find("p")
        description = description_tag.text.strip() if description_tag else "No description"

        news_list.append({"source": "Derana News", "title": title, "description": description, "link": link})

    return news_list


# Generate AI Summary using Groq LLM
def generate_summary(news_title):
    prompt = f"Summarize this news in 2 sentences: {news_title}"

    response = groq_client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# Combine News & Generate Summaries
def get_news_with_summaries():
    news_list = scrape_hiru_news() + scrape_derana_news()

    for news in news_list:
        news["summary"] = generate_summary(news["title"])

    return news_list



# Fetch News & Print Summaries
news_articles = get_news_with_summaries()
for news in news_articles:
    print(f"\n📌 {news['source']}: {news['title']}")
    print(f"🔹 Summary: {news['summary']}")
    print(f"🔗 Read more: {news['link']}")
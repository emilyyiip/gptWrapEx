import requests 
from bs4 import BeautifulSoup
import time

base_url = "https://www.notion.com"
add_url = "https://www.notion.com/help/"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(add_url, headers = headers)
soup = BeautifulSoup(response.text, "html.parser")

#get all links
links = set()
for a_tag in soup.find_all("a", href = True):
    href = a_tag["href"]
    if href.startswith("/help"):  
        full_url = base_url + href
        links.add(full_url)
        full_url = base_url + href.split("?")[0]   #extracts latter portion after base
        links.add(full_url)

#for each link, get content
articles = []
for i, url in enumerate(sorted(links)):
    page = requests.get(url, headers = headers)
    soup_i = BeautifulSoup(page.text, "html.parser")
    title = soup_i.find("h1").text.strip() if soup_i.find("h1") else "Untitled"
    content_block = soup_i.find_all(["h2", "h3", "p", "li"])
    content_cleaned = {text for text in content_block if len(text) > 40}
    content_text = "\n".join([block.get_text(strip=True) for block in content_block])

    articles.append({
        "url": url,
        "title": title,
        "content": content_text
    })

    print(f"[{i+1}/{len(articles)}] Scraped: {title}")
    time.sleep(1) 

#write all info to text file
with open("grab_text.txt", "w", encoding="utf-8") as f:
    for article in articles:
        f.write(f"### {article['title']}\n")
        f.write(article['content'])
        f.write("\n+ --- \n")
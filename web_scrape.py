import requests 
from bs4 import BeautifulSoup

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
    content_block = soup_i.find_all(["h1", "h2", "h3", "p", "li"])
    content_text = "\n".join([block.get_text(strip=True) for block in content_block])

articles.append({
    "url": url,
    "title": title,
    "content": content_text
})


"""
content = soup.find_all(["h1", "h2", "h3", "li", "p"])
text_content = "\n".join([block.get_text(strip = True) for block in content])
with open("grab_text.txt", "w") as f:
    f.write(text_content)
"""
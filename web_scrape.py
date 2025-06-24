import requests 
from bs4 import BeautifulSoup

url = "https://www.notion.com/help/writing-and-editing-basics"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers = headers)
soup = BeautifulSoup(response.text, "html.parser")

content = soup.find_all(["h1", "h2", "h3", "li", "p"])
print(content)
#text_content = (for block in content)
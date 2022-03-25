from bs4 import BeautifulSoup
from urllib.request import urlopen

htmlString = '''<html>
<head><title>My Document</title></head>
<body>Main text.</body></html>
'''
soup = BeautifulSoup(htmlString, "html.parser")
soup1 = BeautifulSoup("<html><head></head><body></body></html>")
soup2 = BeautifulSoup(open("myDoc.html"))
soup3 = BeautifulSoup(urlopen("http://www.networksciencelab.com/"))
text = soup.get_text()
print(text)

href = soup3.find(href = "v2.jpg")
print(href)

links = soup3.find_all("a")
firstLink = links[0]["href"]
print(links)
print(firstLink)
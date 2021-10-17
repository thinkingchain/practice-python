from bs4 import BeautifulSoup

#with open("bs-html.html") as fp:
soup = BeautifulSoup("<html><b id='oldest'>Extremely bold</b></html>","html.parser")
tag = soup.b
print(tag.contents)
  
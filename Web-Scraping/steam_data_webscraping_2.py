import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

def get_text(url):
    try:
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/85.0.4183.102 Safari/537.36', 'Accept-Language': 'en-US '
        }
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "Webscraping Fails！"

num = 1
game_info = dict()
name = []
date = []
genre = []
price = []
score = []
rating = []
votes = []

while num <= 250:
	link = "https://steam250.com/top250"
	text = get_text(link)
	soup = BeautifulSoup(text, "html.parser")
	name_text = soup.find_all('div', id = num)
	for a in name_text:
		b1 = a.find_all('span', class_= 'title')
		if a.find_all('span', class_= 'date') == []:
			b2 = 'Not Available'
		else:
			b2 = a.find_all('span', class_= 'date')
		b3 = a.find_all('a', class_= 'genre')
		if a.find_all('a', class_= 'free') == []:
			b4 = a.find_all('span', class_= 'price')
		else:
			b4 = a.find_all('a', class_= 'free') 
		b5 = a.find_all('span', class_= 'score')
		b6 = a.find_all('span', class_= 'rating')
		b7 = a.find_all('span', class_= 'votes')
		for c1 in b1:
			name.append(c1.find('a').text)
		if b2 != 'Not Available':
			for c2 in b2:
				date.append(c2.find('a').text)
		else:
			date.append(b2)
		for x in b3:
			genre.append(x.text)
		for x in b4:
			price.append(x.text)
		for x in b5:
			score.append(x.text)
		for x in b6:
			rating.append(x.text)
		for x in b7:
			votes.append(x.text)
	num += 1

game_info = {
	'Name': name,
	'Release_Date': date,
	'Genre': genre,
	'Price(USD)': price,
	'Score': score,
	'Rating': rating,
	'Votes': votes
}

save_path = "F:/Baruch College/Project/Steam250.csv"

df = pd.DataFrame(game_info, columns=['Name', 'Release_Date', 'Genre', 'Price(USD)', 'Score', 'Rating', 'Votes'])
df.to_csv(save_path, index = 0, encoding = 'utf-8-sig')
print("The files has been successfully saved！")
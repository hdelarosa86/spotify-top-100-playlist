import requests
from bs4 import BeautifulSoup

date = input('Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ')

ENDPOINT = 'https://www.billboard.com/charts/hot-100/'

response = requests.get(f'{ENDPOINT}{date}/')
web_page_data = response.text

soup = BeautifulSoup(web_page_data, 'html.parser')

music_list = soup.select(selector='.o-chart-results-list__item h3')
top_100_songs = [song.getText().strip() for song in music_list]

print(top_100_songs)







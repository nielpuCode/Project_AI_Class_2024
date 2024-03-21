import os
import requests
from bs4 import BeautifulSoup

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
clear()

# enter city name
city = "jakarta"
 
# create url
url = "https://www.google.com/search?q="+"weather"+city
 
# requests instance
html = requests.get(url).content
 
# getting raw data
soup = BeautifulSoup(html, 'html.parser')


# --------------------------


# get the temperature
temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
 
# this contains time and sky description
str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
 
# format the data
data = str.split('\n')
time = data[0]
sky = data[1]


# ---------------------------


# list having all div tags having particular class name
listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
 
# particular list with required data
strd = listdiv[5].text
 
# formatting the string
pos = strd.find('Wind')
other_data = strd[pos:]


# ----------------------------


# printing all the data
print("\nTemperature is", temp)
print("\nTime: ", time)
print("\nSky Description: ", sky)
print(f"\n\n{other_data}\n\n")
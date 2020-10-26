import telegram
import json

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import time
import pickle
import os
import sys


here = os.path.dirname(os.path.abspath(__file__))  #per renderlo più universale, trova il path della cartella corrente


with open('config.json') as f:  #carica i dati sensibili, token, url e simili dal file di config
	jdata = json.load(f)

tokerino = jdata['tokerino']
URL = jdata['URL']
ade_id = jdata['ade_id']
unic2r1_id = jdata['unic2r1_id']


bot = telegram.Bot(token=tokerino) #creiamo e avviamo un istanza del bot

def cerca_slide():
	slide = [] #inizializziamo vuote le liste, slide contiene i pdf già inviati
	links = [] #links contiene i link appena scrapati dal sito
	difference = [] #i link di links non contenuti in slide, da inviare al canale

	options = Options()  
	options.add_argument("--headless") #aggiunge headless come opzione a chrome
	options.add_argument("--remote-debugging-port=9222")


	driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=options) 
	driver.get(URL) #avvia chrome ed apre la pagina


	html = driver.page_source #salva il codice html
	

	driver.close() #chiude chromedriver

	soup = BeautifulSoup(html) #rende più cercabile e leggibile l'html

	for lin in soup.find_all('a'): #estrae solo i link dall'html
		links.append(lin.get('href'))



	iteraz = 0
	while iteraz < 6: #rimuove i primi che sono link ad altre pagine
		links.pop(0)
		iteraz += 1

	with open(os.path.join(here, "slide.pickle"), "rb") as ft: #carichiamo da file i link già scaricati
		try:
			slide = pickle.load(ft)
		except:
			print("no slide file")

	
	difference = list(set(slide)^set(links))   #mettiamo in difference i link non contenuti in slide

	#print(difference)

	#difference = [i for i in links if i not in slide]
	


	for addr in difference: # per ogni link che manca, il bot invia il file sul canale
		bot.send_document(chat_id = ade_id, document=str(addr))


	todisk = slide + difference #compila la lista unione dei file scaricati in passato e or ora

	with open(os.path.join(here, "slide.pickle"), "wb") as fp: #reimpacchetta la lista su file  
		pickle.dump(todisk, fp)  




cerca_slide()






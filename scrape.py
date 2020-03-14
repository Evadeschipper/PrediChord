import requests
import pandas as pd
from os import path as op
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

def __scrape_chords(html):
  """
  Extract the chords from an ultimate-guitar html template.

  Args:
    html: string - html-content of a song-page.

  Returns:
    chords: list - list of chords
  """

  soup = BeautifulSoup(html, 'html.parser')

  return soup

def __check_cache_for_scrape(song_name, artist):
  """
  Read cached scrape if available.

  Args:
    song_name: string - name of the song
    artis: string - name of the main artist
  
  Returns:
    scrape: string - html-content of the scrape
  """
  # CHECK EXPECTED PATH FOR A SCRAPE
  return None


def scrape_song(song_name, artist, force_rescrape=False):
  """
  Scrape for song from ultimate-guitar.com

  Args:
    song_name: string - name of the song
    artis: string - name of the main artist
    force_rescape: boolean - skip the use of cached scrape
  
  Returns:
    scrape: string - html-content of the scrape
  """

  if not force_rescrape:
    scrape = __check_cache_for_scrape(song_name, artist)
    # Scrape is None, if cached version is not available
    if scrape:
      return scrape
  # TODO Requests search
  # TODO Choose the best result (X)
  # TODO Request X
  # TODO Scrape X
  # TODO Cache X

  payload = {"value": ""}
  #resp = requests.get(https://www.ultimate-guitar.com/search.php?search_type=title&value=Van%20Jou)


def scrape_csv(fp):
  df = pd.read_csv(fp, sep=";")
  for i, row in df.iterrows():
    song_name, artist = row[["song-name", "artist"]]

if __name__ == "__main__":
  
  chrome_options = Options()
  chrome_options.add_argument("--headless")
  
  driver = webdriver.Chrome(chrome_options=chrome_options)

  driver.get("https://tabs.ultimate-guitar.com/tab/ed-sheeran/perfect-chords-1956589")

  chords = __scrape_chords(driver.page_source)

  print(chords)

  # response = requests.get("https://tabs.ultimate-guitar.com/tab/ed-sheeran/perfect-chords-1956589")
  # chords = __scrape_chords(response.text)
  # print(chords)
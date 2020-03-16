
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from scrape import __scrape_chords
import pickle
import sys
from os import path as op

templinks = ["https://tabs.ultimate-guitar.com/tab/bruno-mars/when-i-was-your-man-chords-1198871",
            "https://tabs.ultimate-guitar.com/tab/lewis-capaldi/someone-you-loved-chords-2512737",
            "https://tabs.ultimate-guitar.com/tab/elvis-presley/cant-help-falling-in-love-chords-1086983",
            "https://tabs.ultimate-guitar.com/tab/tones-and-i/dance-monkey-chords-2787730",
            "https://tabs.ultimate-guitar.com/tab/avicii/wake-me-up-chords-1397194",
            "https://tabs.ultimate-guitar.com/tab/elton-john/your-song-chords-29113",
            "https://tabs.ultimate-guitar.com/tab/adele/when-we-were-young-chords-1782038",
            "https://tabs.ultimate-guitar.com/tab/ed-sheeran/the-a-team-chords-989712",
            "https://tabs.ultimate-guitar.com/tab/chris-isaak/wicked-game-chords-11066",
            "https://tabs.ultimate-guitar.com/tab/coldplay/yellow-chords-114080"]

if __name__ == "__main__":

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    data = {}
    
    for link in templinks:

        if sys.platform.startswith("linux"):
          if op.exists(op.join(op.dirname(__file__), "chromedrivers")):
            driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=op.join(op.dirname(__file__), "chromedrivers", "chromedriver"))
          else:
            driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=op.join(op.dirname(__file__), "chromedriver"))
        elif sys.platform.startswith("win32"):
          if op.exists(op.join(op.dirname(__file__), "chromedrivers")):
            driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=op.join(op.dirname(__file__), "chromedrivers", "chromedriver.exe"))
          else:
            driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=op.join(op.dirname(__file__), "chromedriver.exe"))
        else:
          # Try to recover with opportunistic pathing
          driver = webdriver.Chrome(chrome_options=chrome_options)
        
        driver.get(link)

        data[link] = __scrape_chords(driver.page_source)
        print(data[link])

        driver.close()
    
    with open('tempdata.pickle', 'wb') as handle:
        pickle.dump(data, handle)
import requests
import pandas as pd
import sys
import re
import json
import warnings
from os import path as op
from os import listdir, mkdir
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from transpose import equiChord
from edit_distance import iterative_levenshtein

def scrape_csv(fp):
    df = pd.read_csv(fp, sep=";")
    for i, row in df.iterrows():
        song_name, artist = row[["song-name", "artist"]]

def scrape_streaming_data(datapath):
    """
    Scrape streaming data from a spotify datadump. 

    Args:
        datapath: string - path of folder with spotify datadump.
    
    Returns:
        df: pandas df with the streaming data. 
    """

    r = re.compile("StreamingHistory")
    jsonfiles = list(filter(r.match, listdir(datapath)))

    jsonlist = []

    for jsonfile in jsonfiles:
        with open(datapath + "/" + jsonfile, encoding="utf8") as f:
            jsonlist += json.load(f)

    endTime = []
    artistName = []
    trackName = []
    msPlayed = []

    for play in jsonlist:
        endTime.append(play.get('endTime'))
        artistName.append(play.get('artistName'))
        trackName.append(play.get('trackName'))
        msPlayed.append(play.get('msPlayed'))

    data = {'endTime':  endTime,
            'artistName': artistName,
            'trackName': trackName,
            'msPlayed': msPlayed}

    df = pd.DataFrame(data, columns = ['endTime','artistName', 'trackName', 'msPlayed'])

    # Throw out plays that lasted less than a minute.
    df = df[df['msPlayed'] > 60000]

    return df

def __scrape_chords(html):
    """
    Extract the chords from an ultimate-guitar html template.

    Args:
      html: string - html-content of a song-page.

    Returns:
      chords: list - list of chords
    """

    soup = BeautifulSoup(html, 'html.parser')
    
    chords = []
    for element in soup.find_all('span', attrs={"class": "_3bHP1 _3ffP6"}):

        chord = element.get_text()
        chord = equiChord(chord)
        chords.append(chord)
      
    return chords


def __scrape_matches(html):
    """
    Extract matches from the search.

    Args:
        html: string - html-content of a results page.
    
    Returns:
        matches: list - matches with (song, artist, #ratings, ratings, result-type, url)
    """

    matches = []

    # Ultimate-guitar seems to use encoded names for classes, but they seem to be consistent
    # Code below relies on that consistency

    soup = BeautifulSoup(html, features="html.parser")
    cur_artist = None

    if soup.find(attrs={"class": "pZcWD"}) is None:
        matches = []
    else:
        # Skip the header row of the results
        for result_line in soup.find_all(attrs={"class": "pZcWD"})[1:]:
            artist, song, rating, result_type = result_line.contents
            
            if artist.find("a") is not None:
                artist = artist.find("a").text
                cur_artist = artist
            else:
                artist = cur_artist
            
            song_a_tag = song.find("a")
            song = song_a_tag.text
            chord_url = song_a_tag["href"]

            result_type = result_type.text

            if result_type != "chords":
                continue

            # Skip official version of song on UG.
            if rating.find(attrs={"class": "dEQ1I"}) is None:
                continue

            stars, n_raters = rating.find(attrs={"class": "dEQ1I"}), rating.find(attrs={"class": "_31dWM"}).text

            numerical_stars = 0.0
            for star in stars.contents:
                # Name consistently contains '_3v82_'.
                if "_34xpF" in star["class"]:
                    numerical_stars += 0.5
                elif "_3YfNh" in star["class"]:
                    numerical_stars += 0.
                else:
                    numerical_stars += 1.
            
            n_raters = re.sub(r",", "", n_raters)
            n_raters = int(n_raters)

            matches.append((song, artist, n_raters, numerical_stars, result_type, chord_url))
        
    return matches


def __choose_best_matching_candidate(candidates, artist):
    """
    Chooses the best matching candidate according to pre-determined rules.

    Args:
        candidates: list - list of candidate tuples (song-name, artist, #ratings, avg-rating, result-type, url)
        artist: str - original artist name in search query

    Returns:
        candidate: tuple - 'Best' matching candidate tuple (song-name, artist, #ratings, avg-rating, result-type, url)
    """

    matched_artists = []
    for match in candidates:
        matched_artists.append(match[1])
    matched_artists = set(matched_artists)

    # If there is more than 1 matched artist:
    if len(matched_artists) > 1:
        distance = []

        # Calculate the levenshtein edit distance between the searched artist name and the artist names in the search results.
        for matched_artist in matched_artists:
            distance.append(iterative_levenshtein(matched_artist, artist))
        
        print(distance)

    # If there is more than 1 artist: find the artist with the smallest edit distance. 
    # Then exclude from candidates all matches that do not have that artist. 

    # Descending list
    sort_on_nratings = sorted(candidates, key=lambda cand: cand[2], reverse=True)

    # Take the one with the most votes
    selected = sort_on_nratings[0]

    # Unless it has a rating lower than 4.
    if selected[3] < 4:

        sort_on_rating = sorted(candidates, key=lambda cand: cand[3], reverse=True)

        # If there is one with a rating higher than 4, select that one. 
        if sort_on_rating[0][3] > 4:
            selected = sort_on_rating[0]

    print(selected)

    return selected


def __cache_path(song_name, artist):
    """
    Encodes a cache-path for given song & artist combination.

    Args:
        song_name: string - name of the song
        artis: string - name of the main artist
    
    Returns:
        cache_path: str - deterministicly created file-path for song
    """
    cache_name = "-".join([artist, song_name]) + ".json"
    cache_path = op.join(op.dirname(__file__), "data", "cache", cache_name)

    return cache_path


def __cached_scrape_available(song_name, artist):
    """
    Check cache for song specific scrape.

    Args:
        song_name: string - name of the song
        artis: string - name of the main artist
    
    Returns:
        is_available: boolean
    """
    cache_path = __cache_path(song_name, artist)

    return op.exists(cache_path)

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
        if __cached_scrape_available(song_name, artist):
            with open(__cache_path(song_name, artist), "r") as cache_file:
                try:
                    cached_song = json.load(cache_file)
                    return cached_song["Chords"]
                except (KeyError, TypeError):
                    # Really old caches consist on list -> TypeError for indexing
                    # KeyError to check that the attribute exists
                    warnings.warn("Cached file did not contain expected key 'Chords'. Rescraping the song")

    chrome_options = Options()
    chrome_options.add_argument("--headless")

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
    
    driver.get("https://www.ultimate-guitar.com/search.php?search_type=title&type=300&value={title}".format(
        title=" ".join([song_name, artist]).replace(" ", "%20")
    ))

    html = driver.page_source

    candidates = __scrape_matches(html)
  
    if not candidates:
        # Cannot find chords if we have no candidates
        driver.close()
        return []

    UG_song_name, UG_artist, _, _, _, chord_url  = __choose_best_matching_candidate(candidates, artist)

    driver.get(chord_url)

    chords_html = driver.page_source

    chords = __scrape_chords(chords_html)

    driver.close()

    if chords:
        # Cache the results
        cache_folder = op.join(op.dirname(__file__), "data", "cache")

        if not op.exists(cache_folder):
            mkdir(cache_folder)
        with open(__cache_path(song_name, artist), "w+") as cache_file:
            cache_dump = {
                "UltimateGuitar-song_name": UG_song_name,
                "UltimateGuitar-artist": UG_artist,
                "UltimageGuitar-song_url": chord_url,
                "Chords": chords
            }
            json.dump(cache_dump, cache_file, indent=4)
    
    return chords

if __name__ == "__main__":

    chords = scrape_song("Wake me up", "Avicii", force_rescrape = True)
    print(chords)

    # "Robot Rock / Oh yeah", "Daft Punk"
    # "I'm like a bird", "Nelly Furtado"
    # "Perfect", "Ed Sheeran"
    # "Symphony", "Clean Bandit"
    # "Wake me up", "Avicii"

    """   df = scrape_streaming_data("./MyData")

    # Plays per track
    trackCounts = df.groupby('artistName')['trackName'].value_counts() """
    
import requests
import json
import time
from bs4 import BeautifulSoup


def save_movies(movies):
    json_file = open(MOVIES_DICT_NAME, "w")
    json.dump(movies, json_file)
    json_file.close()


def movies_append(movies, title, year, classification, length, rating, genres, directors, writers, stars, url, img):
    movies['Title'].append(title)
    movies['Year'].append(year)
    movies['Classification'].append(classification)
    movies['Length'].append(length)
    movies['Rating'].append(rating)
    movies['Genres'].append(genres)
    movies['Directors'].append(directors)
    movies['Writers'].append(writers)
    movies['Stars'].append(stars)
    movies['URL'].append(url)
    movies['img'].append(img)


def load_cache():
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache


def save_cache(cache):
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()


def make_url_request_using_cache(url, cache):
    if url in cache.keys():
        print("Using cache")
        return cache[url]
    else:
        print("Fetching")
        time.sleep(1)
        response = requests.get(url, headers=headers)
        cache[url] = response.text
        save_cache(cache)
        return cache[url]


def scrape_info(soup_detail):
    # title, year, classification, length, rating, genres

    info_block = soup_detail.find('div', class_="TitleBlock__Container-sc-1nlhx7j-0 hglRHk")
    info_list = info_block.find_all('li')
    year = info_list[0].find('a').text
    if info_list[1].find('a'):
        classification = info_list[1].find('a').text
        length = info_list[2].text
    else:
        classification = 'Not Rated'
        length = info_list[1].text

    title = soup_detail.find('h1').text
    rating = float(soup_detail.find('span', class_='AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV').text)
    genre_list = soup_detail.find_all('a',
                                      class_='GenresAndPlot__GenreChip-cum89p-3 fzmeux ipc-chip ipc-chip--on-baseAlt')
    genres = [genre.text for genre in genre_list]

    if soup_detail.find('div', class_='ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--baseAlt ipc-media--poster-l ipc-poster__poster-image ipc-media__img') == None:
        print(title)
    img = soup_detail.find('div', class_='ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--baseAlt ipc-media--poster-l ipc-poster__poster-image ipc-media__img').find('img')['src']

    return title, year, classification, length, rating, genres, img


def scrape_staff(soup_detail):
    # directors, writers, stars
    staff_block = soup_detail.find('ul',
                                   class_='ipc-metadata-list ipc-metadata-list--dividers-all title-pc-list ipc-metadata-list--baseAlt')
    staff_list = staff_block.find_all('li', class_='ipc-metadata-list__item')

    if staff_list[0].find('span') and staff_list[0].find('span').text == 'Directors':
        directors = [director.text.split('(')[0] for director in staff_list[0].find_all('li')]
    elif staff_list[0].find('a').text == 'Directors':
        directors = [director.text.split('(')[0] for director in staff_list[0].find_all('li')]
    else:
        directors = [staff_list[0].find('a').text.split('(')[0]]

    if staff_list[1].find('span') and staff_list[1].find('span').text == 'Writers':
        writers = [writer.text.split('(')[0] for writer in staff_list[1].find_all('li')]
    elif staff_list[1].find('a').text == 'Writers':
        writers = [writer.text.split('(')[0] for writer in staff_list[1].find_all('li')]
    else:
        writers = [staff_list[1].find('a').text.split('(')[0]]

    stars = [star.text.split('(')[0] for star in staff_list[2].find_all('li')]
    return directors, writers, stars


def scrape_detail(movie_listing_tr, movies, cache_dict):
    movie_link_tag = movie_listing_tr.find('a')
    movie_details_path = movie_link_tag['href']
    movie_details_url = BASE_URL + movie_details_path
    movie_details = make_url_request_using_cache(movie_details_url, cache_dict)
    soup_detail = BeautifulSoup(movie_details, 'html.parser')

    title, year, classification, length, rating, genres, img = scrape_info(soup_detail)
    directors, writers, stars = scrape_staff(soup_detail)
    movies_append(movies, title, year, classification, length, rating, genres, directors, writers, stars,
                  movie_details_url, img)


def scrape():
    cache_dict = load_cache()
    movies_page_url = BASE_URL + MOVIES_PATH
    url_text = make_url_request_using_cache(movies_page_url, cache_dict)
    soup = BeautifulSoup(url_text, 'html.parser')

    movie_listing_parent = soup.find('tbody', class_='lister-list')
    movie_listing_trs = movie_listing_parent.find_all('tr', recursive=False)

    movies = {'Title': [], 'Year': [], 'Classification': [], 'Length': [], 'Rating': [], 'Genres': [], 'Directors': [],
              'Writers': [], 'Stars': [], 'URL': [], 'img': []}
    for movie_listing_tr in movie_listing_trs:
        scrape_detail(movie_listing_tr, movies, cache_dict)
    save_movies(movies)
    save_cache(cache_dict)

BASE_URL = 'https://www.imdb.com'
MOVIES_PATH = '/chart/top/?ref_=nv_mv_250'
CACHE_FILE_NAME = 'cache_html_texts.json'
MOVIES_DICT_NAME = 'movies.json'

headers = {'User-Agent': 'UMSI 507 Course Project - Python Web Scraping', 'From': 'lizshen@umich.edu',
           'Course-Info': 'https://www.si.umich.edu/programs/courses/507'}


'''

# This scraper saves the html text of each movie pages to 'cache_html_texts.json',
    and saves movies information to 'movies.json'
    
scrape()

'''
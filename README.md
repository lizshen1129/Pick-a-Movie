# Pick a Movie

This project is a 'Pick a Movie' app, which takes user inputs, and outputs a list of movies correspondingly. It first used BeautifulSoup to scrape information from [IMDb Top 250 movies](https://www.imdb.com/chart/top/?ref_=nv_mv_250), and manage information using caches. The data structure applied is graph structure. The interaction is realized through Flask app.

## Requirements

This project requires Flask, request, render\_template from flask only, if you are a user.
However, if you want to reproduce the scraping, you also need BeautifulSoup from bs4, and requests.
You might install them all using the this command.

```
pip install -r requirements.txt
```

## How to use this app

After installing the packages, open 'interface.py' in terminal.

```
python interface.pt
```

Then go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) on your browser.
You will see the index page of Pick a Movie, where you can enter your preferences about years, genres, ratings, etc..
After you are done, click on 'Submit Form', and you will be directed to the result page, where a list of movies is shown according to your preferences.

Notice that the conditions of the same attributes will be taken the union. For example, if you choose Crime and Horror, it will search for movies in crime or horror genre (or both). But conditions across attributes will be taken the intersection. For example, if you choose Crime (genre) and R (classification), it will only search for crime movies rated as R movies.

Have fun!

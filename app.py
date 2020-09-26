from flask import Flask
import threading
import toml
import hashlib
from datetime import datetime
from time import mktime
from loguru import logger

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('Agg') # prevent main thread crash
from matplotlib import pyplot as plt

import seaborn as sns


import feedparser
from pprint import pprint

from flask import Flask, render_template, redirect, session, request
import os
from flaskwebgui import FlaskUI # https://pypi.org/project/flaskwebgui/

from bs4 import BeautifulSoup

from text_tools import TextAnalyzer

from collections import Counter

from wordcloud import WordCloud


config = toml.load('config.toml')



app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

ui = FlaskUI(app)

def encode(sentence):
    m = hashlib.md5()
    m.update(sentence.encode('utf-8'))
    encoded = str(int(m.hexdigest(), 16))[0:12]
    return encoded

def parse_feed(container:[], source:str, url:str, pre_filter:bool, stopwords:[]):
    feed = feedparser.parse(url)
    ids = []
    titles = []
    urls = []
    dates = []
    sources = []
    incipit = []
    for i in range(len(feed.entries)):
        entry = feed.entries[i]
        if pre_filter == True and any(word.lower() in entry.title.lower() for word in stopwords):
            pass
            # logger.debug(f"Filtered out: {entry.title}")
        else:
            titles.append(entry.title)
            urls.append(entry.link)
            dates.append(datetime.fromtimestamp(mktime(entry.updated_parsed)))
            ids.append(encode(entry.title))
            sources.append(source)
            try:
                soup = BeautifulSoup(entry.summary, 'html.parser')
                incipit.append([''.join(s.findAll(text=True)) for s in soup.findAll('p')][0].split('...')[0])
            except:
                incipit.append("") 
    data = {}
    data['title'] = titles
    data['url'] = urls
    data['date'] = dates
    data['id'] = ids
    data['source'] = sources
    data['incipit'] = incipit
    container.append(pd.DataFrame(data))
    return container

def gather_data(container:[], target_f, data:{}, *argv):
    thread_list = []
    for key, value in data.items():
        thread = threading.Thread(target=parse_feed, args=([container, value[argv[0]], value[argv[1]], value[argv[2]], value[argv[3]]]))
        thread_list.append(thread)
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()
    return container

def get_feed_data():
    container = []
    data = gather_data(container, parse_feed, config['sources'], 'name', 'url', 'pre_filter', 'stopwords')
    data = pd.concat(data)
    data = data.sort_values("date", ascending=False)
    data = data.reset_index(drop=True)
    return data



@app.route("/")
def home():
    config = toml.load('config.toml')
    if not os.path.exists('./json'):
        os.makedirs('./json')
    try:
        data = pd.read_json('./json/data.json')
    except:
        data = get_feed_data()
        data.to_json('./json/data.json')
    
    sources = list(data['source'].unique())

    return render_template('index.html', data=data, display_limit=500, active=sources, feed_title=config['feed_title'], theme=config['theme']) 


@app.route("/update")
def update():
    if not os.path.exists('./json'):
        os.makedirs('./json')
    data = get_feed_data()
    data.to_json('./json/data.json')
    return redirect("/", code=302)


@app.route("/filter_title", methods=["GET", "POST"])
def filter_title():
    word = request.form.get("word")
    word = str(word).strip()
    data = pd.read_json('./json/data.json')
    data =  data[data['title'].str.contains(word, case=False)]
    sources = list(data['source'].unique())
    # session['sources'] = sources.to_dict()
    return render_template('index.html', data=data, display_limit=500, active=sources, feed_title=config['feed_title'], theme=config['theme'])

@app.route("/text", methods=['GET', 'POST'])
def text():
    config = toml.load('config.toml')
    if not os.path.exists('./json'):
        os.makedirs('./json')
    try:
        data = pd.read_json('./json/data.json')
    except:
        data = get_feed_data()
        data.to_json('./json/data.json')
    sources = list(data['source'].unique())
    word_bag, sentence_bag = TextAnalyzer.prepare_data(data, ["title"])
  
    counts = Counter(word_bag)
    
    most_common_dict= dict(counts.most_common(n=20))
    most_common_df = pd.DataFrame()
    
    keys = []
    values = []
    for key, value in most_common_dict.items():
        keys.append(key)
        values.append(value)

    most_common_df['term'] = keys
    most_common_df['freq'] = values

    sns.set_style("whitegrid")

    palette = sns.color_palette("deep")
    fig = sns.catplot(x="freq", y="term", data=most_common_df, kind="bar", orient="horizontal", palette=palette)
    fig.ax.set(xlabel=None, ylabel=None)
    fig.savefig("./static/img/countplot.png")
    plt.close()

    ax = sns.countplot(y='source', data=data, palette=palette)
    ax.set(xlabel=None, ylabel=None)
    fig = ax.get_figure()
    fig.savefig("./static/img/pie.png", bbox_inches = "tight")
    plt.close()

    word_bag, sentence_bag = TextAnalyzer.prepare_data(data, ["incipit"])
    wc = WordCloud(background_color="white", max_words=150, width=1280, height=250, 
               contour_width=4, contour_color='white', colormap="twilight_shifted")

    wc.generate_from_text(' '.join(word_bag))
    wc.to_file("./static/img/incipit.png")

    return render_template('insights.html', feed_title="📈 Insights", count_plot="countplot.png", pie_chart="pie.png", count_plot_incipit="incipit.png")


if __name__ == '__main__':
    app.run(debug=True)
    #ui.run()
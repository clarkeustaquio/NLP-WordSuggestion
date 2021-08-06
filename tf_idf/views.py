import re
import requests
import json

from django.shortcuts import render

from bs4 import BeautifulSoup
from bs4.element import Comment

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

from sklearn.feature_extraction.text import TfidfVectorizer


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def perform_scraping(url):
    response = requests.get(url)
    if response.status_code != 200: return str()
    else:
        soup = BeautifulSoup(response.text, 'lxml')
        find_all = soup.findAll(text=True)
        text_page = filter(tag_visible, find_all)

        full_text = ''
        for text in text_page:
            full_text += text.strip().lower() + ' '

        stop_words = stopwords.words('english')
        tokens = word_tokenize(full_text)

        tokenize = list()
        punctuation = re.compile(r"[-.?!,:;()'`|0-9]")
        for token in tokens:
            word = punctuation.sub("", token)
            if word: tokenize.append(word)

        new_token = list()
        for token in tokenize:
            if token not in stop_words and len(token) > 1:
                new_token.append(token)

        clean_data = ''
        stemmer = PorterStemmer()
        for token in new_token:
            clean_data += stemmer.stem(token) + ' '    

        return clean_data

def scrape(request):
    significant = list()
    labels = list()
    data = list()

    # https://www.short-story.me/
    urls = [
        "https://www.short-story.me/stories/crime-stories/1312-imperfect",
        "https://www.short-story.me/stories/science-fiction-stories/1311-rite-of-passage",
        "https://www.short-story.me/stories/general-stories/1310-a-drunken-uncles-bedtime-story",
        "https://www.short-story.me/stories/crime-stories/1309-liars",
        "https://www.short-story.me/stories/general-stories/1308-embracing-the-night",
        "https://www.short-story.me/stories/flash-fiction/1307-pixie-pickings",
        "https://www.short-story.me/stories/crime-stories/1306-the-victim",
        "https://www.short-story.me/stories/horror-stories/1305-an-old-friend-returns",
        "https://www.short-story.me/stories/fantasy-stories/1304-old-boots",
        "https://www.short-story.me/stories/general-stories/1303-a-peculiar-way-to-tell-a-story"
    ]

    # The cycle is ridden on the track
    # The bus is driven on the road.
    
    # to_vectorize = [
    #     'The cycle is ridden on the track.',
    #     'The bus is driven on the road.',
    # ]

    to_vectorize = list()
    for url in urls:
        to_vectorize.append(perform_scraping(url))

    vectorize = TfidfVectorizer()
    if len(to_vectorize) > 1:
        vectorize.fit(to_vectorize)

        significant = list()
        for index, key in enumerate(vectorize.vocabulary_.items()):
            significant.append({
                'word': key[0],
                'frequency': key[1],
                'score': vectorize.idf_[index]
            })

        sorted_by_score = sorted(significant, key=lambda item: item['score'], reverse=True)[:10]
        sorted_by_frequency = sorted(sorted_by_score, key=lambda item: item['frequency'], reverse=True)

        labels = [item['word'] for item in sorted_by_frequency]
        data = [item['frequency'] for item in sorted_by_frequency]
    
    return render(request, 'tf_idf/index.html', {
        'labels': json.dumps(labels),
        'data': json.dumps(data),
        'urls': urls
    })
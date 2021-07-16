import re

from django.shortcuts import render

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, brown
from nltk.probability import FreqDist

# Create your views here.
def index(request):
    value = str()
    most_common = list()

    if request.method == 'POST':
        targets = request.POST['sentence'].strip()
        tokens = word_tokenize(targets)

        punctuation = re.compile(r"[-.?!,:;()'`|0-9]")
        tokenize = list()
        for token in tokens:
            word = punctuation.sub("", token)
            
            if word:
                tokenize.append(word)

        target = tokenize[-1]

        frequency = FreqDist()
        brown_corpora = brown.words()
        stopwords_check = stopwords.words('english')

        remover = re.compile(r"[-.?!,:;()'`|0-9]")
        for corpora in brown_corpora:
            word = remover.sub("", corpora)

            if len(word) > 0 and word.lower() not in stopwords_check:
                if word.startswith(target):
                    frequency[word.lower()] += 1

        most_common = frequency.most_common(10)

        tokenize[-1] = most_common[0][0]

        for token in tokenize:
            value += token.title() + ' '

    return render(request, 'generator/index.html', {
        'value': value,
        'most_common': most_common
    })
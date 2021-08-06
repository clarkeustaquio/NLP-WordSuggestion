from django.shortcuts import render
import nltk
from nltk import word_tokenize, pos_tag, RegexpParser

# Create your views here.
def chunk(request):
    noun_phrase = list()
    verb_phrase = list()

    nouns = [
        'A vase of roses stood on the table.',
        'A box of shoes hidden in the bag.',
        'She was reading a book about the emancipation of women.',
        'She wrote a book about the world of men.'
    ]

    verbs = [
        'She had been living in London.',
        'I will be working to a certain company.',
        'I will be going to college next year.',
        'She had been working for a day.'
    ]
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key == 'noun_phrase':
                rule = 'NP: {<DT>*<NN>*<IN><JJ>*<NNS>}'
                sentence = request.POST['noun_phrase']
                tokenize, trees = _parser(sentence, rule)

                noun_phrase = get_leaves(tokenize, trees)

                return render(request, 'word_chunk/chunker.html', {
                    'noun_phrase': noun_phrase
                })

            elif key == 'verb_phrase':
                rule = 'VP: {<MD>?<VB>?<VBD>?<VBN>?<VBG>}'
                sentence = request.POST['verb_phrase']
                tokenize, trees = _parser(sentence, rule)

                verb_phrase = get_leaves(tokenize, trees)

                return render(request, 'word_chunk/chunker.html', {
                    'verb_phrase': verb_phrase
                })
                
    return render(request, 'word_chunk/chunker.html', {
        'noun_phrase': noun_phrase,
        'verb_phrase': verb_phrase
    })

def _parser(sentence, rule):
    tokenize = word_tokenize(sentence)
    tag = pos_tag(tokenize)
    chunk = RegexpParser(rule)
    trees = chunk.parse(tag)

    return tokenize, trees

def get_leaves(tokenize, trees):
    leaves = list()
    roots = list()

    for tree in trees:
        if type(tree) is nltk.Tree:
            leaves = [leave[0] for leave in tree.leaves()]

    for token in tokenize:
        if token in leaves:
            roots.append({
                'character': token,
                'is_phrase': True 
            })
        else:
            roots.append({
                'character': token,
                'is_phrase': False 
            })

    return roots
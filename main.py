from flask import Flask, render_template, request, flash
from forms import AnalyzeForm
import json
import re
import nltk
from nltk.collocations import *
from nltk.tokenize.toktok import ToktokTokenizer
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SECRET_KEY'] = '7b7e30111ddc1f8a5b1d80934d336798'

@app.route('/')
def index():
  return render_template('index.html', data=None)

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
  form = AnalyzeForm()
  data = None
  
  if form.validate_on_submit():
    filename = secure_filename(form.jsonFile.data.filename)
    # form.jsonFile.data.save('tmp/questions.json')
    form.jsonFile.data.seek(0)
    data = json.loads(form.jsonFile.data.read())
    texts = [data["data"]["tossups"][i]["text"] for i in range(len(data["data"]["tossups"]))]
    
    MAX_RESULTS = form.maxResults.data
    NUM_QUESTIONS = len(texts)
    automatic = True #Will be added later release.
    
    # Replace separators and punctuation with spaces
    text = re.sub(r'[.!?,:;/\-\s]', ' ', ' '.join(texts))
    # Remove extraneous chars
    text = re.sub(r'[\\|@#“”*$&~%\(\)*\"]', '', text)
    text = text.lower()
    
    toktok = ToktokTokenizer()
    STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
    quizbowlKeywords = ['title', 'character', 'points', 'work', 'novel', 'poem', 'book', 'name', 'story', 'man', 'one', 'narrator', 'novella', 'author', 'another', 'found', 'comes', 'come', 'called', 'poet', 'speaker', 'like', 'opens', 'includes', 'piece', 'begins', 'use', 'used', 'features', 'played', 'within', 'written', 'composer', 'protagonist']
    
    def common_unigrams(text, num=15, otherWords=[]):
      allWords = toktok.tokenize(text)
      allWordDist = nltk.FreqDist(w.lower() for w in allWords)
      #Remove stopwords or quizbowl indicators
      stopwords = STOPWORDS + quizbowlKeywords + otherWords
      allWordExceptStopDist = nltk.FreqDist(w for w in allWords if len(w) > 2 and w.lower() not in stopwords and not any([(w in i) for i in otherWords]))
      return [i[0] for i in allWordExceptStopDist.most_common(num)]
    
    def common_bigrams(text, frequency=0.40, otherWords=[]):
      bigram_measures = nltk.collocations.BigramAssocMeasures()
      
      # change this to read in your data
      finder = BigramCollocationFinder.from_words(toktok.tokenize(text))
      
      # only bigrams that apper at certain frequency
      finder.apply_freq_filter(round(len(texts)*frequency))
      
      ignored_words = STOPWORDS + quizbowlKeywords
      finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in ignored_words or any([(w in i) for i in otherWords]))
      
      # return the 20 n-grams with the highest PMI
      results = finder.nbest(bigram_measures.pmi, 50)
      return [' '.join(i) for i in results]
    
    def common_trigrams(text, frequency=0.40, otherWords=[]):
      trigram_measures = nltk.collocations.TrigramAssocMeasures()
      
      # change this to read in your data
      finder = TrigramCollocationFinder.from_words(toktok.tokenize(text))
      
      # only bigrams that apper at certain frequency
      finder.apply_freq_filter(round(len(texts)*frequency))
      
      ignored_words = STOPWORDS + quizbowlKeywords
      finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in ignored_words or any([(w in i) for i in otherWords]))
      
      # return the 20 n-grams with the highest PMI
      results = finder.nbest(trigram_measures.pmi, 50)
      return [' '.join(i) for i in results]
    
    def common_quadgrams(text, frequency=0.40, otherWords=[]):
      quadgram_measures = nltk.collocations.QuadgramAssocMeasures()
      
      # change this to read in your data
      finder = QuadgramCollocationFinder.from_words(toktok.tokenize(text))
      
      # only bigrams that apper at certain frequency
      finder.apply_freq_filter(round(len(texts)*frequency))
      
      ignored_words = STOPWORDS + quizbowlKeywords
      finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in ignored_words)
      
      # return the 20 n-grams with the highest PMI
      results = finder.nbest(quadgram_measures.pmi, 50)
      return [' '.join(i) for i in results]
    
    def automatic_solving(func, text, automatic, frequency=None, otherWords=[]):
      if automatic:
        startingFrequency = 2/NUM_QUESTIONS
        results = func(text, frequency=startingFrequency, otherWords=otherWords)
        while len(results) > MAX_RESULTS:
          results = func(text, frequency=startingFrequency, otherWords=otherWords)
          startingFrequency += 0.02
        print(startingFrequency)
        return results
      else:
        return func(text, frequency=frequency, otherWords=otherWords)
    
    quadgrams = automatic_solving(common_quadgrams, text, automatic)
    trigrams = automatic_solving(common_trigrams, text, automatic, otherWords=quadgrams)
    bigrams = automatic_solving(common_bigrams, text, automatic, otherWords=quadgrams+trigrams)
    unigrams = common_unigrams(text, num=MAX_RESULTS, otherWords=quadgrams+trigrams+bigrams)
    # print(unigrams)
    # print(bigrams)
    # print(trigrams)
    # print(quadgrams)
  
    data = (unigrams, bigrams, trigrams, quadgrams)
  return render_template('analyze.html', form=form, data=data)

app.run(host='0.0.0.0', port=81)
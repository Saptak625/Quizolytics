from flask import Flask, render_template, request, flash
from forms import AnalyzeForm
import json
import re
import nltk
from nltk.collocations import *
from werkzeug.utils import secure_filename

nltk.download('stopwords')
nltk.download('punkt')

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
    form.jsonFile.data.save('uploads/questions.json')

    texts=[]
    with open('uploads/questions.json', 'r', encoding="utf-8") as f:
      data = json.load(f)
      texts = [data["data"]["tossups"][i]["text"] for i in range(len(data["data"]["tossups"]))]
    
    # Replace separators and punctuation with spaces
    text = re.sub(r'[.!?,:;/\-\s]', ' ', ' '.join(texts))
    # Remove extraneous chars
    text = re.sub(r'[\\|@#“”*$&~%\(\)*\"]', '', text)
  
    quizbowlKeywords = ['title', 'character', 'points', 'work']
    
    def common_unigrams(text, frequency=0.40):
      allWords = nltk.tokenize.word_tokenize(text)
      allWordDist = nltk.FreqDist(w.lower() for w in allWords)
      #Remove stopwords or quizbowl indicators
      stopwords = nltk.corpus.stopwords.words('english') + quizbowlKeywords
      allWordExceptStopDist = nltk.FreqDist(w for w in allWords if len(w) > 2 and w.lower() not in stopwords)
      return [i[0] for i in allWordExceptStopDist.most_common(15)]
    
    def common_bigrams(text, frequency=0.28):
      bigram_measures = nltk.collocations.BigramAssocMeasures()
      
      # change this to read in your data
      finder = BigramCollocationFinder.from_words(nltk.wordpunct_tokenize(text))
      
      # only bigrams that apper at certain frequency
      finder.apply_freq_filter(int(len(texts)*frequency))
      
      ignored_words = nltk.corpus.stopwords.words('english') + quizbowlKeywords
      finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in ignored_words)
      
      # return the 20 n-grams with the highest PMI
      results = sorted(finder.nbest(bigram_measures.pmi, 50))
      return [' '.join(i) for i in results]
  
    data = (common_unigrams(text), common_bigrams(text))
  return render_template('analyze.html', form=form, data=data)

# app.run(host='0.0.0.0', port=81)
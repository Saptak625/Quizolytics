from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed

class AnalyzeForm(FlaskForm):
  jsonFile = FileField("Upload JSON file from QuizDB: ", validators=[FileRequired(), FileAllowed(['json'], 'JSON only!')])
  automatic = BooleanField("Automatic", default="checked")
  maxResults = IntegerField("Max Results: ", default=15)
  unigramNum = IntegerField("Number of Unigrams: ", default=15)
  bigramFreq = DecimalField('Bigram Frequency: ', default=0.2)
  trigramFreq = DecimalField('Trigram Frequency: ', default=0.15)
  quadgramFreq = DecimalField('Quadgram Frequency: ', default=0.1)
  submit = SubmitField('Submit')
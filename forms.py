from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, DecimalField, StringField, SelectMultipleField, SubmitField, FormField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed


class AnalyzeDetailForm(FlaskForm):
    automatic = BooleanField("Automatic", default="checked")
    maxResults = IntegerField("Max Results: ", default=15)
    unigramNum = IntegerField("Number of Unigrams: ", default=15)
    bigramFreq = DecimalField('Bigram Frequency: ', default=0.2)
    trigramFreq = DecimalField('Trigram Frequency: ', default=0.15)
    quadgramFreq = DecimalField('Quadgram Frequency: ', default=0.1)


class AutomaticAnalyzeForm(FlaskForm):
    query = StringField("Answerline Search: ",
                        render_kw={"placeholder": "Query"}, validators=[DataRequired()])
    literature = BooleanField("Literature", default="checked")
    science = BooleanField("Science", default="checked")
    fineArts = BooleanField("Fine Arts", default="checked")
    history = BooleanField("History", default="checked")
    currentEvents = BooleanField("Current Events", default="checked")
    geography = BooleanField("Geography", default="checked")
    religion = BooleanField("Religion", default="checked")
    mythology = BooleanField("Mythology", default="checked")
    philosophy = BooleanField("Philosophy", default="checked")
    socialScience = BooleanField("Social Science", default="checked")
    otherAcademic = BooleanField("Other Academic", default="checked")
    trash = BooleanField("Trash", default="checked")

    americanLit = BooleanField("American", default="checked")
    britishLit = BooleanField("British", default="checked")
    europeanLit = BooleanField("European", default="checked")
    classicalLit = BooleanField("Classical", default="checked")
    worldLit = BooleanField("World", default="checked")
    otherLit = BooleanField("Other", default="checked")

    biology = BooleanField("Biology", default="checked")
    chemistry = BooleanField("Chemistry", default="checked")
    physics = BooleanField("Physics", default="checked")
    math = BooleanField("Math", default="checked")
    otherSci = BooleanField("Other", default="checked")

    visualFA = BooleanField("Visual", default="checked")
    auditoryFA = BooleanField("Auditory", default="checked")
    otherFA = BooleanField("Other", default="checked")

    americanHis = BooleanField("American", default="checked")
    ancientHis = BooleanField("Ancient", default="checked")
    europeanHis = BooleanField("European", default="checked")
    worldHis = BooleanField("World", default="checked")
    otherHis = BooleanField("Other", default="checked")

    difficulty = StringField("Difficulty (1-10): ")
    analyzeDetails = FormField(AnalyzeDetailForm)
    submit1 = SubmitField('Search')


class ManualAnalyzeForm(FlaskForm):
    jsonFile = FileField("Upload JSON file from QuizDB: ", validators=[FileRequired(), FileAllowed(['json'], 'JSON only!')])
    analyzeDetails = FormField(AnalyzeDetailForm)
    submit2 = SubmitField('Submit')

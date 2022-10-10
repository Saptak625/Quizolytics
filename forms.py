from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed

class AnalyzeForm(FlaskForm):
  jsonFile = FileField("Upload JSON file from QuizDB: ", validators=[FileRequired(), FileAllowed(['json'], 'JSON only!')])
  submit = SubmitField('Submit')
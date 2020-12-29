from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ClientLinkForm(FlaskForm):
    placeholder = 'https://www.sec.gov/Archives/edgar/data/1363829/000136382919000003/ex-101termloandec2018.htm'
    url = StringField('EDGAR document URL', default=placeholder, validators=[DataRequired()])
    submit = SubmitField('Submit')

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length

class ValidationForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=2)])
    email = StringField('email', validators=[DataRequired(), Length(min=2)])
    submit = SubmitField('form')

class RadioForm(FlaskForm):
    choices = RadioField('Choose an option', choices=[('category11', '에코라이프: 친환경 상품들'), ('category13', '홈웨어: 편안한 실내복들'), ('category14', '초기성장기 청소년용 속옷'), ('category15', '후기성장기 청소년 + 성인을 위한 속옷')])
    submit = SubmitField('form')

# Citation: https://youtu.be/UIJKdCIEXUQ?si=m6GZ3O54ZYCjmuTT
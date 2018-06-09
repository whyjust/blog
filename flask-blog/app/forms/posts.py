from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField
from wtforms.validators import DataRequired,Length

class Posts(FlaskForm):
    content = TextAreaField('发表博客',validators=[DataRequired(message='帖子可以为空'),Length(min=6,max=100,message='帖子内容为6-100个字')],render_kw={'placeholder':'发表你此刻的感想...','style':'resize:none;'})
    submit = SubmitField('发表')
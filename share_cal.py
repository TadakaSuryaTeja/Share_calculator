from flask import Flask, session, redirect, url_for, render_template
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)


class NameForm(FlaskForm):
    optionname = StringField('What is the Option', validators=[DataRequired()])
    cmp = StringField("Enter the CMP:", validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/", methods=['GET', 'POST'])
def index():
    entry = 0
    target = 0
    stop_loss = 0
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.optionname.data
        session['cmp'] = form.cmp.data
        return redirect(url_for('index'))
    if session.get('cmp') is not None:
        entry, target, stop_loss = share_calculate(session.get('cmp'))

    return render_template('index.html',
                           form=form,
                           name=session.get('name'),
                           cmp=session.get('cmp'),
                           entry=entry,
                           target=target,
                           stop_loss=stop_loss)


def share_calculate(cmp=0):
    """
    Calculates the share price based on the day
    :cmp: Current Market Price
    :return: returns the calculated result
    """
    # Extract today date
    cmp = float(cmp)
    today = date.today()
    entry = 0.0
    target = 0.0
    stop_loss = 0.0
    if today.weekday() == 0:
        entry = 1.3
        target = 1.15
        stop_loss = 0.85
    elif today.weekday() == 1:
        entry = 1.3
        target = 1.15
        stop_loss = 0.85
    elif today.weekday() == 2:
        entry = 1.4
        target = 1.2
        stop_loss = 0.8
    elif today.weekday() == 3:
        entry = 1.5
        target = 1.25
        stop_loss = 0.75
    elif today.weekday() == 4:
        entry = 1.2
        target = 1.1
        stop_loss = 0.9
    elif today.weekday() == 5:
        print("Today is: Saturday")
    else:
        print("Today is: Sunday")

    return entry * cmp, target * cmp, stop_loss * cmp

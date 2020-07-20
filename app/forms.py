from flask_wtf import FlaskForm
from wtforms import RadioField
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.validators import InputRequired
from wtforms.validators import Length

from app.models import Goal, Much_time


class RequestForm(FlaskForm):
    goals = RadioField(
        "goal",
        choices=[(str(goal.id), goal.name_ru) for goal in Goal.query.all()],
        validators=[DataRequired()],
        default=Goal.query.filter(Goal.id == 1).first().id,
    )
    clientName = StringField("clientName", [InputRequired()])
    clientPhone = StringField(
        "clientPhone", [Length(min=6, message="Длина номера должна быть не менее 6")]
    )
    time = RadioField(
        "time",
        choices=[
            (str(much_time.id), much_time.time + " часа в неделю")
            for much_time in Much_time.query.all()
        ],
        default=Much_time.query.filter(Much_time.id == 1).first().id,
    )


class BookingForm(FlaskForm):
    clientName = StringField("clientName", [InputRequired()])
    clientPhone = StringField(
        "clientPhone", [Length(min=6, message="Длина номера должна быть не менее 6")]
    )

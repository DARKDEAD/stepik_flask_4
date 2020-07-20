import random

from flask import render_template
from flask import request
from flask import url_for

from app import app, db
from app.forms import BookingForm
from app.forms import RequestForm
from app.models import Booking, Client, Request
from app.models import Teacher, ReadData, Goal, Schedule


@app.route("/all_teachers/")
@app.route("/")
def render_index():
    teachers_query = Teacher.query.all()
    if not request.path == "/all_teachers/":
        teachers = random.sample(teachers_query, 6)
    else:
        teachers = teachers_query

    return render_template(
        "index.html",
        teachers=teachers,
        pic_goals=ReadData.pic_goal,
        goals=Goal.query.all(),
        href_goals=ReadData.href_goal,
    )


@app.route("/goals/<goal_name>/")
def render_search(goal_name):
    goal = Goal.query.filter(Goal.name == goal_name).first()

    return render_template(
        "goal.html",
        teachers=goal.teachers,
        goal=goal.name_ru,
        pic_goals=ReadData.pic_goal.get(goal_name, ""),
    )


@app.route("/profiles/<int:id_teacher>/")
def render_profile(id_teacher):
    teachers_query = Teacher.query.all()
    schedule = Schedule.query.filter(Schedule.teacher_id == id_teacher).all()
    return render_template(
        "profile.html",
        teacher=teachers_query[id_teacher],
        goals=Goal.query.all(),
        day_week=ReadData.day_week,
        id_teacher=id_teacher,
        schedule=schedule,
    )


@app.route("/request/")
def render_request():
    form = RequestForm()
    return render_template("request.html", form=form)


@app.route("/request_done/", methods=["POST", "GET"])
def render_request_done():
    form = RequestForm()
    if form.validate_on_submit():
        goal = int(form.goals.data)

        name = form.clientName.data
        phone = form.clientPhone.data

        client = Client(name=name, phone=phone)

        db.session.add(client)
        db.session.commit()

        db.session.add(Request(client=client.id, goals=goal, time=int(form.time.data)))
        db.session.commit()

        return render_template(
            "request_done.html",
            goal=Goal.query.filter(Goal.id == goal).first(),
            form=form,
        )
    else:
        return render_template("request.html", form=form)


@app.route("/booking/<int:id_teacher>/<int:id_schedule>/")
def render_booking(id_teacher, id_schedule):
    teachers_query = Teacher.query.filter(Teacher.id == id_teacher).first()
    schedule_query = Schedule.query.filter(Schedule.id == id_schedule).first()
    form = BookingForm()
    return render_template(
        "booking.html",
        form=form,
        teacher=teachers_query,
        day=ReadData.day_week.get(schedule_query.day_week, ""),
        schedule=schedule_query,
    )


@app.route("/booking_done/", methods=["GET", "POST"])
def render_booking_done():
    teacher = Teacher.query.filter(
        Teacher.id == int(request.form.get("clientTeacher"))
    ).first()
    schedule = Schedule.query.filter(
        Schedule.id == int(request.form.get("schedule"))
    ).first()

    form = BookingForm()
    if form.validate_on_submit():
        name = form.clientName.data
        phone = form.clientPhone.data

        client = Client(name=name, phone=phone)

        db.session.add(client)
        # TODO
        # изменить ли структуру модели Client
        # так что бы хранил не id и ссылку
        # тогда можно без коммита
        db.session.commit()

        db.session.add(
            Booking(client=client.id, teacher=teacher.id, schedule=schedule.id)
        )
        db.session.commit()

        return render_template(
            "booking_done.html",
            name=name,
            phone=phone,
            day=ReadData.day_week.get(schedule.day_week, ""),
            time=schedule.time,
        )
    else:
        return url_for("booking.html")

from app import db

teacher_goal = db.Table(
    "teacher_goals",
    db.Column("teacher", db.Integer, db.ForeignKey("teachers.id")),
    db.Column("goal", db.Integer, db.ForeignKey("goals.id")),
)


class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=True)
    about = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    price = db.Column(db.Integer, nullable=True)
    picture = db.Column(db.String(255), nullable=True)

    goals = db.relationship("Goal", secondary=teacher_goal, back_populates="teachers")
    booking = db.relationship("Booking")
    schedule = db.relationship("Schedule")


class Goal(db.Model):
    __tablename__ = "goals"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=True)
    name_ru = db.Column(db.String(255), nullable=True)

    requests = db.relationship("Request")
    teachers = db.relationship(
        "Teacher", secondary=teacher_goal, back_populates="goals"
    )


class Request(db.Model):
    __tablename__ = "requests"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.Integer, db.ForeignKey("much_time.id"))
    goals = db.Column(db.Integer, db.ForeignKey("goals.id"))
    client = db.Column(db.Integer, db.ForeignKey("clients.id"))

    goal = db.relationship("Goal", back_populates="requests")


class Much_time(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.String(255), nullable=True)

    request = db.relationship("Request")


class Client(db.Model):
    __tablename__ = "clients"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(255), nullable=True)

    booking = db.relationship("Booking")
    request = db.relationship("Request")


class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client = db.Column(db.Integer, db.ForeignKey("clients.id"))
    teacher = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    schedule = db.Column(db.Integer, db.ForeignKey("schedule.id"))


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    free = db.Column(db.Boolean, default=False)
    day_week = db.Column(db.String(255), nullable=True)
    time = db.Column(db.String(255), nullable=True)

    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    teacher = db.relationship("Teacher")
    booking = db.relationship("Booking")


class ReadData(object):
    # teachers = db.session.query(Teacher).all()
    pic_goal = {"travel": "⛱", "study": "🏫", "work": "🏢", "relocate": "🚜"}
    href_goal = {
        "travel": "travel/",
        "study": "study/",
        "work": "work/",
        "relocate": "relocate/",
        "programming": "programming/",
    }
    day_week = {
        "mon": "Понедельник",
        "tue": "Вторник",
        "wed": "Среда",
        "thu": "Четверг",
        "fri": "Пятница",
        "sat": "Суббота",
        "sun": "Воскресенье",
    }

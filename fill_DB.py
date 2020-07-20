import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Goal, Teacher, Schedule, Much_time
from data import goals, teachers

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

engine = create_engine(os.getenv("DEVELOPMENT_DATABASE_URI"))

session = sessionmaker()
session.configure(bind=engine)
s = session()

goal_in_db = dict()

for g_key, g_value in goals.items():
    # Model GOAL
    g = Goal(name=g_key, name_ru=g_value)
    s.add(g)
    goal_in_db[g_key] = g

for teacher in teachers:

    # Model TEACHER
    t = Teacher(
        name=teacher["name"],
        about=teacher["about"],
        rating=teacher["rating"],
        picture=teacher["picture"],
        price=teacher["price"],
    )

    # Model Teacher_goal
    for goal in teacher["goals"]:
        t.goals.append(goal_in_db[goal])

    s.add(t)

    # Model SCHEDULE
    for sc in teacher["free"]:
        for day_key, day_value in teacher["free"][sc].items():
            sh = Schedule(free=day_value, day_week=sc, time=day_key,)
            sh.teacher = t
            s.add(sh)

# Model Much_time
s.add(Much_time(time="1-2"))
s.add(Much_time(time="3-5"))
s.add(Much_time(time="5-7"))
s.add(Much_time(time="7-10"))

s.commit()

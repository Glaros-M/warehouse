import os.path

from flask import Flask

from views import render_warehouse_remains, render_technic_remains, render_histogram
from busines_logic import init_db

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
from db import engine
from sqlalchemy.orm import Session


@app.route("/")
def index():
    return "hello_world"


@app.route("/warehouse-report")
def warehouse_remains():
    s = Session(engine)
    return render_warehouse_remains(session=s)


@app.route("/technic-report")
def technic_remains():
    s = Session(engine)
    return render_technic_remains(session=s)


@app.route("/technic-report/histogram")
def get_histogram():
    s = Session(engine)
    return render_histogram(session=s)


if __name__ == '__main__':
    if not os.path.exists("sqlite3.db"):
        init_db()
    app.run(debug=True)

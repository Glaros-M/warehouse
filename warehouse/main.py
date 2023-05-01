from flask import Flask

from views import render_warehouse_remains

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
    return 'Technic_remains'


@app.route("/technic-report/histogram")
def get_histogram():
    return "histogram"


if __name__ == '__main__':
    app.run(debug=True)

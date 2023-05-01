from jinja2 import Environment, FileSystemLoader
from sqlalchemy.orm import Session
from busines_logic import (
    get_remains_for_all_warehouse,
    get_all_remains_for_technics,
    get_diagram)
env = Environment(
    loader=FileSystemLoader('./static')
)


def render_warehouse_remains(*, session: Session):
    remains = get_remains_for_all_warehouse(session=session)
    tamplate = env.get_template('report_all_warehouse_remains.html')
    return tamplate.render(data=remains)

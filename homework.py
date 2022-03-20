import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase):
    __tablename__ = ''

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    job = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    collaborators = sqlalchemy.Column(sqlalchemy.PickleType, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    end_date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)




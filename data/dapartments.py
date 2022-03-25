import datetime
import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Departments(SqlAlchemyBase):
    __tablename__ = 'departments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chef_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True)
    chef = orm.relation("User")
    members = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    department_email = sqlalchemy.Column(sqlalchemy.String, nullable=False)

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base

from models.user import User
from models.project import Project


class DBSessionManage(object):
    "Class to manage database session"

    def __init__(self, database):
        """
        Start session
        :param str database: Database
        """
        self.database = database
        try:
            self.engine = self.get_server_connection()
            self.engine.connect()
            self.engine.execute('USE `{0}`'.format(database))
            self.create_tables(self.engine)

        except OperationalError as error:
            self.sql_database_connection_error(str(error))
        except Exception as error:
            self.sql_database_connection_error(str(error))

    def get_db_session(self):
        """Generate db session"""
        session = sessionmaker(bind=self.engine)

        return session()

    def sql_database_connection_error(self, error):
        """
        Mysql database connection error
        :param str error: Error
        """
        if 'Connection refused' in error:
            raise Exception('Error on connect to database server')
        else:
            raise Exception(error)

    @staticmethod
    def create_tables(engine):
        """
        Create tables
        :param MysqlConnection engine: Mysql connection engine
        """
        Base = declarative_base()

        tables = [
            Project().__table__,
            User().__table__
        ]

        Base.metadata.create_all(engine, tables)

    @staticmethod
    def get_server_connection():
        """
        Get server connection
        :return Engine: Server connection
        """
        return create_engine(
            # to implement
        )

import datetime

from sqlalchemy import BigInteger, Column, DateTime, String, asc, desc, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

MYSQL_BASE = declarative_base()


class Project(MYSQL_BASE):
    """Project Model"""
    __tablename__ = "project"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, server_default=text('now()'))
    deadline = Column(DateTime)
    description = Column(String(500), nullable=False)
    designated = relationship("User", back_populates='project')
    leader = relationship("User", back_populates='project')
    status = Column(String(30), nullable=False, default='analysis')
    title = Column(String(100), nullable=False)
    updated_at = Column(DateTime, server_default=text('now()'))

    def to_dict(self):
        """
        Return project details in dict format
        :return Project
        """
        return {
            'id': self.id,
            'created_at': self.created_at,
            'deadline': self.deadline,
            'description': self.description,
            'designated': self.designated,
            'leader': self.leader,
            'status': self.status,
            'title': self.title,
            'updated_at': self.updated_at
        }

    @classmethod
    def get_by_id(cls, id, db_session):
        """
        Get Project by id
        :param int id: Project id
        :param session db_session: Database session
        :return Project
        """
        return db_session.query(cls).filter(
            cls.id == id
        ).first()

    @classmethod
    def get_by_designated(cls, contact_key, db_session):
        """
        Get projects by designated
        :param str contact_key: Contact db key
        :param session db_session: Database session
        :return list of project
        """
        return db_session.query(cls).filter(
            cls.designated == contact_key
        )

    @classmethod
    def get_by_leader(cls, contact_key, db_session):
        """
        Get projects by leader
        :param str contact_key: Contact db key
        :param session db_session: Database session
        :return list of project
        """
        return db_session.query(cls).filter(
            cls.leader == contact_key
        )

    @classmethod
    def get_by_status(cls, status, db_session):
        """
        Get projects by status
        :param str status: Project status
        :param session db_session: Database session
        :return: All project by status
        """
        return db_session.query(cls).filter(
            cls.status == status
        )

    @classmethod
    def get_by_filter_params(cls, params, db_session):
        """
        Get projects by filter params
        :param dict params: Params to filter
        :param session db_session: Database session
        :return: All project by filter params
        """
        sort_by = desc if params.get('sort_by') == 'desc' else asc
        order_by = getattr(cls, params['order_by']) if params.get('order_by') else cls.created_at

        query = cls.set_default_fields(db_session)
        query = cls._query_add_filter(query, params).order_by(
            sort_by(order_by), cls.title)
        return query.all(), query.count()

    @classmethod
    def set_default_fields(cls, db_session):
        """
        Query to get list of projects with default fields
        :param session db_session: Database session
        :return Query: Query to get project list
        """
        return db_session.query(
            cls.id, cls.created_at, cls.deadline,
            cls.description, cls.designated, cls.leader,
            cls.status, cls.title, cls.updated_at
        )

    @classmethod
    def _query_add_filter(cls, query, params):
        """
        Add filter conditions in query
        :param Query query: Query
        :param dict params: Filter params
        :return Query: Query with filters
        """
        if params.get('start_at'):
            query = query.filter(cls.created_at >= params['start_at'])
        if params.get('end_at'):
            query = query.filter(cls.created_at <= params['end_at'])
        if params.get('status'):
            if isinstance(params['status'], list):
                query = query.filter(cls.status.in_(params['status']))
            elif params['status'] == 'overdue':
                query = query.filter(cls.status != 'finished')
                query = query.filter(cls.deadline < datetime.now().date())
            else:
                query = query.filter(cls.status == params['status'])

        return query

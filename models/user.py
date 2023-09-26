from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String, text
from sqlalchemy.ext.declarative import declarative_base

MYSQL = declarative_base()


class User(MYSQL):
    """User Model"""
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, server_default=text('now()'))
    fullname = Column(String(100), nullable=False)
    projects_designated = Column(BigInteger, ForeignKey('project.id'), nullable=True)
    projects_leader = Column(BigInteger, ForeignKey('project.id'), nullable=True)
    updated_at = Column(DateTime, server_default=text('now()'))

    def to_dict(self):
        """
        Return user details in dict format
        :return User
        """
        return {
            'id': self.id,
            'created_at': self.created_at,
            'fullname': self.fullname,
            'projects_designated': self.projects_designated,
            'projects_leader': self.projects_leader,
            'updated_at': self.updated_at
        }

    @classmethod
    def get_by_id(cls, id, db_session):
        """
        Get User by id
        :param int id: User id
        :param session db_session: Database session
        :return User
        """
        return db_session.query(cls).filter(
            cls.id == id
        ).first()

    @classmethod
    def get_by_fullname(cls, name, db_session):
        """
        Get User by id
        :param str name: User name
        :param session db_session: Database session
        :return User
        """
        return db_session.query(cls).filter(
            cls.fullname == name
        ).first()

    @classmethod
    def get_leader_by_project_id(cls, project_id, db_session):
        """
        Get User leader by project id
        :param int project_id: Project id
        :param session db_session: Database session
        :return User
        """
        return db_session.query(cls).filter(
            cls.projects_leader == project_id
        ).all()

    @classmethod
    def get_designated_by_project_id(cls, project_id, db_session):
        """
        Get User designated by project id
        :param int project_id: Project id
        :param session db_session: Database session
        :return User
        """
        return db_session.query(cls).filter(
            cls.projects_designated == project_id
        ).all()

from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.orm import sessionmaker
from .base import Base


class DatabaseService:

    def __init__(self, user, host, db_name):
        self.db_name = db_name
        self.url = 'mysql://{0}@{1}/{2}?charset=utf8'.format(
            user, host, db_name)
        self.create_connection()
        self.init_database()

    def create_connection(self):
        print('Creating connection...')
        self.engine = create_engine(self.url)

    def init_database(self):

        if not database_exists(self.url):
            print('Creating database {0}...'.format(self.db_name))
            create_database(self.engine.url, encoding='utf8')

        print('Initializing database {0}...'.format(self.db_name))
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

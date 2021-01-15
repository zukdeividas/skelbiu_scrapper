from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.orm import sessionmaker
from .base import Base


class DatabaseService:

    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.create_connection()
        self.init_database()

    def create_connection(self):
        print('Creating connection...')
        self.engine = create_engine(self.connection_string)

    def init_database(self):

        if not database_exists(self.connection_string):
            print('Creating database...')
            create_database(self.engine.url, encoding='utf8')

        print('Initializing database...')
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

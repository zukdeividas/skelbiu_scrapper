from sqlalchemy import *
from dataclasses import dataclass
from .base import Base
from sqlalchemy.orm import relationship


@dataclass
class HousePost(Base):
    __tablename__ = 'house_posts'
    id = Column('id', Integer, primary_key=True)
    post_inner_id = Column('post_inner_id', String(15))
    original_url = Column('original_url', String(200))
    town = Column('town', String(30))
    street = Column('street', String(50))
    room_count = Column('room_count', Integer)
    year = Column('year', Integer)
    heating = Column('heating', String(100))
    house_area = Column('house_area', Integer)
    land_area = Column('land_area', Integer)
    description = Column('description', Text)
    price = Column('price', Integer)
    is_new = Column('is_new', Boolean)
    is_liked = Column('is_liked', Boolean)
    image_urls = relationship(
        "HouseImage", backref='parent', passive_deletes=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name)
                for c in self.__table__.columns}

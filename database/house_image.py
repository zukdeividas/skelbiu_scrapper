from sqlalchemy import *
from .base import Base


class HouseImage(Base):
    __tablename__ = 'house_images'
    id = Column('id', Integer, primary_key=True)
    image_url = Column('image_url', String(1000))
    post_id = Column(Integer, ForeignKey('house_posts.id', ondelete='CASCADE'))

    def as_dict(self):
        return {c.name: getattr(self, c.name)
                for c in self.__table__.columns}

from flask import Flask, jsonify, request
from flask_classy import FlaskView, route
from database.database_service import DatabaseService
from database.house_post import HousePost
from flask_cors import CORS
from sqlalchemy import inspect
import os


class ApiView(FlaskView):
    route_base = '/'

    def __init__(self):
        self.api = Flask(
            __name__, static_folder='./scraper_ui/build', static_url_path='/')
        self.api.config["DEBUG"] = False
        CORS(self.api)

    def init(self):
        return self.api

    def index(self):
        return self.api.send_static_file('index.html')

    @route('/api/posts', )
    def get_all(self, sort=''):
        filter_param = request.args.to_dict()

        database = DatabaseService(os.getenv('DATABASE_CONNECTOR'))
        session = database.get_session()

        filters = []

        if filter_param['is_new'] == 'true':
            print('Filter is_new')
            filters.append(HousePost.is_new == True)
        if filter_param['is_liked'] == 'true':
            print('Filter is_liked')
            filters.append(HousePost.is_liked == True)

        posts_from_db = session.query(HousePost).filter(*filters).all()

        posts_to_return = []
        for post in posts_from_db:
            images = []
            post_dict = post.as_dict()
            for image in post.image_urls:
                images.append(image.as_dict()['image_url'])
            post_dict['image_urls'] = images

            posts_to_return.append(post_dict)
        return jsonify(posts_to_return)

    @route('/api/posts/<id>/liked')
    def change_like_status(self, id):
        print(id)
        database = DatabaseService(os.getenv('DATABASE_CONNECTOR'))
        session = database.get_session()

        post = session.query(HousePost).filter_by(
            id=id).first()
        post.is_liked = not post.is_liked

        session.commit()
        return jsonify({'success': True})

    @route('/api/posts/<id>/seen')
    def change_seen_status(self, id):
        print(id)
        database = DatabaseService(os.getenv('DATABASE_CONNECTOR'))
        session = database.get_session()

        post = session.query(HousePost).filter_by(
            id=id).first()
        post.is_new = False

        session.commit()
        return jsonify({'success': True})

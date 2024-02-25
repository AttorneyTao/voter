#encoding:utf-8
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import csv
from .extensions import db
from .models import Voter,Poll, Option


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../vote_app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    from .route import bp
    app.register_blueprint(bp)

    @app.cli.command('init-db')
    def init_db_command():
        db.create_all()
        print('Initialized the database.')
        with open(r'./app/voters.csv', mode='r') as file:  # 调整路径根据实际位置
            reader = csv.DictReader(file)
            for row in reader:
                voter = Voter(name=row['name'])
                db.session.add(voter)
        db.session.commit()
        #初始化投票轮次
        poll1 = Poll(title='高级合伙人委员选举', max_votes=4)
        db.session.add(poll1)
        db.session.commit()
        poll2 = Poll(title='有限合伙人委员选举', max_votes=5)
        db.session.add(poll2)
        db.session.commit()
        poll3 = Poll(title='专职律师及律师助理委员选举', max_votes=5)
        db.session.add(poll3)
        db.session.commit()
        #初始化高伙候选人
        for name in ['王春华','侍文文','赵宸','王卓','郭如璞']:
            opt=Option(title=name, poll_id=poll1.id)
            db.session.add(opt)
        db.session.commit()
        #初始化二伙候选人
        for name in ['李艳红','陈丹','张楚','黄杨林','马芳林','徐娇']:
            opt=Option(title=name, poll_id=poll2.id)
            db.session.add(opt)
        db.session.commit()
        #初始化助理候选人
        for name in ['祝心怡','曹胜男','李林','孙红丽','董昕怡','孙馨怡']:
            opt=Option(title=name, poll_id=poll3.id)
            db.session.add(opt)
        db.session.commit()
        



        db.session.commit()


    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    return app
    

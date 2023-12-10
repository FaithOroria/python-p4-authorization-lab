from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Article(db.Model, SerializerMixin):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String)
    title = db.Column(db.String)
    content = db.Column(db.String)
    preview = db.Column(db.String)
    minutes_to_read = db.Column(db.Integer)
    is_member_only = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, server_default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        data = {
            'id': self.id,
            'author': self.author,
            'title': self.title,
            'content': self.content,
            'preview': self.preview,
            'minutes_to_read': self.minutes_to_read,
            'is_member_only': self.is_member_only,
            'date': self.date.isoformat() if self.date else None
        }

        return data

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)

    articles = db.relationship('Article', backref='user')

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'articles': [article.to_dict() for article in self.articles]
        }

        return data

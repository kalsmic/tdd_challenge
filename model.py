"""
This module contains the models for our application
"""
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)

    def insert(self):
        """
        Insert a new user into the database
        The user must not exist in the database
        EXAMPLE:
            user = User(username='joe')
            user.insert()
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Update an existing user in the database
        The user must exist in the database
        EXAMPLE:
            user = User.query.filter(User.username == 'joe').first_or_404()
            user.username = 'joe2'
            user.update()
        """
        db.session.commit()

    def delete(self):
        """
        Delete an existing user from the database
        The user must exist in the database
        EXAMPLE:
            user = User.query.filter(User.username == 'joe').first_or_404()
            user.delete()
        """
        db.session.delete(self)
        db.session.commit()

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'username': self.username
        }

    def __repr__(self):
        """
        Representation of the User object"""
        return f"User('{self.id} {self.username}')"

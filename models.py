import datetime

from app import db

#
# class BaseModel(db.Model):
#     """Base data model for all objects"""
#     __abstract__ = True
#
#     def __init__(self, *args):
#         super().__init__(*args)
#
#     def __repr__(self):
#         """Define a base way to print models"""
#         return '%s(%s)' % (self.__class__.__name__, {
#             column: value
#             for column, value in self._to_dict().items()
#         })
#
#     def json(self):
#         """
#                 Define a base way to jsonify models, dealing with datetime objects
#         """
#         return {
#             column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
#             for column, value in self._to_dict().items()
#         }


class Room(db.Model):
    __tablename__ = 'ROOMS'
    # define your model
    roomId = db.Column(db.Integer, primary_key=True)
    roomName = db.Column(db.String)


class Assignment(db.Model):
    __tablename__ = "ASSIGNMENTS"

    assignmentId = db.Column(db.Integer, primary_key=True)
    assignedUser = db.Column(db.String)
    createdUser = db.Column(db.Integer)
    assignmentName = db.Column(db.String)
    date = db.Column(db.Date)
    completed = db.Column(db.Boolean)
    roomId = db.Column(db.Integer)


class UserRegistration(db.Model):
    __tablename__ = "REGISTERED_USERS"

    entryId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    roomId = db.Column(db.Integer)

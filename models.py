from flask_migrate import Migrate
from app import app, db


migrate = Migrate(app, db)

class Room(db.Model):
    __tablename__ = 'ROOMS'
    # define your model
    roomId = db.Column(db.Integer, primary_key=True)
    roomName = db.Column(db.String)

    def json(self):
        return {
            'roomId': self.roomId,
            'roomName': self.roomName
        }


class Assignment(db.Model):
    __tablename__ = "ASSIGNMENTS"

    assignmentId = db.Column(db.Integer, primary_key=True)
    assignedUser = db.Column(db.String)
    createdUser = db.Column(db.String)
    assignmentName = db.Column(db.String)
    date = db.Column(db.Date)
    completed = db.Column(db.Boolean)
    roomId = db.Column(db.Integer)

    def json(self):
        return {
            "assignmentId": self.assignmentId,
            "assignedUser": self.assignedUser,
            "createdUser": self.createdUser,
            "assignmentName": self.assignmentName,
            "date": self.date,
            "completed": self.completed,
            "roomId": self.roomId
        }


class UserRegistration(db.Model):
    __tablename__ = "USER_REGISTRATIONS"

    entryId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String)
    roomId = db.Column(db.Integer)

    def json(self):
        return {
            "userId": self.userId,
            "roomId": self.roomId
        }

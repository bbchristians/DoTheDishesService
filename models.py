from flask_migrate import Migrate
from app import app, db


migrate = Migrate(app, db)


class Room(db.Model):
    __tablename__ = 'rooms'
    # define your model
    roomid = db.Column(db.Integer, primary_key=True)
    roomname = db.Column(db.String)

    def json(self):
        return {
            'roomId': self.roomid,
            'roomName': self.roomname
        }


class Assignment(db.Model):
    __tablename__ = "assignments"

    assignmentid = db.Column(db.Integer, primary_key=True)
    assigneduser = db.Column(db.String)
    createduser = db.Column(db.String)
    assignmentname = db.Column(db.String)
    date = db.Column(db.Date)
    completed = db.Column(db.Boolean)
    roomid = db.Column(db.Integer)

    def json(self):
        return {
            "assignmentId": self.assignmentid,
            "assignedUser": self.assigneduser,
            "createdUser": self.createduser,
            "assignmentName": self.assignmentname,
            "date": self.date.strftime("%d/%m/%Y"),
            "completed": self.completed,
            "roomId": self.roomid
        }

    def get_id(self):
        return self.assignmentid


class UserRegistration(db.Model):
    __tablename__ = "user_registrations"

    entryid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String)
    roomid = db.Column(db.Integer)

    def json(self):
        return {
            "userId": self.userid,
            "roomId": self.roomid
        }

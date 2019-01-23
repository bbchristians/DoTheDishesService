import app


class Room(app.db.Model):
    __tablename__ = 'ROOMS'
    # define your model
    roomId = app.db.Column(app.db.Integer, primary_key=True)
    roomName = app.db.Column(app.db.String)

    def json(self):
        return {
            'roomId': self.roomId,
            'roomName': self.roomName
        }


class Assignment(app.db.Model):
    __tablename__ = "ASSIGNMENTS"

    assignmentId = app.db.Column(app.db.Integer, primary_key=True)
    assignedUser = app.db.Column(app.db.String)
    createdUser = app.db.Column(app.db.String)
    assignmentName = app.db.Column(app.db.String)
    date = app.db.Column(app.db.Date)
    completed = app.db.Column(app.db.Boolean)
    roomId = app.db.Column(app.db.Integer)

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


class UserRegistration(app.db.Model):
    __tablename__ = "USER_REGISTRATIONS"

    entryId = app.db.Column(app.db.Integer, primary_key=True)
    userId = app.db.Column(app.db.String)
    roomId = app.db.Column(app.db.Integer)

    def json(self):
        return {
            "userId": self.userId,
            "roomId": self.roomId
        }

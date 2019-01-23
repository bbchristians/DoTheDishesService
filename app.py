from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import models

app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'postgres',
    'host': 'localhost',
    'port': '5432',
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db = SQLAlchemy()
db.init_app(app)


@app.route('/create_room', methods=['POST'])
def create_room():
    if not request.is_json:
        return "Expected JSON"

    newRoom = models.Room(roomName=request.json["roomName"])
    db.session.add(newRoom)
    db.session.commit()
    return "Created new room"


@app.route('/get_room', methods=['GET'])
def get_room():
    if not request.is_json:
        return "Expected JSON"

    roomId = request.json["roomId"]

    roomQuery = models.Room.query.filter_by(roomId=roomId)
    roomJson = roomQuery[0].json()

    assignmentsQuery = models.Assignment.query.filter_by(roomId=roomId).all()
    roomJson["assignments"] = list(map(models.Assignment.json, assignmentsQuery))

    # registeredUsersQuery = models.UserRegistration.query.filter_by(roomId=roomId).all()
    # roomJson["registeredUsers"] = registeredUsersQuery

    return jsonify(roomJson)


@app.route('/create_assignment', methods=['POST'])
def create_assignments():
    if not request.is_json:
        return "Expected JSON"

    roomId = request.json["roomId"]
    createdUser = request.json["createdUser"]
    assignments = request.json["assignments"]

    for assignment in assignments:
        newAssignment = models.Assignment(
            roomId=roomId,
            createdUser=createdUser,
            assignedUser=assignment["assignedUser"],
            assignmentName=assignment["name"],
            date=assignment["date"],
            completed=False
        )
        db.session.add(newAssignment)

    db.session.commit()
    return "Created %s assignment(s)" % len(assignments)


if __name__ == '__main__':
    app.run()

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()

import models

# POSTGRES = {
#     'user': 'postgres',
#     'pw': 'postgres',
#     'db': 'postgres',
#     'host': 'localhost',
#     'port': '5432',
# }
#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
# %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://apbsrnockrqxma:41d5ed02a77b3d37a89ec4e49db803ee8460adb13bc33ec2fbb3547d47570452@ec2-107-22-238-186.compute-1.amazonaws.com:5432/di0b2e80kth2v'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
session = db.session


@app.route('/create_room', methods=['POST'])
def create_room():
    if not request.is_json:
        return "Expected JSON"

    newRoom = models.Room(roomname=request.json["roomName"])
    session.add(newRoom)
    session.commit()
    return "Created new room"


@app.route('/get_room', methods=['GET'])
def get_room():
    if not request.is_json:
        return "Expected JSON"

    roomId = request.json["roomId"]

    roomQuery = models.Room.query.filter_by(roomid=roomId)
    roomJson = roomQuery[0].json()

    assignmentsQuery = models.Assignment.query.filter_by(roomid=roomId).all()
    if len(assignmentsQuery) > 0:
        roomJson["assignments"] = list(map(models.Assignment.json, assignmentsQuery))
    else:
        roomJson["assignments"] = []

    registeredUsersQuery = models.UserRegistration.query.filter_by(roomid=roomId).all()
    if len(registeredUsersQuery) > 0:
        roomJson["registeredUsers"] = list(map(models.UserRegistration.json, registeredUsersQuery))
    else:
        roomJson["registeredUsers"] = []

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
            roomid=roomId,
            createduser=createdUser,
            assigneduser=assignment["assignedUser"],
            assignmentname=assignment["name"],
            date=assignment["date"],
            completed=False
        )
        session.add(newAssignment)

    session.commit()
    return "Created %s assignment(s)" % len(assignments)


@app.route('/delete_assignment', methods=['POST'])
def delete_assignment():
    if not request.is_json:
        return "Expected JSON"

    assignmentId = request.json["assignmentId"]

    assignment = models.Assignment.query.filter_by(assignmentid=assignmentId).first()

    o_session = session.object_session(assignment)
    o_session.delete(assignment)
    o_session.commit()

    if( assignment is not None ):
        return "Assignment with id %s deleted" % assignmentId
    return "No assignment found with id " + assignmentId


@app.route('/register_user', methods=['POST'])
def register_user():
    if not request.is_json:
        return "Expected JSON"

    userId = request.json["userId"]
    roomId = request.json["roomId"]

    session.add(models.UserRegistration(userid=userId, roomid=roomId))
    session.commit()

    return "User registered"


if __name__ == '__main__':
    app.run()

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import error
import success
import json

app = Flask(__name__)
db = SQLAlchemy()

import models

# POSTGRES = {
#     'user': 'postgres',
#     'pw': 'postgres',
#     'db': 'dishes',
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
        return error.error_400("Expected JSON")

    try:
        newRoom = models.Room(roomname=request.json["roomName"])
        session.add(newRoom)
        session.commit()
    except KeyError:
        return error.error_400("Missing field in body: 'roomName'")

    if newRoom.roomid is None:
        return error.error_400("Error adding room to database")

    return success.success_200({
        "roomId": newRoom.roomid
    })


@app.route('/get_room', methods=['GET'])
def get_room():
    if not request.is_json:
        return error.error_400("Expected JSON")

    try:
        roomId = request.json["roomId"]
    except KeyError:
        return error.error_400("Missing field in body: 'roomId'")

    roomQuery = models.Room.query.filter_by(roomid=roomId).first()
    if roomQuery is None:
        return error.error_400("No room found with id " + str(roomId))

    roomJson = roomQuery.json()

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

    return success.success_200(roomJson)


@app.route('/create_assignment', methods=['POST'])
def create_assignments():
    if not request.is_json:
        return error.error_400("Expected JSON")

    try:
        roomId = request.json["roomId"]
    except KeyError:
        return error.error_400("Missing field in body: 'roomId'")

    try:
        createdUser = request.json["createdUser"]
    except KeyError:
        return error.error_400("Missing field in body: 'createdUser'")

    try:
        assignments = request.json["assignments"]
    except KeyError:
        return error.error_400("Missing field in body: 'assignments'")

    created_assignments = list()
    for assignment in assignments:
        newAssignment = models.Assignment(
            roomid=roomId,
            createduser=createdUser,
            assigneduser=assignment["assignedUser"],
            assignmentname=assignment["name"],
            date=assignment["date"],
            completed=False
        )
        created_assignments.append(newAssignment)
        session.add(newAssignment)

    if len(created_assignments) == 0:
        return error.error_400("No assignments created")

    session.commit()
    return success.success_200({
        "createdAssignments": list(map(models.Assignment.get_id, created_assignments))
    })


@app.route('/delete_assignment', methods=['POST'])
def delete_assignment():
    if not request.is_json:
        return error.error_400("Expected JSON")

    try:
        assignmentId = request.json["assignmentId"]
    except KeyError:
        return error.error_400("Missing field in body: 'assignmentId'")

    assignment = models.Assignment.query.filter_by(assignmentid=assignmentId).first()
    if assignment is None:
        return error.error_400("No assignment found with assignmentId %s" % assignmentId)

    o_session = session.object_session(assignment)
    o_session.delete(assignment)
    o_session.commit()

    return success.success_200({
        "deletedAssignmentId": assignmentId
    })


@app.route('/register_user', methods=['POST'])
def register_user():
    if not request.is_json:
        return error.error_400("Expected JSON")

    try:
        userId = request.json["userId"]
    except KeyError:
        return error.error_400("Missing key in body: 'userId'")

    try:
        roomId = request.json["roomId"]
    except KeyError:
        return error.error_400("Missing key in body: 'roomId'")

    existingRegistration = models.UserRegistration.query.filter_by(userid=userId, roomid=roomId).first()
    if existingRegistration is not None:
        return success.success_200({
            "registration": existingRegistration.json(),
            "newRegistration": False
        })

    userRegistration = models.UserRegistration(userid=userId, roomid=roomId)
    session.add(userRegistration)
    session.commit()

    return success.success_200({
        "registration": userRegistration.json(),
        "newRegistration": True
    })


if __name__ == '__main__':
    app.run()

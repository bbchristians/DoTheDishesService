from flask import request, jsonify
from server import app, session
import models


@app.route('/create_room', methods=['POST'])
def create_room():
    if not request.is_json:
        return "Expected JSON"

    newRoom = models.Room(roomName=request.json["roomName"])
    session.add(newRoom)
    session.commit()
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

    registeredUsersQuery = models.UserRegistration.query.filter_by(roomId=roomId).all()
    roomJson["registeredUsers"] = list(map(models.UserRegistration.json, registeredUsersQuery))

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
        session.add(newAssignment)

    session.commit()
    return "Created %s assignment(s)" % len(assignments)


@app.route('/delete_assignment', methods=['POST'])
def delete_assignment():
    if not request.is_json:
        return "Expected JSON"

    assignmentId = request.json["assignmentId"]

    assignment = models.Assignment.query.filter_by(assignmentId=assignmentId).first()

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

    session.add(models.UserRegistration(userId=userId, roomId=roomId))
    session.commit()

    return "User registered"


if __name__ == '__main__':
    app.run()

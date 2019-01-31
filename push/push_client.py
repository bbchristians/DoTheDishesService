from pusher_push_notifications import PushNotifications

push_client = PushNotifications(
  instance_id='fc67890c-2ad8-418d-90a7-b4b845cf03c1',
  secret_key='02836FF19BFACC63BC74E0315741445C67E445E31FED4AEFE7493843125A1EB2',
)


def send_push_nudge(userId, roomId, assignmentName):
    return push_client.publish(
        interests=[get_interest_key(userId, roomId)],
        publish_body={
            'fcm': {
                'notification': {
                    'title': "Nudge",
                    'body': "Someone nudged you to %s".format(assignmentName)
                }
            }
        }
    )


def get_interest_key(userId, roomId):
    return userId + '@' + str(roomId)

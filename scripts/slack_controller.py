import requests

SLACK_BLUE = "#0000FF"
SLACK_RED = "#FF4500"
SLACK_GREEN = "#00FF00"


# Sends a specific message to the slack
# message - message that is sent
# chanel - chanel to which the message will be sent
# username - the name of the message
def send_message_in_slack(url, channel, header, message, username, icon_name, color):
    payload = '{"channel": "' + channel + '", "username": "' + username + \
              '", "text": "' + header + \
              '", "icon_emoji": "' + icon_name + \
              '", "attachments": [{ ' \
              '"fallback": "Required plain-text summary of the attachment."' \
              ',"color": "' + color + '"' \
                                      ',"author_name": "' + message + '" }]}'
    response = requests.post(url, data=payload)
    # if an error is returned, throw an exception
    if response.status_code != 200:
        raise NameError("ERROR!! send message slack, err code - " + str(response.status_code))


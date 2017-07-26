import requests


# Sends a specific message to the slack
# message - message that is sent
# chanel - chanel to which the message will be sent
# username - the name of the message
def send_message_in_slack(chanel, header, message, username, icon_name, color):
    url = "https://hooks.slack.com/services/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"
    payload = '{"channel": "' + chanel + '", "username": "' + username + \
              '", "text": "' + header + \
              '", "icon_emoji": "' + icon_name + \
              '", "attachments": [{ ' \
                    '"fallback": "Required plain-text summary of the attachment."' \
                    ',"color": "' + color + '"' \
                    ',"author_name": "' + message + '" }]}'
    response = requests.post(url, data=payload)
    return response




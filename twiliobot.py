import os
from flask import Flask, request, Response
from slackclient import SlackClient
from twilio import twiml
from twilio.rest import TwilioRestClient
import trains
import nba

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET', None)
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', None)
USER_NUMBER = os.environ.get('USER_NUMBER', None)

app = Flask(__name__)
slack_client = SlackClient(os.environ.get('SLACK_TOKEN', None))
twilio_client = TwilioRestClient()


@app.route('/twilio', methods=['POST'])
def twilio_post():
    response = twiml.Response()
    msg_request = request.form['Body']
    print(request.form)
    slack_client.api_call("chat.postMessage", channel="#general",
                              text=msg_request, username=request.form['From'],
                              icon_emoji=':robot_face:')
    msg_response="I could not understand your text. Did you know cats use their tails for balance and have nearly 30 individual bones in them?"
    if "MERCHANDISE MART" in msg_request.upper():
        msg_response=trains.requestTrainSchedule("MERCHANDISE MART")
    elif "SOUTHPORT" in msg_request.upper():
        msg_response=trains.requestTrainSchedule("SOUTHPORT")
    elif "NBA" in msg_request.upper():
        if "POWER" in msg_request.upper():
            msg_response=nba.request("power")
        else:
            msg_response=nba.request("preds")
    if request.form['From'] == USER_NUMBER or True:
        
        slack_client.api_call("chat.postMessage", channel="#general",
                              text=msg_response, username="Joshua Bot",
                              icon_emoji=':robot_face:')
        twilio_client.messages.create(to=request.form['From'], from_=TWILIO_NUMBER,
                                      body=msg_response)
    return Response(response.toxml(), mimetype="text/xml"), 200


@app.route('/slack', methods=['POST'])
def slack_post():
    print(request.form)
    if request.form['token'] == SLACK_WEBHOOK_SECRET:
        channel = request.form['channel_name']
        username = request.form['user_name']
        text = request.form['text']
        response_message = username + " in " + channel + " says: " + text
        twilio_client.messages.create(to=USER_NUMBER, from_=TWILIO_NUMBER,
                                      body=response_message)
    return Response(), 200


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")

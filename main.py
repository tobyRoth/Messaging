from sqlite3 import Error

from flask import Flask, jsonify, request

from messagesDB import messagesDB

app = Flask(__name__)
mDB = messagesDB()


@app.route('/addMessage', methods=['POST'])
def add_message():
    try:
        message_id = request.json['message_id']
        session_id = request.json['session_id']
        application_id = request.json['application_id']
        participants = request.json['participants']
        content = request.json['content']
        msg_row_id = mDB.create_message(message_id, session_id, application_id, participants, content)
        response = "added successfully message number:{} ".format(msg_row_id)
        return jsonify({'response': response})
    except Error as er:
        errorMessage = "{}".format(er)
        return jsonify({'errorMessage': errorMessage})


@app.route('/getMessage', methods=['GET'])
def get_message():
    application_id = request.args.get('application_id', '')
    session_id = request.args.get('session_id', '')
    message_id = request.args.get('message_id', '')
    if application_id:
        key = 'application_id'
        id=application_id
    elif session_id:
        key = 'session_id'
        id=session_id
    elif message_id:
        key = 'message_id'
        id=message_id
    else:
        return jsonify({'message':'No parameters sent please try again'})
    result = mDB.get_messages(key, id)
    received_messages = {"list": result}
    if len(result) == 0:
        response = 'no messages found with {} :{}'.format(key,id)
        return jsonify({'message': response})
    return received_messages

@app.route('/deleteMessage', methods=['DELETE'])
def delete_message():
    application_id = request.args.get('application_id', '')
    session_id = request.args.get('session_id', '')
    message_id = request.args.get('message_id', '')
    if application_id:
        key = 'application_id'
        id = application_id
    elif session_id:
        key = 'session_id'
        id = session_id
    elif message_id:
        key = 'message_id'
        id = message_id
    else:
        return jsonify({'response': 'No parameters sent please try again'})
    if mDB.delete_messages(key, id):
        response = 'message with {} : {} was deleted'.format(key, id)
    else:
       response='message with {} : {} was not found'.format(key, id)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)

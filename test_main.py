from main import app
from flask import json
import json
import random
import math

random.random() * 100

def add_message_for_test( application_id=False, session_id=False, message_id=False,rand_message_id=None ):
    if rand_message_id is None:
       rand_message_id= math.floor(random.random() * 100)
    response = app.test_client().post(
        'http://127.0.0.1:5000/addMessage',
        data=json.dumps({
            "application_id": 3,
            "session_id": "sid5",
            "message_id": str(rand_message_id),
            "participants": ["moshe cohen", "chaim levi", "bracha segal"],
            "content": "how was your day?"}),
        content_type='application/json',
    )
    if application_id:
        return 3
    if session_id:
        return "sid5"
    if message_id:return rand_message_id
    return response


def test_add_message_success():
    response = add_message_for_test()
    assert response.status_code == 200
    assert response.json['response'] is not None


def test_add_message_pK_exist_failed():
    mId = add_message_for_test(False,False,True)
    response = add_message_for_test(False,False,False,mId)
    assert response.status_code == 200
    assert response.json['errorMessage'] is not None


def test_get_messages_by_application_id_success():
    aId = add_message_for_test(True)
    response = app.test_client().get(
        'http://127.0.0.1:5000/getMessage', query_string={'application_id': aId}
    )
    assert response.status_code == 200
    list = response.json['list']
    assert len(list) > -1


def test_get_messages_by_session_id_success():
    sId = add_message_for_test(False, True)
    response = app.test_client().get(
        'http://127.0.0.1:5000/getMessage', query_string={'session_id': sId}
    )
    assert response.status_code == 200
    list = response.json['list']
    assert len(list) > -1


def test_get_message_by_message_id_success():
    mId = add_message_for_test(False,False,True)
    response = app.test_client().get(
        'http://127.0.0.1:5000/getMessage', query_string={'message_id': mId}
    )
    assert response.status_code == 200
    list = response.json['list']
    assert len(list) > -1


def test_delete_message_by_application_id_success():
    aId = add_message_for_test(True)
    # aId = res.json['applicationId']
    response = app.test_client().delete(
        'http://127.0.0.1:5000/deleteMessage', query_string={'application_id': aId}
    )
    assert response.status_code == 200
    assert response.json['response'] is not None


def test_delete_message_by_session_id_success():
    sId = add_message_for_test(False, True)
    response = app.test_client().delete(
        'http://127.0.0.1:5000/deleteMessage', query_string={'session_id': sId}
    )
    assert response.status_code == 200
    assert response.json['response'] is not None


def test_delete_message_by_message_id_success():
    mId = add_message_for_test(False,False,True)
    response = app.test_client().delete(
        'http://127.0.0.1:5000/deleteMessage', query_string={'message_id': mId}
    )
    assert response.status_code == 200
    assert response.json['response'] is not None



from main import app
from flask import json
import json
import random

random.random() * 100

def add_message_for_test( application_id=False, session_id=False, new_message=True, ):
    # if new_message:
    #   cnt += 1
    if new_message:
       message_id= random.random() * 100
    response = app.test_client().post(
        'http://127.0.0.1:5000/addMessage',
        data=json.dumps({
            "application_id": 3,
            "session_id": "sid5",
            "message_id": str(message_id),
            "participants": ["moshe cohen", "chaim levi", "bracha segal"],
            "content": "how was your day?"}),
        content_type='application/json',
    )
    if application_id:
        return 3
    if session_id:
        return "sid5"
    return response


def test_add_message_success():
    response = add_message_for_test()
    assert response.status_code == 200
    assert response.json['response'] is not None


def test_add_message_pK_exist_failed():
    response = add_message_for_test('mid15')
    assert response.status_code == 200
    # assert response.json['lastRawId'] is not None
    assert response.json['errorMessage'] is not None


def test_get_messages_by_application_id_success():
    aId = add_message_for_test('mid3', True)
    response = app.test_client().get(
        'http://127.0.0.1:5000/getMessage', query_string={'application_id': aId}
    )
    assert response.status_code == 200
    list = response.json['list']
    assert len(list) > -1


def test_get_messages_by_session_id_success():
    sId = add_message_for_test('mid4', False, True)
    response = app.test_client().get(
        'http://127.0.0.1:5000/getMessage', query_string={'session_id': sId}
    )
    assert response.status_code == 200
    list = response.json['list']
    assert len(list) > -1


def test_get_message_by_message_id_success():
    res = add_message_for_test('mid4')
    # mId = res.json['messageId']
    response = app.test_client().get(
        'http://127.0.0.1:5000/getMessage', query_string={'message_id': 'mId4'}
    )
    assert response.status_code == 200
    list = response.json['list']
    assert len(list) > -1


def test_delete_message_by_application_id_success():
    aId = add_message_for_test('mid20', True)
    # aId = res.json['applicationId']
    response = app.test_client().delete(
        'http://127.0.0.1:5000/deleteMessage', query_string={'application_id': aId}
    )
    assert response.status_code == 200
    assert response.json['messages'] is not None


def test_delete_message_by_session_id_success():
    sId = add_message_for_test('mid20', False, True)
    # sId = res.json['sessionId']
    response = app.test_client().delete(
        'http://127.0.0.1:5000/deleteMessage', query_string={'session_id': sId}
    )
    assert response.status_code == 200
    assert response.json['messages'] is not None


def test_delete_message_by_message_id_success():
    mId = add_message_for_test('mid20')
    # mId = res.json['messageId']
    response = app.test_client().delete(
        'http://127.0.0.1:5000/deleteMessage', query_string={'message_id': mId}
    )
    assert response.status_code == 200
    assert response.json['message'] is not None

# def test_get_messages_by_message_id_success():
#     response = app.test_client().get(
#         'http://127.0.0.1:5000/getMessage?messageId=mid3'  # .format(self.baseUrl),
#     )
#     data = json.loads(response.().decode('utf-8').replace("'",'"'))
#     assert response.status_code == 200
#     #json.loads(data)
#     # print(data[5])
#     print(type(data))
#     #s = json.dumps(data, indent=4, sort_keys=True)
#     #json_data=json.loads(data['list'])
#     #print(json_data['messageId'])
#     json_data = data['list']
#     x=json.dumps(json_data)
#     y=json.loads(x)
#
#     #if 'messageId' in json_data:
#        # print("yes!!")
#     print(type(json_data))
#     print(x)
#     print(type(x))
#     print(y)
#     print(type(y))
#     #print(json_data['messageId'])
#     #print(type(s))
#     # assert len(data)==158
#     # for i in data:
#         #print(i)
#
#     #print(data["list"])
#
#     #assert str(m) == "mid5"
#     #assert data[2]=="'messageId':'mid5'"
#     print(data)
#
# def test_delete_message_by_application_id_success():
#     response = app.test_client().delete(
#         'http://127.0.0.1:5000/deleteMessage?messageId=mid2'  # .format(self.baseUrl),
#     )
#     data = response.get_data()
#     assert response.status_code == 200
#     print(data)

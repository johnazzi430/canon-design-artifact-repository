import json
from unittest import mock
from unittest.mock import MagicMock, patch

import server.modules
import server.modules.models

class TestUser():
    username = 'Admin@utc.com'
    user_id = 5
    role = 'admin'

    def filter(self):
        return self

    def first(self):
        return self



def test_index(app, client):
    res = client.get("/")
    assert res.status_code == 200
    expected = "<!DOCTYPE html>"
    assert expected in res.get_data(as_text=True)


# @patch('flask_sqlalchemy._QueryProperty.__get__')
# def test_login(app, client, query):
#     data = {"username": "Admin@utc.com", "password": "Mypass01"}
#     headers = {"Content-Type": "application/json",}
#
#     mocker.return_value.filter.return_value.first = {}
#
#     response = client.post("/api/login", data=json.dumps(data), headers=headers)
#     assert response.status_code == 200
#     expected = {
#         "token": "",
#         "user": {"username": "Admin@utc.com", "user_id": 5, "role": "admin",},
#     }
#     assert json.loads(response.data)["token"] != None
#     assert json.loads(response.data)["user"] == expected["user"]
#

def test_user_not_in_session(app, client):
    response = client.get("/api/users?session=True")
    assert response.status_code == 200


def test_logout(app, client):
    response = client.post("/api/logout")
    assert response.status_code == 200

import requests


def test_setup_webserver():
    try:
        res = requests.get("http://localhost:8000/")
    except:
        raise ConnectionError()

    assert res.status_code == 200

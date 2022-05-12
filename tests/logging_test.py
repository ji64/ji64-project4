"""The tests the logging"""

import os


def test_log_files_exists():
    assert os.path.exists(
        os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../logs/errors.log"))) == True
    #assert os.path.exists(
    #    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../logs/flask.log"))) == True
    assert os.path.exists(
        os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../logs/myapp.log"))) == True
    assert os.path.exists(
        os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../logs/request.log"))) == True
    assert os.path.exists(
        os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../logs/sqlalchemy.log"))) == True
    assert os.path.exists(
        os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../logs/werkzeug.log"))) == True

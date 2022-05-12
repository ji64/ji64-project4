"""This makes the test configuration setup"""
# pylint: disable=redefined-outer-name
import logging
import os

import pytest
from flask import Flask

import app.run
from app import create_app, User
from app.db import db

#this is a good tutorial I used to fix this code to do datbase testing.
#https://xvrdm.github.io/2017/07/03/testing-flask-sqlalchemy-database-with-pytest/

@pytest.fixture()
def application():
    """This makes the app"""
    #you need this one if you want to see whats in the database
    #os.environ['FLASK_ENV'] = 'development'
    #you need to run it in testing to pass on github
    os.environ['FLASK_ENV'] = 'testing'

    os.environ['SECRET_KEY'] = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
    os.environ['MAIL_USERNAME'] = 'fajsdfsdsd'

    application = create_app()

    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        #drops the database tables after the test runs
        #db.drop_all()

@pytest.fixture()
def add_user(application):
    user = ''
    with application.app_context():
        #new record
        user = User('test@test.com', 'testtest', True)
        db.session.add(user)
        db.session.commit()
    #return user




@pytest.fixture()
def client(application):
    """This makes the http client"""
    return application.test_client()


@pytest.fixture()
def runner(application):
    """This makes the task runner"""
    return application.test_cli_runner()

@pytest.fixture()
def test_client(application):
    flask_app = app.run.app
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()

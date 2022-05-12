import logging
import os

from app import db
from app.db.models import User, Song
from faker import Faker

def test_adding_user(application):
    log = logging.getLogger("myApp")
    with application.app_context():
        assert db.session.query(User).count() == 0
        assert db.session.query(Song).count() == 0
        #showing how to add a record
        #create a record
        user = User('keith@webizly.com', 'testtest', False)
        #add it to get ready to be committed
        db.session.add(user)
        #call the commit
        #db.session.commit()
        #assert that we now have a new user
        #assert db.session.query(User).count() == 1
        #finding one user record by email
        user = User.query.filter_by(email='keith@webizly.com').first()
        log.info(user)
        #asserting that the user retrieved is correct
        assert user.email == 'keith@webizly.com'
        #this is how you get a related record ready for insert
        user.songs= [Song("test","smap", "test", 2016),Song("test2","te", "test",2020)]
        #commit is what saves the songs
        db.session.commit()
        assert db.session.query(Song).count() == 2
        song1 = Song.query.filter_by(title='test').first()
        assert song1.title == "test"
        #changing the title of the song
        song1.title = "SuperSongTitle"
        #saving the new title of the song
        db.session.commit()
        song2 = Song.query.filter_by(title='SuperSongTitle').first()
        assert song2.title == "SuperSongTitle"
        #checking cascade delete
        db.session.delete(user)
        assert db.session.query(User).count() == 0
        assert db.session.query(Song).count() == 0

def test_register(application):
    application.app_context()

    #print(os.getenv('MAIL_USERNAME'))
    #print(os.getenv('MAIL_PASSWORD'))
    #application.secret_key="this is a testing secret key"
    #application.config['WTF_CSRF_ENABLED'] = False
    with application.app_context():
        print(application.config["MAIL_USERNAME"])
        print(application.config["MAIL_PASSWORD"])
        #response = test_client.post('/register', data=dict(email="test@test.com", password="testtest", confirm="testtest"),
                                  #  follow_redirects=True)
        #assert response.status_code == 200

def test_login(test_client, application):
    application.app_context()
    #application.secret_key = "this is a testing secret key"
    #application.config['WTF_CSRF_ENABLED'] = False
    response = test_client.post('/login', data=dict(email="test@test.com", password="testtest"),
                                follow_redirects=True)
    assert response.status_code == 200
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200

def test_logged_in_dashboard(test_client, application):
    response = test_client.post('/login', data=dict(email="test@test.com", password="testtest"),
                                follow_redirects=True)
    assert response.status_code == 200
    response = test_client.get('/dashboard')
    assert response.status_code == 200
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200

def test_logged_out_dashboard(test_client, application):
    application.app_context()
    application.secret_key = "this is a testing secret key"
    #application.config['WTF_CSRF_ENABLED'] = False
    response = test_client.get('/dashboard')
    assert response.status_code == 302

def test_upload_song_csv(test_client, application):
    application.app_context()
    application.secret_key = "this is a testing secret key"
    application.config['WTF_CSRF_ENABLED'] = False
    response = test_client.post('/login', data=dict(email="test@test.com", password="testtest"),
                                follow_redirects=True)
    assert response.status_code == 200

    songs = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "music.csv"))
    csv_data = open(songs, "rb")
    data = {"file": (csv_data, "music.csv")}
    response = test_client.post('/songs/upload', data=data, follow_redirects=True, buffered=True,
                                content_type='multipart/form-data')
    assert response.status_code == 200
    response = test_client.get("/songs")
    assert response.status_code == 200

    assert os.path.exists(
        os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads', 'music.csv'))) == True
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200


def test_upload_location_csv(test_client, application):
    application.app_context()
    application.secret_key = "this is a testing secret key"
    application.config['WTF_CSRF_ENABLED'] = False
    response = test_client.post('/login', data=dict(email="test@test.com", password="testtest"),
                                follow_redirects=True)
    assert response.status_code == 200

    songs = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "us_cities_short.csv"))
    csv_data = open(songs, "rb")
    data = {"file": (csv_data, "us_cities_short.csv")}
    response = test_client.post('/locations/upload', data=data, follow_redirects=True, buffered=True,
                                content_type='multipart/form-data')
    assert response.status_code == 200
    response = test_client.get("/locations/map")
    assert response.status_code == 200

    assert os.path.exists(
        os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads', 'us_cities_short.csv'))) == True
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200





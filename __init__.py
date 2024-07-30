import os
from dotenv import load_dotenv
from flask import Flask
from rcon.source import Client

load_dotenv()

RCON_PASS=os.getenv('RCON_PASS')
SERVER_IP=os.getenv('SERVER_IP')

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/boom')
    def boom():
        print('>> REQUEST RECIEVED')
        with Client(SERVER_IP, 8101, passwd=RCON_PASS) as client:
            print(">> RCON CONNECTED")
            client.run("kill @a")
        return 'Allahu akbar'

    return app
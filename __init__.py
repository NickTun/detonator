import os, math, time, random
from dotenv import load_dotenv
from flask import Flask, request
from rcon.source import Client

load_dotenv()

RCON_PASS=os.getenv('RCON_PASS')
SERVER_IP=os.getenv('SERVER_IP')
SERVER_PORT=os.getenv('SERVER_PORT')

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
        with Client(SERVER_IP, int(SERVER_PORT), passwd=RCON_PASS) as client:
            print(">> RCON CONNECTED")
            client.run("execute as @e at @s run summon tnt")
        return 'Allahu akbar'
    
    @app.route('/<player_name>/shoot')
    def shoot(player_name):
        print('>> REQUEST RECIEVED')
        with Client(SERVER_IP, int(SERVER_PORT), passwd=RCON_PASS) as client:
            print(">> RCON CONNECTED")

            client.run('summon marker 0 0 0 {Tags:["position"]}')
            client.run('data modify entity @e[tag=position,limit=1] Rotation set from entity '+player_name+' Rotation')
            client.run('execute as @e[tag=position,limit=1] at @s run summon marker ^ ^ ^9 {Tags:["direction"]}')

            client.run('execute as '+player_name+' at @s run summon arrow ^ ^ ^1 {fuse:5,Tags:["projectile"]}')

            client.run('data modify entity @e[tag=projectile,limit=1] Motion set from entity @e[tag=direction,limit=1] Pos')

            time.sleep(0.5)
            for i in range(20):
                client.run('execute as @e[tag=projectile, limit=1] at @s run summon tnt ~'+str(random.randint(-2,2))+' ~'+str(random.randint(-2,2))+' ~'+str(random.randint(-2,2))+' {fuse:'+str(i)+'}')
                client.run('execute as @e[tag=projectile, limit=1] at @s run summon lightning_bolt ~'+str(random.randint(-5,5))+' ~'+str(random.randint(-5,5))+' ~'+str(random.randint(-5,5)))
                client.run('execute as @e[tag=projectile, limit=1] at @s run summon falling_block ~'+str(random.randint(-2,2))+' ~'+str(random.randint(-2,2))+' ~'+str(random.randint(-2,2))+' {BlockState:{Name:"minecraft:fire"},Time:1}')
            client.run('kill @e[tag=projectile]')
            client.run('kill @e[tag=position]')
            client.run('kill @e[tag=direction]')
        return 'Allahu akbar'

    return app
import os, math, time, random
from dotenv import load_dotenv
from flask import Flask, request
from rcon.source import Client
import json

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
        print('>> REQUEST RECIEVED: BOOM')
        with Client(SERVER_IP, int(SERVER_PORT), passwd=RCON_PASS) as client:
            print(">> RCON CONNECTED")
            client.run("execute as @e at @s run summon tnt")
        return 'Allahu akbar'
    
    @app.route('/<player_name>/shoot')
    def shoot(player_name):
        print('>> REQUEST RECIEVED: SHOOT')
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
    
    @app.route('/<player_name>/napalm')
    def napalm(player_name):
        print('>> REQUEST RECIEVED: NAPALM')
        with Client(SERVER_IP, int(SERVER_PORT), passwd=RCON_PASS) as client:
            print(">> RCON CONNECTED")
            client.run('execute as '+player_name+' at @s run summon marker ^ ^ ^ {Tags:["napalm_position"]}')
            client.run('data modify entity @e[tag=napalm_position,limit=1] Rotation set from entity '+player_name+' Rotation')
            for i in range(50):
                for a in range(i):
                    client.run('execute as @e[tag=napalm_position,limit=1] at @s run summon falling_block ^'+str(a-i//2)+' ^40 ^'+str(i-25)+' {BlockState:{Name:"minecraft:fire"},Time:1,}')
                time.sleep(0.02)
            client.run('kill @e[tag=napalm_position]')
        return 'Allahu akbar'
    
    @app.route('/<player_name>/lightning')
    def lightning(player_name):
        print('>> REQUEST RECIEVED: Lightning')
        with Client(SERVER_IP, int(SERVER_PORT), passwd=RCON_PASS) as client:
            print(">> RCON CONNECTED")
            client.run('execute as '+player_name+' at @s run summon marker ^ ^ ^ {Tags:["lightning_position"]}')
            client.run('data modify entity @e[tag=lightning_position,limit=1] Rotation set from entity '+player_name+' Rotation')
            for i in range(50):
                for a in range(i):
                    print(client.run('execute as @e[tag=lightning_position,limit=1] at @s run summon lightning_bolt ^'+str(a-i//2)+' ^ ^'+str(i+1)))
                time.sleep(0.02)
            client.run('kill @e[tag=lightning_position]')
        return 'Allahu akbar'

    @app.route('/<player_name>/build')
    def build(player_name):
        print('>> REQUEST RECIEVED: BUILD')
        with Client(SERVER_IP, int(SERVER_PORT), passwd=RCON_PASS) as client:
            print(">> RCON CONNECTED")
            with open('data.json') as arr:
                x = 0
                for line in arr:
                    convertedLine = json.loads(line)
                    for z in range(len(convertedLine)):
                        yAbs = float(convertedLine[z])
                        for y in range(int(yAbs) + 5):
                            client.run("execute as "+player_name+" at @s run setblock ~" + str(x + 1) + " ~" + str(y) + " ~" + str(z + 1) + " minecraft:grass_block")
                    print('>>> LINE BUILT')
                    x += 1
            print(">>> FINISHED")
        return 'Allahu ahahah'

    return app
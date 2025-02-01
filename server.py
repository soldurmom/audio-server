from flask import Flask, abort, jsonify, request
from database import models
from config import config
from api import telegram
import time

app = Flask('hello')
app.secret_key = config.APP_KEY

def token(func):
    def decorator(*args, **kwargs):
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            if config.BOT_TOKEN == token:
                return func(*args, **kwargs)
        return abort(401)
    return decorator

@app.route("/music/<id>", endpoint="getMusic", methods=['GET'])
@token
def getMusic(id):
    music = models.MusicModel.getMusicByUserId(id)
    result = []
    for item in music:
        result.append({
            'id' :          item[0],
            'performer' :   item[1],
            'title' :       item[2],
            'file_path' :   item[3],
            'duration' :    item[4],
        })
    return jsonify(result)

@app.route("/music/<id>", endpoint="removeMusic", methods=['DELETE'])
@token
def removeMusic(id):
    models.MusicModel.deleteMusicById(id)
    return jsonify({
            'status_code' : 200,
            'success' :     True
        })

@app.route("/getToken/<remote_key>/<user_id>")
def getToken(remote_key, user_id):
    user_auth = models.UsersAuthModel.getUserAuthByUserId(user_id)
    if user_auth and user_auth.remote_key == remote_key:
        return jsonify(config.BOT_TOKEN)
    return abort(401)

@app.route("/authUser/<remote_key>/<username>")
def authUser(remote_key, username):
    user = models.UserModel.getUserByUsername(username)
    if user and user.username == username:
        if confirmUser(user, remote_key):
            return user.get()
    return abort(404)

@app.route("/logout/<remote_key>/<user_id>")
def logout(remote_key, user_id):
    user_auth = models.UsersAuthModel.getUserAuthByUserId(user_id)
    if user_auth and user_auth.remote_key == remote_key:
        user_auth.updateUserAuth('confirmed', 0)
        return jsonify({
                'status_code' : 200,
                'success' :     True
            })
    return abort(401)

def confirmUser(user: models.UserModel, remote_key: str) -> bool:
    if models.UsersAuthModel.getUserAuthByUserId(user.id, 0) == None:
        models.UsersAuthModel(user.id, remote_key).createUserAuth()
    message = telegram.send_message(user.id, '/confirm your authorization or ignore this message')
    for second in range(10):
        if models.UsersAuthModel.getUserAuthByUserId(user.id):
            return True
        time.sleep(5)
    models.UsersAuthModel.deleteUserAuthByAddress(remote_key)
    telegram.edit_message(user.id, message.message_id, 'authorization timed out! try again...')
    return False

app.run('192.168.43.230')
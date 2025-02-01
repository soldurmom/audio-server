import database.db as db
from datetime import datetime, timedelta
import time

class Model:

    def get(self):
        return self.__dict__


class UserModel(Model):

    table_name = 'users'

    def __init__(self, id, username):
        self.id = id
        self.username = username
        self._created_at = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    @property
    def created_at(self):
        return datetime.strptime(self._created_at, "%m/%d/%Y %H:%M:%S")
    
    @created_at.setter
    def created_at(self, value):
        self._created_at = value
        
    def createUser(self):
        db.insert(self.table_name,['id', 'username', 'created_at'],[self.id, self.username, self._created_at])

    def updateUser(self, column, value):
        db.update(self.table_name,{'column': column, 'value': value},{'column': 'id', 'value': self.id})

    @staticmethod
    def getUserById(id):
        result = db.select(UserModel.table_name, ['id'], [id])
        if len(result):
            result = result[0]
            return UserModel(result[0], result[1])
        return None

    @staticmethod
    def getUserByUsername(username):
        result = db.select(UserModel.table_name, ['username'], [username])
        if len(result):
            result = result[0]
            return UserModel(result[0], result[1])
        return None
    
    @staticmethod
    def getAllUsers():
        return db.select(UserModel.table_name)
    

class UsersAuthModel(Model):

    table_name = 'users_auth'

    def __init__(self, user_id, remote_key, confirmed = 0):
        self.user_id = user_id
        self.remote_key = remote_key
        self.confirmed = confirmed
        self._last_visit = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    @property
    def last_visit(self):
        return datetime.strptime(self._last_visit, "%m/%d/%Y %H:%M:%S")
    
    @last_visit.setter
    def last_visit(self, value):
        self._last_visit = value

    def createUserAuth(self):
        db.insert(self.table_name, ['user_id', 'remote_key', 'confirmed', 'last_visit'], [self.user_id, self.remote_key, self.confirmed, self._last_visit])

    def updateUserAuth(self, column, value):
        db.update(self.table_name, {'column': column, 'value': value}, {'column': 'remote_key', 'value': self.remote_key})

    @staticmethod
    def getUserAuthByUserId(user_id, confirmed = 1):
        result =  db.select(UsersAuthModel.table_name, ['user_id', 'confirmed'], [user_id, confirmed])
        if len(result):
            result = result[0]
            return UsersAuthModel(result[0], result[1], result[2])
        return None
    
    @staticmethod
    def deleteUserAuthByAddress(remote_key):
        db.delete(UsersAuthModel.table_name, 'remote_key', remote_key)


class MusicModel(Model):

    table_name = 'music'

    def __init__(self, id, performer, title, file_path, music_duration):
        self.id = id
        self.performer = performer
        self.title = title
        self.file_path = file_path
        self.music_duration = music_duration

    def createMusic(self):
        db.insert(
            self.table_name,
            ['id', 'performer', 'title', 'file_path', 'duration'],
            [self.id, self.performer, self.title, self.file_path, self.music_duration]
        )

    @staticmethod
    def getMusicByUserId(user_id):
        return db.selectMusicByUserId(user_id)

    @staticmethod
    def getMusicById(id): 
        result =  db.select(MusicModel.table_name, ['id'], [id])
        if len(result):
            result = result[0]
            return MusicModel(
                result[0],
                result[1],
                result[2],
                result[3],
                result[4],
            )
        return None
    
    @staticmethod
    def deleteMusicById(id):
        db.delete(MusicModel.table_name, 'id', id)
    

class UsersMusicModel(Model):

    table_name = 'users_music'

    def __init__(self, user_id, music_id):
        self.user_id = user_id
        self.music_id = music_id
        self._created_at = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    @property
    def created_at(self):
        return datetime.strptime(self._created_at, "%m/%d/%Y %H:%M:%S")
    
    @created_at.setter
    def created_at(self, value):
        self._created_at = value

    def createUsersMusic(self):
        db.insert(self.table_name, ['user_id', 'music_id', 'created_at'], [self.user_id, self.music_id, self._created_at])

    @staticmethod
    def getUsersMusicByBothId(user_id, music_id):
        result = db.select(UsersMusicModel.table_name, ['user_id', 'music_id'], [user_id, music_id])
        if len(result):
            return result
        return None

    @staticmethod
    def getAllUsersMusicByUserId(user_id):
        result = db.select(UsersMusicModel.table_name, ['user_id'], [user_id])
        if len(result):
            return result
        return None
    
    @staticmethod
    def checkIsExpiredByUser(user_id):
        users_music = UsersMusicModel.getAllUsersMusicByUserId(user_id)
        sorted_music = sorted(users_music, key=lambda item: datetime.strptime(item[2], "%m/%d/%Y %H:%M:%S"), reverse=True)
        time_delta = datetime.strptime(sorted_music[0][2], "%m/%d/%Y %H:%M:%S") + timedelta(seconds=60)
        return True if datetime.now() > time_delta else False
    
    @staticmethod
    def deleteAllExpiredByUser(user_id):
        users_music = UsersMusicModel.getAllUsersMusicByUserId(user_id)
        for music in users_music:
            MusicModel.deleteMusicById(music[1])

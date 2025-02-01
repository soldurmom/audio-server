import telebot
from api import telegram
import database.models as models
import config.config as config

bot = telebot.TeleBot(config.BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_handler(message):
    createUser(message.from_user.id, message.from_user.username)
    telegram.send_message(message.chat.id, 'hello!')

@bot.message_handler(commands=['confirm'])
def confirm_handler(message):
    confirmUser(message.chat.id)
    telegram.send_message(message.chat.id, 'confirmed successfully!')

@bot.message_handler(content_types=['audio'])
def message_handler(message):
    saveFile(message)
    telegram.send_message(message.chat.id, 'music saved!')

def createUser(id: int, username: str) -> None:
    if models.UserModel.getUserById(id) == None:
        models.UserModel(id, username).createUser()

def confirmUser(user_id) -> None:
    user_auth = models.UsersAuthModel.getUserAuthByUserId(user_id, 0)
    if user_auth:
        user_auth.updateUserAuth('confirmed', 1)

def saveFile(message) -> None:
    if models.MusicModel.getMusicById(message.audio.file_unique_id) == None:
        file_info = bot.get_file(message.audio.file_id)
        models.MusicModel(
            id =             message.audio.file_unique_id,
            performer =      message.audio.performer,
            title =          message.audio.title,
            file_path =      file_info.file_path,
            music_duration = message.audio.duration
        ).createMusic()
        models.UsersMusicModel(
            message.chat.id,
            message.audio.file_unique_id
        ).createUsersMusic()
    elif models.UsersMusicModel.getUsersMusicByBothId(message.chat.id, message.audio.file_unique_id) == None:
        models.UsersMusicModel(
            message.chat.id,
            message.audio.file_unique_id
        ).createUsersMusic()

bot.infinity_polling(timeout=10, long_polling_timeout = 5)

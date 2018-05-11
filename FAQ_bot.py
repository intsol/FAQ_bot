#
# FAQ_Bot
# Handles hashtags and prints sends useful info to the channel
# This Telegram bot reads an FAQ sheet from Google Drive and loads it into an internal disctionary
#
#
# Setup:
#   - The Google auth file "client_secret.json" must exist in the same directory as the script
#   - Add the bot to the group & make an admin


from telegram.ext import Updater, Handler, CommandHandler, MessageHandler, InlineQueryHandler, Filters

BotKey   = 'Insert bot Father Key Here'
FaqSheet = 'insert Google Sheet Name Here'

Faq = {}  # tuple for storing the FAQ, indexed by hash tag

# Google Docs Imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Load the google sheet into the Dictionary "Faq"
def Load_faq():
    global Faq

    Faq.clear()
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open(FaqSheet).sheet1

    # Extract and print all of the values
    keys   = sheet.col_values(1)
    values = sheet.col_values(2)


    # read the sheet ros in to the Dictionary (associative array)
    for key, value in zip(keys, values) :
        Faq[key] = value    # the '#' is left on the key - hashtag entities returned have #


# Read Admin IDs from the channel
def loadAdminIDs(bot, update):
    _adminIDs = []
    longAdmins = bot.get_chat_administrators(update.message.chat.id)
    for admin in longAdmins:
        _adminIDs.append(admin.user.id)
    return _adminIDs

#Python Telegram Callbacks
def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def start(bot, update):
    update.message.reply_text(
        'Starting {}'.format(update.message.from_user.first_name))


# Callback handler for general messages
# - Handle the #hastags here
def message_handler(bot, update):

    entities = update.message.parse_entities()
    for entity in entities:
        if entity.type == 'hashtag':
            hashtag = update.message.parse_entity(entity)
            if hashtag == '#update':
                Load_faq()
            else:
                bot.send_message(chat_id=update.message.chat_id, text=Faq[hashtag.lower()])



Load_faq()      # read the FAQ from sheet
#
# The following is Telegram Python Bot startup code - Go to Bot Father to register Bot Key
#
updater = Updater(BotKey)

dp = updater.dispatcher

dp.add_handler(CommandHandler('hello', hello))
dp.add_handler(CommandHandler('start', start))
dp.add_handler(MessageHandler(Filters.all, message_handler))    # all other messages

updater.start_polling()
updater.idle()

# FAQ_bot
A Simple Python Telegram Bot for using #tags to send description text to channel, using Google Drive for Storage

Library Requirements:
  - Telegram Python Bot
  - Google gspread, oauth

Telegram Setup
  - register a new bot using BotFather
  - Insert the generated Bot Key into the script at BOTKey = " "
  - Add the bot to the required group and promote to Admin
  
Google Docs OAuth Setup (Instructions From Google):
  http://gspread.readthedocs.io/en/latest/oauth2.html
  You must activate both the Drive and Sheets APIs in the Google Developers Console
  The downloaded .json file must be renamed to client_secret.json and stored in the script folder

from pytube import YouTube as yt
from googlesearch import search 

import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Olá {user.mention_markdown_v2()}\, eu sou o AbdonBot\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Ajuda!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def reverse_echo(update: Update, context: CallbackContext) -> None:
    """Reversed Echo user message."""
    update.message.reply_text(update.message.text[::-1])
    
def youtube(update: Update, context: CallbackContext) -> None:
    """Search for a video on Google and send it."""
    user_message = update.message.text
    for s in search(user_message, tld="com", num=10, stop=5, pause=2):
        print(s)
        video = yt(s)
        update.message.reply_text(s)
        video_info = {
            "title": video.title,
            "author": video.author,
            "channel_url": video.channel_url,
            "description": video.description,
            "length": video.length,
            "views": video.views,
            "rating": video.rating,
        }
        """update.message.reply(video.title, 
                                  video.author, 
                                  video.channel_url,
                                  video.description, 
                                  video.length, 
                                  video.views, 
                                  video.rating)"""
    

def main() -> None:
    """Start the bot."""
    
    file = open("token.txt")
    token = file.read()
    file.close()
    
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    
    # on non command i.e message - echo the message on Telegram
    #dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reverse_echo))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, youtube))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
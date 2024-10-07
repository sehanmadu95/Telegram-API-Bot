from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler,filters,ContextTypes

BOT_TOKEN = '7620151410:AAHSaGheLQ8R_Ir4KlHWzbqQ7P8OVKtlhO8'


#Define the start command handler function

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE)-> None :
    await update.message.reply_text("Hi Welcome to SEHAN MADUSHANKA BOT....., SAY SOMETHING I 'll REPEAT...")


#Defin the echo message handler function
async def echo(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    await update.message.reply_text(update.message.text)

def main()->None:
    app=ApplicationBuilder().token("7620151410:AAHSaGheLQ8R_Ir4KlHWzbqQ7P8OVKtlhO8").build()

    app.add_handler(CommandHandler("start",start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,echo))


    app.run_polling()

if __name__== '__main__':
   main()
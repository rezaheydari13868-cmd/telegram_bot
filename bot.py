from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋 بات با موفقیت روشن شد")

def main():
    TOKEN = "8515539607:AAFpCF9ORREAUtCAKfPBVNIJdVKA1toicZQ"

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# توکن بات شما
TOKEN = "8515539607:AAFpCF9ORREAUtCAKfPBVNIJdVKA1toicZQ"

# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["💎 خرید اشتراک و WEST"],
        ["📚 ثبت‌نام آزمون کلاس ", "🚀 محصولات پنجم تا نهم"],
        ["💸 کسب درآمد "],
        ["👤 پشتیبانی", "✉️ ارسال پیام ناشناس"],
        ["📄 نتایج رتبه های برتر کنکور"],
        ["📌 درباره نمایندگی ما در تهران"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    text = (
        "😍 سلام! به ربات دانش اموزی وست خوش اومدی\n\n"
        "هدف من کمک رسوندن به توعه،\n"
        "چیکار می‌تونم برات انجام بدم عزیزم؟"
    )

    await update.message.reply_text(text, reply_markup=reply_markup)


# ---------- پیام‌ها ----------
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    if msg == "💎 خرید اشتراک WEST":
        await update.message.reply_text(
            "💎 اشتراک الماس WEST\n\n"
            "✔️ دسترسی کامل به آموزش‌ها\n"
            "✔️ پشتیبانی ویژه\n\n"
            "📞 برای خرید با پشتیبانی در تماس باش"
        )

    elif msg == "📚 ثبت‌نام آزمون کلاس ما  ":
        await update.message.reply_text(
            "📚 ثبت‌نام آزمون‌های وست\n\n"
            "لطفاً پایه تحصیلی خودت رو ارسال کن."
        )

    elif msg == "🚀 محصولات پنجم تا نهم":
        await update.message.reply_text(
            "🚀 محصولات آموزشی وست \n\n"
            "پایه پنجم تا نهم\n"
            "جزوه، آزمون، کلاس آنلاین"
        )

    elif msg == "💸 کسب درآمد ":
        await update.message.reply_text(
            "💸 همکاری در فروش و کسب درآمد\n\n"
            "برای اطلاعات بیشتر با پشتیبانی تماس بگیر."
        )

    elif msg == "👤 پشتیبانی":
        await update.message.reply_text(
            "👤 پشتیبانی WEST تهران\n\n"
            "🆔 @SupportID"
        )

    elif msg == "✉️ ارسال پیام ناشناس":
        await update.message.reply_text(
            "✉️ پیام خودت رو ارسال کن\n"
            "پیام به صورت ناشناس به ادمین ارسال میشه."
        )
        context.user_data["anon"] = True

    elif msg == "📄نتایج رتبه های برتر کنکور ":
        await update.message.reply_text(
            "📄 نتایج رتبه های برتر کنکور۴\n\n"
            "به‌زودی داخل کانال قرار می‌گیره."
        )

    elif msg == "📌 درباره نمایندگی ما تهران":
        await update.message.reply_text(
            "📌 نمایندگی رسمی ما تهران\n\n"
            "📍 آموزش تخصصی\n"
            "📍 آزمون‌های استاندارد\n"
            "📍 پشتیبانی قوی"
        )

    else:
        # پیام ناشناس
        if context.user_data.get("anon"):
            # اینجا می‌تونی به ادمین فوروارد کنی
            await update.message.reply_text("✅ پیام شما ارسال شد.")
            context.user_data["anon"] = False
        else:
            await update.message.reply_text("❓ لطفاً از منو یکی از گزینه‌ها رو انتخاب کن.")


# ---------- main ----------
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

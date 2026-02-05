from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, CallbackQueryHandler, filters

# ---------------- تنظیمات اصلی ----------------
TOKEN = "8515539607:AAFpCF9ORREAUtCAKfPBVNIJdVKA1toicZQ"
ADMIN_ID = 7312005758  # ← آیدی عددی شما
CHANNEL_USERNAME = "@westcartel1"  # ← کانالی که حتماً عضو باشن
SUPPORT_USERNAME = "@Eiejduxj"  # ← آیدی پشتیبانی

# ---------- ذخیره کاربران ----------
def save_user(user_id):
    with open("users.txt", "a+") as f:
        f.seek(0)
        users = f.read().splitlines()
        if str(user_id) not in users:
            f.write(str(user_id) + "\n")

# ---------- بررسی عضویت در کانال ----------
async def is_member(bot, user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if not await is_member(context.bot, user.id):
        await update.message.reply_text(
            "❌ برای استفاده از ربات باید عضو کانال ما باشی\n\n"
            f"🔗 {CHANNEL_USERNAME}\n\n"
            "بعد از عضویت دوباره /start رو بزن"
        )
        return

    save_user(user.id)

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            "🚀 کاربر جدید ربات رو استارت کرد\n\n"
            f"👤 نام: {user.full_name}\n"
            f"🆔 ID: {user.id}\n"
            f"🔗 Username: @{user.username}"
        )
    )

    keyboard = [
        ["💎 خرید اشتراک الماس West"],
        ["📚 ثبت‌نام آزمون کلاس West", "🚀 محصولات پنجم تا نهم"],
        ["💸 کسب درآمد از West"],
        ["👤 پشتیبانی", "✉️ ارسال پیام ناشناس"],
        ["📄 مصاحبه رتبه‌های برتر ۴۰۴"],
        ["📌 درباره نمایندگی West"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "😍 سلام! به ربات West خوش اومدی\n\n"
        "از منوی زیر انتخاب کن 👇",
        reply_markup=reply_markup
    )

# ---------- پیام‌ها ----------
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    if msg == "💎 خرید اشتراک الماس West":
        await update.message.reply_text("💎 برای خرید اشتراک با پشتیبانی تماس بگیر")

    elif msg == "👤 پشتیبانی":
        await update.message.reply_text(f"🆔 {SUPPORT_USERNAME}")

    elif msg == "پنل ادمین" and update.effective_user.id == ADMIN_ID:
        await send_admin_panel(update, context)

    else:
        await update.message.reply_text("❓ لطفاً از منو انتخاب کن")

# ---------- پنل حرفه‌ای ادمین ----------
async def send_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👥 مشاهده کاربران", callback_data="view_users")],
        [InlineKeyboardButton("📊 آمار کاربران", callback_data="stats_users")],
        [InlineKeyboardButton("📩 پیام همگانی", callback_data="broadcast_users")],
        [InlineKeyboardButton("✉️ پیام به کاربر خاص", callback_data="message_user")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎛 پنل ادمین:", reply_markup=reply_markup)

# ---------- پاسخ دکمه‌های پنل ----------
async def admin_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        await query.edit_message_text("❌ شما اجازه دسترسی ندارید")
        return

    if query.data == "view_users":
        await users_list(update, context)
    elif query.data == "stats_users":
        await stats(update, context)
    elif query.data == "broadcast_users":
        await query.edit_message_text("📩 برای ارسال پیام همگانی از دستور زیر استفاده کنید:\n/broadcast متن پیام")
    elif query.data == "message_user":
        await query.edit_message_text("✉️ برای ارسال پیام به کاربر خاص از دستور زیر استفاده کنید:\n/message user_id متن پیام")

# ---------- پیام همگانی ----------
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("❗ متن پیام رو بنویس")
        return

    text = " ".join(context.args)

    with open("users.txt", "r") as f:
        users = f.read().splitlines()

    sent = 0
    for user_id in users:
        try:
            await context.bot.send_message(chat_id=int(user_id), text=text)
            sent += 1
        except:
            pass

    await update.message.reply_text(f"✅ پیام برای {sent} نفر ارسال شد")

# ---------- مشاهده لیست آیدی کاربران ----------
async def users_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("users.txt", "r") as f:
            users = f.read().splitlines()

        if not users:
            await update.message.reply_text("❌ هنوز کاربری ثبت نشده")
            return

        text = "👥 لیست کاربران ربات:\n\n"
        for uid in users:
            text += f"🆔 {uid}\n"

        await update.message.reply_text(text)

    except FileNotFoundError:
        await update.message.reply_text("❌ فایل کاربران وجود ندارد")

# ---------- آمار تعداد کاربران ----------
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("users.txt", "r") as f:
            users = f.read().splitlines()

        total = len(users)

        await update.message.reply_text(
            f"📊 آمار ربات:\n\n"
            f"👥 تعداد کل کاربران: {total}"
        )

    except FileNotFoundError:
        await update.message.reply_text("❌ هنوز کاربری ثبت نشده")

# ---------- ارسال پیام به کاربر خاص ----------
async def message_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("❗ دستور صحیح: /message user_id متن پیام")
        return

    user_id = int(context.args[0])
    text = " ".join(context.args[1:])

    try:
        await context.bot.send_message(chat_id=user_id, text=text)
        await update.message.reply_text("✅ پیام ارسال شد")
    except:
        await update.message.reply_text("❌ ارسال پیام موفق نبود")

# ---------- main ----------
def main():
    app = Application.builder().token(TOKEN).build()

    # دستورات اصلی
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("users", users_list))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("message", message_user))

    # دکمه‌های پنل ادمین
    app.add_handler(CallbackQueryHandler(admin_button))

    # پیام‌های متنی عادی
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

    app.run_polling()


if __name__ == "__main__":
    main()

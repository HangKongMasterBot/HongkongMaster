import os
from flask import Flask, request
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram.error import BadRequest

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@grandlakeofficial"
users_data = {}

if not TOKEN:
    print("❌ BOT_TOKEN পাওয়া যায়নি! Render এর Environment Variables এ সেট করো।")
    exit()

app = Flask(__name__)

def is_member(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    try:
        chat_member = context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return chat_member.status in ['member', 'creator', 'administrator']
    except BadRequest:
        return False

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not is_member(update, context):
        keyboard = [
            [InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.strip('@')}")],
            [InlineKeyboardButton("✅ Check", callback_data='check_join')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "Please join our channel first to play HangKong Master",
            reply_markup=reply_markup
        )
        return

    if user_id not in users_data:
        users_data[user_id] = {"coins": 0}

    keyboard = [[InlineKeyboardButton("💰 Tap to Earn", callback_data='tap')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Welcome to HangKong Master!\nCollect coins by tapping the button below.",
        reply_markup=reply_markup
    )

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()

    if query.data == 'tap':
        if user_id not in users_data:
            users_data[user_id] = {"coins": 0}
        users_data[user_id]['coins'] += 1
        keyboard = [[InlineKeyboardButton("💰 Tap to Earn", callback_data='tap')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text=f"💰 Coins: {users_data[user_id]['coins']}",
            reply_markup=reply_markup
        )
    elif query.data == 'check_join':
        if is_member(update=query, context=context):
            if user_id not in users_data:
                users_data[user_id] = {"coins": 0}
            keyboard = [[InlineKeyboardButton("💰 Tap to Earn", callback_data='tap')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="✅ Welcome to HangKong Master!\nCollect coins by tapping the button below.",
                reply_markup=reply_markup
            )
        else:
            query.answer(text="❌ You are not a member yet. Please join the channel.", show_alert=True)

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CallbackQueryHandler(button))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), updater.bot)
    updater.dispatcher.process_update(update)
    return "OK", 200

@app.route("/")
def home():
    return "Bot is Alive!", 200

if __name__ == "__main__":
    print("✅ Bot running with Flask (Webhook Mode)...")
    app.run(host="0.0.0.0", port=8080)

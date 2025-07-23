import os
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise Exception("❌ BOT_TOKEN পাওয়া যায়নি! সেট করো।")

CHANNEL_USERNAME = "@grandlakeofficial"

app = Flask(__name__)
telegram_app = Application.builder().token(BOT_TOKEN).build()

users_data = {}

async def is_member(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return chat_member.status in ['member', 'creator', 'administrator']
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await is_member(user_id, context):
        keyboard = [
            [InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.strip('@')}")],
            [InlineKeyboardButton("✅ Check", callback_data='check_join')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Please join our channel first to play HangKong Master", reply_markup=reply_markup)
        return

    if user_id not in users_data:
        users_data[user_id] = {"coins": 0}

    keyboard = [[InlineKeyboardButton("💰 Tap to Earn", callback_data='tap')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to HangKong Master!\nCollect coins by tapping the button below.", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == 'tap':
        if user_id not in users_data:
            users_data[user_id] = {"coins": 0}
        users_data[user_id]['coins'] += 1
        keyboard = [[InlineKeyboardButton("💰 Tap to Earn", callback_data='tap')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"💰 Coins: {users_data[user_id]['coins']}", reply_markup=reply_markup)

    elif query.data == 'check_join':
        if await is_member(user_id, context):
            if user_id not in users_data:
                users_data[user_id] = {"coins": 0}
            keyboard = [[InlineKeyboardButton("💰 Tap to Earn", callback_data='tap')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text="✅ Welcome to HangKong Master!\nCollect coins by tapping the button below.", reply_markup=reply_markup)
        else:
            await query.answer(text="❌ You are not a member yet. Please join the channel.", show_alert=True)

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(button))

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    asyncio.run(telegram_app.process_update(update))
    return "OK"

@app.route('/')
def home():
    return "✅ Bot is Alive!"

if __name__ == "__main__":
    telegram_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8080)),
        url_path=BOT_TOKEN,
        webhook_url=f"https://{os.getenv('REPLIT_URL')}/{BOT_TOKEN}"
    )

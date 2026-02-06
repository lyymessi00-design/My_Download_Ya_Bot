import telebot
from yt_dlp import YoutubeDL

# --- ضع بياناتك هنا ---
TOKEN = '7996053587:AAGScSrCOvS9KzHBGh5vkksWsem6uPPBj94'
CHANNEL_ID = '-1003758785234'
CHANNEL_URL = 'https://t.me/Apps_Zone26'
# ----------------------

bot = telebot.TeleBot(TOKEN)

def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except: return False

@bot.message_handler(func=lambda message: True)
def handle(message):
    if not is_subscribed(message.from_user.id):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("اشترك في القناة 📢", url=CHANNEL_URL))
        bot.send_message(message.chat.id, "يجب الاشتراك أولاً!", reply_markup=markup)
        return

    url = message.text
    if "http" in url:
        bot.reply_to(message, "⏳ جاري التحميل...")
        try:
            with YoutubeDL({'format': 'best', 'outtmpl': 'vid.mp4'}) as ydl:
                ydl.download([url])
            with open('vid.mp4', 'rb') as v:
                bot.send_video(message.chat.id, v)
        except: bot.reply_to(message, "خطأ في الرابط!")

bot.polling()

import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# التوكن يتم قراءته من إعدادات السيرفر للأمان
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 أرسل رابط يوتيوب وسأقطع لك أول 10 ثواني!")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.message.chat_id
    await update.message.reply_text("⏳ جاري المعالجة...")
    
    output = f"clip_{chat_id}.mp4"
    # تقنية أينشتاين: التحميل والتقطيع في خطوة واحدة
    cmd = f'yt-dlp -f "best[ext=mp4]" --download-sections "*00:00-00:10" -o "{output}" "{url}"'
    
    try:
        os.system(cmd)
        with open(output, 'rb') as v:
            await update.message.reply_video(video=v)
        os.remove(output)
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video))
    app.run_polling()

if __name__ == "__main__":
    main()

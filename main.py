import os
import time
from instagrapi import Client
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# الإعدادات من Variables في Railway
TOKEN = os.getenv("BOT_TOKEN")
INSTA_USER = os.getenv("INSTA_USER")
INSTA_PASS = os.getenv("INSTA_PASS")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 أرسل رابط يوتيوب وسأقوم بنشره تلقائياً كـ Reels على إنستغرام!")

async def process_and_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.message.chat_id
    status_msg = await update.message.reply_text("⏳ جاري سحب الفيديو من يوتيوب...")
    
    video_file = f"video_{chat_id}.mp4"
    
    try:
        # 1. تحميل أول 10-15 ثانية من يوتيوب
        download_cmd = f'yt-dlp -f "best" --download-sections "*00:00-00:15" --force-overwrites -o "{video_file}" "{url}"'
        os.system(download_cmd)
        
        if not os.path.exists(video_file):
            await status_msg.edit_text("❌ فشل تحميل الفيديو من يوتيوب.")
            return

        await status_msg.edit_text("🔐 جاري تسجيل الدخول إلى إنستغرام...")
        
        # 2. تسجيل الدخول والرفع على إنستغرام
        cl = Client()
        cl.login(INSTA_USER, INSTA_PASS)
        
        await status_msg.edit_text("📤 جاري رفع الفيديو كـ Reels...")
        caption = "فيديو رائع تم نشره تلقائياً بواسطة بوت أينشتاين 🤖🔥 #Python #Automation"
        
        # الرفع كـ Reel
        media = cl.clip_upload(video_file, caption)
        
        await status_msg.edit_text(f"✅ تم النشر بنجاح على حسابك! \nID: {media.pk}")
        
        # تنظيف الملفات
        if os.path.exists(video_file):
            os.remove(video_file)
            
    except Exception as e:
        await status_msg.edit_text(f"❌ حدث خطأ: {str(e)}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_and_post))
    app.run_polling()

if __name__ == "__main__":
    main()


import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from yt_dlp import YoutubeDL
from moviepy.editor import VideoFileClip, vfx

# التوكن الخاص بك
TOKEN = '8765504349:AAFGAMtkXuuqwJ_pX-Ex6NZ4wGJrSBSn9i8'

def process_video_logic(url):
    # إعدادات تحميل ذكية
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': 'input.mp4',
        'noplaylist': True
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # معالجة الفيديو باستخدام مكتبة MoviePy
    clip = VideoFileClip("input.mp4")
    
    # اختيار مقطع عشوائي (15 ثانية لضمان السرعة)
    start = random.uniform(0, max(0, clip.duration - 20))
    clip = clip.subclip(start, start + 15)
    
    # تحويل الأبعاد لـ TikTok (9:16)
    w, h = clip.size
    target_w = h * (9/16)
    final = clip.crop(x_center=w/2, width=target_w, height=h)
    
    # لمسات احترافية: سرعة خفيفة وزووم لتجنب حقوق النشر
    final = final.fx(vfx.speedx, 1.05).resize(1.1)
    
    output = "final_output.mp4"
    # الحفظ بإعدادات سريعة تناسب السحاب
    final.write_videofile(output, codec="libx264", audio_codec="aac", fps=24, preset="ultrafast")
    
    clip.close()
    return output

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "youtu" in url:
        await update.message.reply_text("🚀 جاري المعالجة في سحاب جوجل... انتظر قليلاً!")
        try:
            video_path = process_video_logic(url)
            await update.message.reply_video(video=open(video_path, 'rb'), caption="✅ الفيديو جاهز للنشر!")
            os.remove("input.mp4")
            os.remove(video_path)
        except Exception as e:
            await update.message.reply_text(f"❌ خطأ: {str(e)}")

if __name__ == '__main__':
    # تشغيل البوت
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_msg))
    print("✅ البوت يعمل الآن على Colab! أرسل رابط يوتيوب في تيليجرام.")
    app.run_polling()


import os
import json
import time
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from gradio_client import Client

# Load environment variables (for bot token and API keys)
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
JSON2VIDEO_API_KEY = os.getenv("JSON2VIDEO_API_KEY")
JSON2VIDEO_API_BASE_URL = "https://api.json2video.com/v2"
HUGGINGFACE_SPACE_ID = "liuyuyuil/Wanx2.1_Text_to_Video"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("مرحباً بك! أنا بوت لإنشاء الفيديوهات بالذكاء الاصطناعي. أرسل لي وصفاً للفيديو الذي تريده وسأقوم بإنشائه لك. يمكنك استخدام /json_video أو /hf_video.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("يمكنك إرسال وصف نصي لإنشاء فيديو. مثال: \"فيديو لقطة تلعب بكرة صوف في حديقة خضراء\".\nاستخدم /json_video لإنشاء فيديو باستخدام JSON2Video.\nاستخدم /hf_video لإنشاء فيديو باستخدام Hugging Face Wanx2.1.")

async def create_json2video_movie(prompt: str) -> str:
    headers = {
        "x-api-key": JSON2VIDEO_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "resolution": "full-hd",
        "scenes": [
            {
                "elements": [
                    {
                        "type": "text",
                        "text": prompt,
                        "font": "Arial",
                        "fontSize": 50,
                        "color": "#ffffff",
                        "x": "center",
                        "y": "center",
                        "width": "80%",
                        "height": "auto",
                        "background": "#000000"
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(f"{JSON2VIDEO_API_BASE_URL}/movies", headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors
        project_id = response.json()["project"]
        return project_id
    except requests.exceptions.RequestException as e:
        print(f"Error creating JSON2Video movie: {e}")
        return None

async def poll_json2video_status(project_id: str) -> str:
    headers = {
        "x-api-key": JSON2VIDEO_API_KEY
    }
    while True:
        try:
            response = requests.get(f"{JSON2VIDEO_API_BASE_URL}/movies/{project_id}", headers=headers)
            response.raise_for_status()
            status = response.json()["status"]
            if status == "finished":
                return response.json()["url"]
            elif status == "failed":
                return None
            time.sleep(10) # Poll every 10 seconds
        except requests.exceptions.RequestException as e:
            print(f"Error polling JSON2Video status: {e}")
            return None

async def generate_json_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt = " ".join(context.args) if context.args else update.message.text
    if not prompt:
        await update.message.reply_text("الرجاء تزويدي بوصف لإنشاء الفيديو.")
        return

    await update.message.reply_text(f"تلقيت طلبك: \"{prompt}\". جاري العمل على إنشاء الفيديو باستخدام JSON2Video، قد يستغرق هذا بعض الوقت...")
    
    project_id = await create_json2video_movie(prompt)
    if project_id:
        video_url = await poll_json2video_status(project_id)
        if video_url:
            await update.message.reply_video(video_url, caption="تم إنشاء الفيديو بنجاح بواسطة JSON2Video!")
        else:
            await update.message.reply_text("عذراً، حدث خطأ أثناء إنشاء الفيديو بواسطة JSON2Video.")
    else:
        await update.message.reply_text("عذراً، لم نتمكن من بدء عملية إنشاء الفيديو بواسطة JSON2Video.")

async def generate_hf_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt = " ".join(context.args) if context.args else update.message.text
    if not prompt:
        await update.message.reply_text("الرجاء تزويدي بوصف لإنشاء الفيديو.")
        return

    await update.message.reply_text(f"تلقيت طلبك: \"{prompt}\". جاري العمل على إنشاء الفيديو باستخدام Hugging Face Wanx2.1، قد يستغرق هذا بعض الوقت...")
    
    try:
        client = Client(HUGGINGFACE_SPACE_ID)
        result = client.predict(prompt, api_name="/video_generation")
        if result and os.path.exists(result):
            await update.message.reply_video(video=open(result, 'rb'), caption="تم إنشاء الفيديو بنجاح بواسطة Hugging Face Wanx2.1!")
            os.remove(result) # Clean up the downloaded video file
        else:
            await update.message.reply_text("عذراً، حدث خطأ أثناء إنشاء الفيديو بواسطة Hugging Face Wanx2.1.")
    except Exception as e:
        await update.message.reply_text(f"عذراً، حدث خطأ أثناء الاتصال بـ Hugging Face Space: {e}")

def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("json_video", generate_json_video))
    application.add_handler(CommandHandler("hf_video", generate_hf_video))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_json_video)) # Default to JSON2Video

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

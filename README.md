# بوت تيليجرام لإنشاء الفيديو بالذكاء الاصطناعي 🎬

هذا البوت يقوم بإنشاء فيديوهات من النصوص باستخدام أدوات ذكاء اصطناعي متعددة ومجانية.

## المميزات ✨
- **دمج أدوات متعددة**: يستخدم JSON2Video و Hugging Face (Wanx2.1).
- **سهل الاستخدام**: أوامر بسيطة لإنشاء الفيديوهات.
- **مجاني بالكامل**: يعتمد على خطط مجانية ونماذج مفتوحة المصدر.

## الأوامر المتاحة 🤖
- `/start`: بدء تشغيل البوت.
- `/help`: عرض المساعدة.
- `/json_video [وصف]`: إنشاء فيديو باستخدام JSON2Video.
- `/hf_video [وصف]`: إنشاء فيديو باستخدام Hugging Face (Wanx2.1).

## طريقة التشغيل 🚀

1. قم بتحميل المشروع وتثبيت المتطلبات:
   ```bash
   pip install -r requirements.txt
   ```

2. قم بتعديل ملف `.env` وإضافة الـ Tokens الخاصة بك:
   - `TELEGRAM_BOT_TOKEN`: توكن البوت من BotFather.
   - `JSON2VIDEO_API_KEY`: مفتاح API من [json2video.com](https://json2video.com).

3. قم بتشغيل البوت:
   ```bash
   python main.py
   ```

## الأدوات المستخدمة 🛠️
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [gradio_client](https://www.gradio.app/guides/getting-started-with-the-python-client)
- [JSON2Video API](https://json2video.com)
- [Hugging Face Spaces](https://huggingface.co/spaces)

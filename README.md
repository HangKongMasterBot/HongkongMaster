# HangKongMasterBot

## Setup

1. GitHub থেকে ক্লোন বা নিজের Replit/Render প্রজেক্টে ফাইলগুলো আপলোড করো।
2. Environment Variables সেট করো:
   - `BOT_TOKEN` = তোমার Telegram Bot Token
   - `REPLIT_URL` = তোমার Replit প্রজেক্ট URL (যেমন: yourprojectname.username.replit.app)
3. `requirements.txt` থেকে ডিপেন্ডেন্সি ইনস্টল করো:
   ```
   pip install -r requirements.txt
   ```
4. প্রজেক্ট রান করো:
   ```
   python bot.py
   ```
5. Telegram এ `/start` দিয়ে বট চেক করো।

---

## Deploy on Render/Railway

Render বা Railway তে Deploy করতে:

- Replit এর মতো ENV variables সেট করো (BOT_TOKEN, REPLIT_URL)  
- Build Command: `pip install -r requirements.txt`  
- Start Command: `python bot.py`  

---

Bot এখন webhook মোডে কাজ করবে এবং 24/7 চলবে।

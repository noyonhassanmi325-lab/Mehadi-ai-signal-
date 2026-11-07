# Mehedi AI Chart Lab

এটি Android browser-এ ব্যবহারযোগ্য Streamlit web app। এতে আছে:
- চার্টের screenshot আপলোড করে শিক্ষামূলক AI ব্যাখ্যা
- Twelve Data API দিয়ে সমর্থিত symbol-এর market data দেখা
- কোনো auto-trading বা real-money order নেই

## Android থেকে চালানোর সহজ পথ

1. ZIP ফাইলটি Extract করুন।
2. GitHub-এ একটি নতুন repository তৈরি করে এই ফোল্ডারের ফাইলগুলো Upload করুন।
3. https://share.streamlit.io/ খুলে GitHub দিয়ে Sign in করুন।
4. **Create app** চাপুন, repository নির্বাচন করুন এবং Main file path দিন: `app.py`
5. Deploy হলে ওয়েবসাইটের লিংক Android Chrome-এ খুলুন।

## API Key

- Screenshot AI-এর জন্য OpenAI API key লাগবে।
- Market Data-এর জন্য Twelve Data API key লাগবে।
- অ্যাপের বাম পাশের Settings-এ key লিখুন। কোডে key বসাবেন না।
- API provider-এর ব্যবহার-খরচ/সীমা থাকতে পারে। আগে তাদের বর্তমান pricing ও terms দেখে নিন।

## গুরুত্বপূর্ণ সীমাবদ্ধতা

- Twelve Data-তে সব symbol বা Quotex OTC feed পাওয়া যায় না।
- লাইভ ডেটা provider অনুযায়ী delayed বা সীমিত হতে পারে।
- Screenshot-এ timeframe, symbol এবং candle স্পষ্ট রাখুন।
- AI ভুল করতে পারে। পরের candle নিশ্চিতভাবে জানা সম্ভব নয়।
- এটি শিক্ষামূলক টুল; BUY/SELL নির্দেশ, auto-trading বা লাভের নিশ্চয়তা দেয় না।

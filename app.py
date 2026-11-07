import base64
import requests
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Mehedi AI Chart Lab", page_icon="📊", layout="centered")
st.title("📊 Mehedi AI Chart Lab")
st.caption("শেখার ও Demo বিশ্লেষণের জন্য — এটি ট্রেডিং নির্দেশ বা লাভের নিশ্চয়তা নয়।")

st.info(
    "এই অ্যাপটি চার্টের বৈশিষ্ট্য শেখার জন্য। এটি বাস্তব টাকা দিয়ে ট্রেড, "
    "BUY/SELL নির্দেশ, বা পরের ক্যান্ডেলের নিশ্চয়তা দেয় না।"
)

with st.sidebar:
    st.header("API সেটিংস")
    openai_key = st.text_input("OpenAI API Key", type="password",
                               help="নিজের API key এখানে দিন। এটি অ্যাপে স্থায়ীভাবে সংরক্ষণ করা হয় না।")
    market_key = st.text_input("Twelve Data API Key (ঐচ্ছিক)", type="password")
    st.caption("লাইভ ডেটার জন্য Twelve Data key প্রয়োজন। Quotex OTC-এর ডেটা এখানে পাওয়া যাবে—এমন নিশ্চয়তা নেই।")

tab1, tab2 = st.tabs(["📸 Screenshot শেখা", "🌐 Market Data"])

with tab1:
    st.subheader("চার্টের Screenshot বিশ্লেষণ")
    uploaded = st.file_uploader("PNG / JPG চার্টের ছবি দিন", type=["png", "jpg", "jpeg"])
    if uploaded:
        st.image(uploaded, caption="আপলোড করা চার্ট", use_container_width=True)
        if st.button("ছবির চার্ট বুঝিয়ে দাও", type="primary"):
            if not openai_key:
                st.error("আগে Sidebar-এ OpenAI API Key দিন।")
            else:
                try:
                    client = OpenAI(api_key=openai_key)
                    raw = uploaded.getvalue()
                    encoded = base64.b64encode(raw).decode("utf-8")
                    mime = uploaded.type or "image/png"
                    with st.spinner("ছবির চার্ট পড়া হচ্ছে..."):
                        response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[
                                {"role": "system", "content":
                                 "তুমি বাংলা ভাষায় একজন শিক্ষামূলক চার্ট-রিডিং সহকারী। "
                                 "ছবিতে যা স্পষ্ট দেখা যায় শুধু তাই বলবে। "
                                 "ট্রেন্ড, ক্যান্ডেলের গঠন, সম্ভাব্য support/resistance এবং "
                                 "অনিশ্চয়তা ব্যাখ্যা করবে। পরের ক্যান্ডেল নিশ্চিতভাবে বলা যায় না। "
                                 "কোনো BUY/SELL, UP/DOWN ট্রেড নির্দেশ, এন্ট্রি, মেয়াদ বা লাভের "
                                 "প্রতিশ্রুতি দেবে না। তথ্য অস্পষ্ট হলে তা বলবে। "
                                 "শেষে লিখবে: এটি শিক্ষামূলক পর্যবেক্ষণ, ট্রেডিং পরামর্শ নয়।"},
                                {"role": "user", "content": [
                                    {"type": "text", "text": "এই চার্টটি সহজ বাংলায় বুঝিয়ে দাও।"},
                                    {"type": "image_url", "image_url": {
                                        "url": f"data:{mime};base64,{encoded}"
                                    }}
                                ]}
                            ],
                            max_tokens=600
                        )
                    st.markdown("### বিশ্লেষণ")
                    st.write(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"বিশ্লেষণ করা যায়নি: {e}")

with tab2:
    st.subheader("লাইভ Market Data")
    st.write("Twelve Data-এর সমর্থিত symbol-এর সাম্প্রতিক quote ও candle data দেখা যাবে।")
    symbol = st.text_input("Symbol", value="EUR/USD",
                           help="উদাহরণ: EUR/USD, BTC/USD, AAPL")
    interval = st.selectbox("Candle interval", ["1min", "5min", "15min", "1h", "1day"])
    if st.button("Market Data আনো"):
        if not market_key:
            st.warning("Sidebar-এ Twelve Data API Key দিন।")
        elif not symbol.strip():
            st.warning("একটি symbol লিখুন।")
        else:
            try:
                params = {"symbol": symbol.strip(), "interval": interval,
                          "outputsize": 12, "apikey": market_key}
                with st.spinner("Market data আনা হচ্ছে..."):
                    r = requests.get("https://api.twelvedata.com/time_series",
                                     params=params, timeout=20)
                    data = r.json()
                if "values" not in data:
                    st.error(data.get("message", "ডেটা পাওয়া যায়নি। Symbol বা API limit পরীক্ষা করুন।"))
                else:
                    st.success(f"{symbol.upper()} — ডেটা পাওয়া গেছে")
                    st.dataframe(data["values"], use_container_width=True)
                    st.caption("ডেটা provider-এর বিলম্ব/সীমাবদ্ধতা থাকতে পারে; এটি Quotex-এর OTC feed নয়।")
            except Exception as e:
                st.error(f"ডেটা আনা যায়নি: {e}")

st.divider()
st.caption("শুধু শেখা ও পর্যবেক্ষণ। API key কাউকে পাঠাবেন না বা public repository-তে রাখবেন না।")

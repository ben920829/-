import streamlit as st
import random
import json

st.set_page_config(page_title="🎵 猜歌遊戲", layout="centered")

# ====== 預設歌單 ======
default_songs = [
    {
        "title": "紅蓮華",
        "url": "https://www.youtube.com/watch?v=CwkzK-F0Y00",
        "hint": "鬼滅之刃 OP"
    },
    {
        "title": "unravel",
        "url": "https://www.youtube.com/watch?v=Fve_lHIPa-I",
        "hint": "東京喰種 OP"
    },
    {
        "title": "青鳥",
        "url": "https://www.youtube.com/watch?v=2upuBiEiXDk",
        "hint": "火影忍者"
    }
]

# ====== 上傳歌單 ======
st.sidebar.title("📂 歌單設定")
uploaded_file = st.sidebar.file_uploader("上傳歌單 JSON", type="json")

if uploaded_file:
    songs = json.load(uploaded_file)
else:
    songs = default_songs

# ====== 初始化狀態 ======
if "song" not in st.session_state:
    st.session_state.song = random.choice(songs)

if "score" not in st.session_state:
    st.session_state.score = 0

if "question_count" not in st.session_state:
    st.session_state.question_count = 1

if "answered" not in st.session_state:
    st.session_state.answered = False

# ====== UI ======
st.title("🎵 猜歌挑戰")
st.write(f"第 {st.session_state.question_count} 題")
st.write(f"目前分數：{st.session_state.score}")

song = st.session_state.song

# 播放 YouTube
st.video(song["url"], start_time=0)

# 提示
if st.button("💡 顯示提示"):
    st.info(song["hint"])

# 輸入答案
answer = st.text_input("你的答案")

# 提交答案
if st.button("✅ 確認答案") and not st.session_state.answered:
    st.session_state.answered = True

    if answer.strip().lower() == song["title"].lower():
        st.success("🎉 答對了！")
        st.session_state.score += 1
    else:
        st.error(f"❌ 錯了！答案是：{song['title']}")

# 下一題
if st.button("➡️ 下一題"):
    st.session_state.song = random.choice(songs)
    st.session_state.question_count += 1
    st.session_state.answered = False
    st.rerun()

# 重置遊戲
if st.button("🔄 重置遊戲"):
    st.session_state.song = random.choice(songs)
    st.session_state.score = 0
    st.session_state.question_count = 1
    st.session_state.answered = False
    st.rerun()

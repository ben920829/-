import streamlit as st
import random
import json

st.set_page_config(page_title="🎵 猜歌遊戲", layout="centered")

# ====== 讀取歌單 ======
def load_songs():
    try:
        with open("songs.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                return data
            else:
                return []
    except Exception as e:
        st.error(f"讀取 songs.json 失敗：{e}")
        return []

songs = load_songs()

if not songs:
    st.stop()

# ====== 初始化狀態 ======
if "used_indices" not in st.session_state:
    st.session_state.used_indices = []

if "current_index" not in st.session_state:
    st.session_state.current_index = random.randint(0, len(songs) - 1)
    st.session_state.used_indices.append(st.session_state.current_index)

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

song = songs[st.session_state.current_index]

# 播放 YouTube
st.video(song["url"], start_time=0)

# 提示
if st.button("💡 顯示提示"):
    st.info(song.get("hint", "無提示"))

# 輸入答案
answer = st.text_input("你的答案")

# ====== 檢查答案 ======
if st.button("✅ 確認答案") and not st.session_state.answered:
    if not answer.strip():
        st.warning("請輸入答案！")
    else:
        st.session_state.answered = True

        if answer.strip().lower() == song["title"].lower():
            st.success("🎉 答對了！")
            st.session_state.score += 1
        else:
            st.error(f"❌ 錯了！答案是：{song['title']}")

# ====== 下一題（避免重複） ======
if st.button("➡️ 下一題"):
    remaining = list(set(range(len(songs))) - set(st.session_state.used_indices))

    if not remaining:
        st.success("🎉 所有題目已完成！")
    else:
        new_index = random.choice(remaining)
        st.session_state.current_index = new_index
        st.session_state.used_indices.append(new_index)

        st.session_state.question_count += 1
        st.session_state.answered = False
        st.rerun()

# ====== 重置 ======
if st.button("🔄 重置遊戲"):
    st.session_state.used_indices = []
    st.session_state.current_index = random.randint(0, len(songs) - 1)
    st.session_state.used_indices.append(st.session_state.current_index)

    st.session_state.score = 0
    st.session_state.question_count = 1
    st.session_state.answered = False

    st.rerun()

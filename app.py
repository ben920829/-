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

if "question_count" not in st.session_state:
    st.session_state.question_count = 1

if "answered" not in st.session_state:
    st.session_state.answered = False

song = songs[st.session_state.current_index]

# ====== UI ======
st.title("🎵 猜歌挑戰")
st.write(f"第 {st.session_state.question_count} 題")

# 盲猜階段：不顯示影片
if not st.session_state.answered:
    st.info("🎧 盲猜階段，影片畫面隱藏（請自己記住或猜歌）")

# 公布答案後顯示影片
if st.session_state.answered:
    st.video(song["url"], start_time=0)

# ====== 提示 ======
if st.button("💡 顯示提示"):
    st.info(song.get("hint", "無提示"))

# ====== 公布答案 ======
if st.button("👀 公布答案") and not st.session_state.answered:
    st.session_state.answered = True
    st.success(f"答案是：{song['title']}")
    st.rerun()

# ====== 下一題 ======
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

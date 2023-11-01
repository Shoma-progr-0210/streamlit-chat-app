from bardapi import Bard
import streamlit as st
import openai
import os
from PIL import Image

# APIキーの設定
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GOOGLE_BARD_TOKEN = os.environ.get("GOOGLE_BARD_TOKEN")

# GOOGLE_BARD_TOKENS = {
#     "__Secure-1PSID": os.environ.get("GOOGLE_BARD_TOKEN__Secure-1PSID"),
#     "__Secure-1PSIDTS": os.environ.get("GOOGLE_BARD_TOKEN__Secure-1PSIDTS"),
#     "__Secure-1PSIDCC": os.environ.get("GOOGLE_BARD_TOKEN__Secure-1PSIDCC"),
# }

if not OPENAI_API_KEY:
    raise Exception('OPENAI_API_KEY is not found.')

openai.api_key = OPENAI_API_KEY

USER_NAME = "user"
ASSISTANT_NAME = "assistant"

google_icon = Image.open('./image/unnamed.png')
openai_icon = Image.open('./image/openai-white-logomark.png')

avatars = {
    USER_NAME: "😎",
    "ChatGPT": openai_icon,
    "Google Bard": google_icon,
}

google_bard_prompt = [
"以下のように会話した前提でGoogle Bardの回答を生成して回答部分のみをそのまま返信してください。",
"Google Bardはあなた自身の発言です。",
"",
# user: 好きな言葉は？一言で答えて。
# Google Bard: 希望
# user: 次に好きな言葉は？
# Google Bard: 愛
# user: その二つの言葉で100文字以内の文章を作って
]

# チャットログを保存したセッション情報を初期化
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

if "chatai" not in st.session_state:
    st.session_state.chatai = "ChatGPT"

def display_chat_log(chat_log):
    # チャットログを表示
    for chat in chat_log:
        with st.chat_message(chat["role"], avatar=avatars[chat["name"]]):
            st.write(chat["content"])

st.title("Streamlit ChatApp")

col1, col2 = st.columns(2)
chatai = ""


# チャット相手
with col1:
    chatai = st.radio(
        "話しかける相手",
        ["ChatGPT", "Google Bard"],
        key="chatai",
        horizontal=True,
        # on_change=display_chat_log,
        # args=(st.session_state.chat_log,),
    )

with col2:
    if st.button('🔄新しい会話を始める'):
        st.session_state.chat_log = []


def talk_chatgpt(chat_logs: str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": x["role"], "content": x["content"]} for x in chat_logs],
        stream=True,
    )
    return response

def talk_bard(chat_logs: str):
    bard = Bard(token=GOOGLE_BARD_TOKEN, timeout=30)

    messages = google_bard_prompt + ["Google Bard: " + x["content"] if x["role"] != "user" else "user: " + x["content"] for x in chat_logs]

    return bard.get_answer("\n".join(messages))


user_msg = st.chat_input("ここにメッセージを入力")
if user_msg:
    # セッションにユーザーのメッセージを追加
    st.session_state.chat_log.append({"role": USER_NAME, "content": user_msg, "name": USER_NAME})

    display_chat_log(st.session_state.chat_log)

    if chatai == "ChatGPT":
        # アシスタントのメッセージを表示
        response = talk_chatgpt(st.session_state.chat_log)
        with st.chat_message(chatai, avatar=avatars[chatai]):
            assistant_msg = ""
            assistant_response_area = st.empty()
            for chunk in response:
                # 回答を逐次表示
                tmp_assistant_msg = chunk["choices"][0]["delta"].get("content", "")
                assistant_msg += tmp_assistant_msg
                assistant_response_area.write(assistant_msg)

        st.session_state.chat_log.append({"role": ASSISTANT_NAME, "content": assistant_msg, "name": chatai})
    elif chatai == "Google Bard":
        response = talk_bard(st.session_state.chat_log)
        assistant_msg = response["content"]
        with st.chat_message(chatai, avatar=avatars[chatai]):
            st.write(assistant_msg)

        st.session_state.chat_log.append({"role": ASSISTANT_NAME, "content": assistant_msg, "name": chatai})
    else:
        with st.chat_message("ai"):
            st.write("話しかける相手を選択してください")

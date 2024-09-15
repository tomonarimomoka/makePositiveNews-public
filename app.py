#####IMPORT###################################################
import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from article import ArticleParser

#####DEF###################################################
def makePrompt(language , artical):
    prompt = f"""以下の手順で、記事の内容をポジティブにしてください。記事の内容を要約してはいけません。Let's think step by step.
    【手順1】
    例えば、以下の様にポジティブな表現に変えてください。この時に、引用された発言は書き換えてはいけません。また、文章は要約せずに忠実に変換してください。
    ・「積極性に欠ける」は「控えめな性格」
    ・「頭が悪い」は「天然」
    ・「貧乏」は「清貧」
    ・「忙しい」は「充実している」
    ・「キモイ」は「優しそう」
    【手順２】
    例えば、以下の様に過激な表現やグロテスクな表現は柔らかい表現に変更して下さい。
    ・「殺す」は「天国へ導いた」
    【手順3】
    見出しは作らずにポジティブにしたニュースをプレーンテキストで出力してください。
    【手順4】
    出力言語は{language}にしてください。
    【手順5】
    ・出力言語が日本語の場合、語尾は「なんだよ💓」や「だよ」や「だって～！」とか「らしいよ✨」とか「♡」にしてください。
    ・語尾が絵文字の時は「。」を削除してください。
    ・出力言語が日本語以外の場合は「♡」とか「★」とか「😊」とか「💕」や「🍀」を使ってください。
    【注意点】
    ・記事の内容を要約せずにポジティブにして表示してください
    ・{language}に直して表示してください。
記事は以下です。
    {artical}"""
    
    print(prompt)
    return prompt

#####MAIN###################################################
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
st.set_page_config(layout="wide")

# テキスト入力
url = st.text_input("URLを入力してください")

# 言語を選ばせたい
language = st.selectbox(
    "出力言語を選択してください。\nPlease choose the output language.",
    ("日本語", "英語", "中国語"),
)

# ポジティブボタン押下処理
if st.button("ポジティブ化する💖"):
    parser = ArticleParser(url)
    article = parser.get_article_body()
    prompt = makePrompt(language,article["body"])

    # 　GPTへ渡す情報
    model_name = "gpt-4o-mini"
    role = "あなたはプロの心理カウンセラーです。\n"
    

    response = ""
    with st.balloons():
        # API叩く
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": prompt},
            ],
        )
    result = response.choices[0].message.content.strip()

    st.header("記事タイトル")
    st.write(article["title"])

    # 2つの列を作成
    col1, col2 = st.columns(2)

    # 左側の列に表示する内容
    with col1:
        st.header("原文😢")
        st.markdown(article["body"])

    # 右側の列に表示する内容
    with col2:
        st.header("💗ポジティブ化したニュース💗")
        st.markdown(result)

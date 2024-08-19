import streamlit as st # フロントエンドを扱うstreamlitの機能をインポート
from openai import OpenAI # openAIのchatGPTのAIを活用するための機能をインポート


# アクセスの為のキーをos.environ["OPENAI_API_KEY"]に代入し、設定

import os # OSが持つ環境変数OPENAI_API_KEYにAPIを入力するためにosにアクセスするためのライブラリをインポート
# ここにご自身のAPIキーを入力してください！

os.environ["OPENAI_API_KEY"]

# openAIの機能をclientに代入
client = OpenAI()


# chatGPTにリクエストするためのメソッドを設定。引数には書いてほしい内容と文章のテイストと最大文字数を指定
def run_gpt(content_text_to_gpt,content_kind_of_to_gpt,content_maxStr_to_gpt):
    # リクエスト内容を決める
    request_to_gpt = content_text_to_gpt + " また、これを記事として読めるように、記事のタイトル、目次、内容の順番で出力してください。内容は"+ content_maxStr_to_gpt + "文字以内で出力してください。" + "また、文章は" + content_kind_of_to_gpt + "にしてください。"
    
    # 決めた内容を元にclient.chat.completions.createでchatGPTにリクエスト。オプションとしてmodelにAIモデル、messagesに内容を指定
    response =  client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": request_to_gpt },
        ],
    )

    # 返って来たレスポンスの内容はresponse.choices[0].message.content.strip()に格納されているので、これをoutput_contentに代入
    output_content = response.choices[0].message.content.strip()
    return output_content # 返って来たレスポンスの内容を返す

print('GPTに記事書かせるアプリ')# タイトル

# 書かせたい内容
content_text_to_gpt = "ワンピースについて教えてください！"
            
# 書かせたい内容のテイストを選択肢として表示する
content_kind_of_to_gpt = "中立的で客観的な文章"

# chatGPTに出力させる文字数
content_maxStr_to_gpt = "500"

output_content_text = run_gpt(content_text_to_gpt,content_kind_of_to_gpt,content_maxStr_to_gpt)
print(output_content_text)
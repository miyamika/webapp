
import streamlit as st
import pandas as pd
import yfinance as yf
import altair as alt

# 取得する銘柄の名前とキーを変換する一覧を設定
tickers = {
    'apple': 'AAPL',
    'facebook': 'META',
    'google': 'GOOGL',
    'microsoft': 'MSFT',
    'netflix': 'NFLX',
    'amazon': 'AMZN',
    'TOTO': '5332.T',
    'TOYOTA': '7203.T',
}

st.title('株価可視化アプリ')
st.sidebar.write("""
### こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
""")

# スライドバーを用いて、取得する日数を選択
days = st.sidebar.slider('表示日数選択', 1, 50, 10)

# サポートされる期間に変換
if days <= 5:
    period = '5d'
elif days <= 30:
    period = '1mo'
elif days <= 90:
    period = '3mo'
elif days <= 180:
    period = '6mo'
else:
    period = '1y'

st.write(f"過去 {days} 日間 の株価")

def get_data(period, tickers):
    df = pd.DataFrame()

    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=period)
        hist.index = pd.to_datetime(hist.index).strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T  # 転置
        hist.index.name = 'Name'  # インデックスの名前を設定
        df = pd.concat([df, hist])  # データを結合
    
    return df

df = get_data(period, tickers)
st.write(df)

# データを整形してチャートを作成
df = df.reset_index()  # インデックスをリセット
df = pd.melt(df, id_vars=['Name'], var_name='Date', value_name='Stock Prices (USD)')

chart = (
    alt.Chart(df)
    .mark_line(opacity=0.8, clip=True)
    .encode(
        x='Date:T',
        y=alt.Y('Stock Prices (USD):Q', stack=None),
        color='Name:N'
    )
)

st.altair_chart(chart, use_container_width=True)

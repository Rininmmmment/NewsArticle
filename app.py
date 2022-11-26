from newspaper import Article
import requests
import urllib
from bs4 import BeautifulSoup
import nltk
nltk.download('punkt')

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer 

import streamlit as st

news_number = 3

keyword = st.text_input(label='Search Word', value='Python')

url = 'https://news.google.com/search'

params_ja = {'hl':'ja', 'gl':'JP', 'ceid':'JP:ja', 'q':keyword}
params_en = {'hl':'en-US', 'gl':'US', 'ceid':'US:en', 'q':keyword}
article_no = 1

# url、パラメータを設定してリクエストを送る
res = requests.get(url, params=params_en)
# レスポンスをBeautifulSoupで解析する
soup = BeautifulSoup(res.content, "html.parser")

# レスポンスからh3階層のニュースを抽出する（classにxrnccdを含むタグ）
h3_blocks = soup.select(".xrnccd")

for i, h3_entry in enumerate(h3_blocks):

    # 記事を10件だけ処理する
    if article_no == news_number:
        break
    
    # ニュースのタイトルを抽出する（h3タグ配下のaタグの内容）
    h3_title = h3_entry.select_one("h3 a").text
    # ニュースのリンクを抽出する（h3タグ配下のaタグのhref属性）
    h3_link = h3_entry.select_one("h3 a")["href"]
    # 抽出したURLを整形して絶対パスを作る
    h3_link = urllib.parse.urljoin(url, h3_link)
    # 記事を分析する
    article = Article(h3_link)
    article.download()
    article.parse()
    text = article.text
    parser_ja = PlaintextParser.from_string(text, Tokenizer('japanese'))
    parser_en = PlaintextParser.from_string(text, Tokenizer('english'))
    summarizer = TextRankSummarizer()
    res = summarizer(document=parser_en.document, sentences_count=1)
    if text == "":
        news_number += 1
        continue
    # ニュースのタイトル、リンクをファイルに書き込む
    st.header(h3_title)
    for sentence in res:
        st.subheader(str(sentence))
    st.write(text)
    st.write('\r\n')
    st.write(h3_link)
    st.write('\r\n')
    st.write('\r\n')

    article_no = article_no + 1
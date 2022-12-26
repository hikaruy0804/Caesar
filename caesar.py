import streamlit as st
from pykakasi import kakasi
import unicodedata
import re

st.title('暗号化システム')

# 文字リストの作成
def moji_list(*args):
    moji = []
    for i in range(len(args)):
        moji.extend([chr(j) for j in range(args[i][0], args[i][1])])
    return moji

moji_lists = moji_list((97, 123),  (48, 58), (12353, 12436), )

# ページ遷移
menu = st.selectbox('メニュー',['ホーム','暗号化','複合化'])

if menu == 'ホーム':
  st.write('利用規約')
  st.write('システム利用に損害や責任は負いません。全て自己責任で使ってください。')


elif menu == '暗号化':
  key = st.number_input('暗号キー', 0, len(moji_lists), 0)
  texts =  st.text_area(label="入力欄",height = 150)

  if st.button('暗号化'):

    texts = ''.join(texts) #リストエラー対策
    texts = re.findall("[^。]+。?", texts.replace('\n', ''))
    texts = ''.join(texts) #リストエラー対策
    texts = texts.replace('　','') #リストエラー対策
    texts = texts.lower()
    texts = ''.join(texts) #リストエラー対策

    kakasi = kakasi()
    kakasi.setMode('J', 'H') #漢字からひらがなに変換
    kakasi.setMode("K", "H") #カタカナからひらがなに変換
    conv = kakasi.getConverter()

    texts = conv.do(texts)
    
    en_list = [] # 文字をずらす処理
    for text in texts: #一文字ずつ取り出す
      if text in moji_lists: #文字照合リストに暗号したい文字があれば
          i = moji_lists.index(text) #インデックスを探す
          if len(moji_lists) <= (i + key): #文字照合リストよりインデックス＋keyが大きければ
            s = (key + i) % len(moji_lists) #繰り越したインデックスで追加
            en_list.append(moji_lists[s])
          else: #文字照合リストよりインデックス＋keyが小さければ
            en_list.append(moji_lists[i + key]) #そのまま追加
      else: #文字照合リストに暗号したい文字がなければそのまま追加
        en_list.append(text)
        
    texts =  unicodedata.normalize('NFKC', texts)
    en = ''.join(en_list)
    
    st.write('暗号キー',key)
    st.write(en)

##複合化
elif menu == '複合化':
  key = st.number_input('復号キー', 0, len(moji_lists), 0)
  texts =  st.text_area(label="入力欄",height = 150)
  
  if st.button('暗号化'):
    
    de_list = [] # 文字をずらす処理
    
    texts = ''.join(texts) #リストエラー対策
    texts = re.findall("[^。]+。?", texts.replace('\n', ''))
    texts = ''.join(texts) #リストエラー対策
    texts = texts.replace('　','') #リストエラー対策
    texts = texts.lower()
    texts = ''.join(texts) #リストエラー対策
    
    for text in texts: #一文字ずつ取り出す
      if text in moji_lists: #文字照合リストに複合したい文字があれば
        i = moji_lists.index(text) #インデックスを探す
        if i + 1 - key < 0: #インデックスからkeyを引いた値が0より小さければ
          
          s = len(moji_lists) - (key - i) # 文字照合リストからkeyからインデックスを引いた値をsとする。
          if abs(s) >= len(moji_lists): # 絶対値でリスト数から確認
            s = s % len(moji_lists) # 余りを算定

          de_list.append(moji_lists[s]) #余り復号化。
        else: #文字照合リストよりインデックス＋keyが小さければ
          de_list.append(moji_lists[i - key]) #keyを引いたインデックスで複合化
      else: #文字照合リストに複合したい文字がなければそのまま追加
        de_list.append(text)
        
    texts =  unicodedata.normalize('NFKC', texts)
    de = ''.join(de_list)
    
    st.write(de)

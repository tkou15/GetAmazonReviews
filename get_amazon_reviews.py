import requests     # webデータダウンロード用
import bs4          # HTML解析用のライブラリ
import pyperclip    # コピー＆ペーストをするためのライブラリ
import textwrap     # 長い文字列を改行して表示

# 全ページ分リストにする
def get_all_reviews(url):
    rvw_list = []
    i = 1
    while True:
        print(i,'searching')
        i += 1
        res = requests.get(url)
        amazon_soup = bs4.BeautifulSoup(res.text, features='lxml')
        rvws = amazon_soup.select('.review-text') # レビューをリストにして取り出す
        for rvw in rvws:
            rvw_list.append(rvw)

        next_page = amazon_soup.select('li.a-last a')   # 次へボタン

        if next_page != []:     # 次へボタンがあれば
            next_url = 'https://www.amazon.co.jp/' + next_page[0].attrs['href']    # 次へボタンの中にあるURLを参照
            url = next_url         # URLを更新
        else:
            break

    return rvw_list

if __name__ == '__main__':
    print('Amazonのレビューを取得します\nURLを入力してください。')
    key_word = input('URL:')      # 検索キーワードの入力
    url = pyperclip.paste()     # ペーストする。URLをコピーしておかないとエラー出る
    new_url = url.replace('dp', 'product-reviews')     # URLをレビューページのものに書き換える
    rvw_list = get_all_reviews(new_url)    # レビューの取得

    # 全データを表示
    for i in range(len(rvw_list)):
        rvw_text = textwrap.fill(rvw_list[i].text, 80)
        print('\nreview{} : '.format(i+1))
        print(rvw_text)
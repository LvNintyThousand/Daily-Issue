import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

num = 0


def get_text(url):
    try:
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/85.0.4183.102 Safari/537.36', 'Accept-Language': 'en-US '
        }
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "Webscraping Fails！"


def run(game_info, jump_link, game_evaluation_general, game_evaluation_positive_percentage, game_evaluation_total_count, text):
    soup = BeautifulSoup(text, "html.parser")

    # 游戏评价
    w = soup.find_all(class_="col search_reviewscore responsive_secondrow")
    for u in w:
        if u.span is not None:
            game_evaluation_general.append(
                u.span["data-tooltip-html"].split("<br>")[0])
            game_evaluation_positive_percentage.append(
                re.sub("\D" , "", u.span['data-tooltip-html'].split('<br>')[-1][0:11]))
            game_evaluation_total_count.append(
                re.sub("\D" , "", u.span['data-tooltip-html'].split('<br>')[-1][11:-1])
                )
        else:
            game_evaluation_general.append("Not having any comments yet")
            game_evaluation_positive_percentage.append('0')
            game_evaluation_total_count.append('0')

    # 游戏详情页面链接
    link_text = soup.find_all("div", id="search_resultsRows")
    for k in link_text:
        b = k.find_all('a')
        for j in b:
            jump_link.append(j['href'])

    # 名字和价格
    global num
    name_text = soup.find_all('div', class_="responsive_search_name_combined")
    for z in name_text:
        # 每个游戏的价格
        name = z.find(class_="title").string.strip()
        # 判断折扣是否为None，提取价格
        if z.find(class_="col search_discount responsive_secondrow").string is None:
            price = z.find(class_="col search_price discounted responsive_secondrow").text.strip().split("$")
            game_info.append([num + 1, name, price[2].strip(), game_evaluation_general[num], game_evaluation_positive_percentage[num], game_evaluation_total_count[num], jump_link[num]])
        else:
            price = z.find(class_="col search_price responsive_secondrow").string.strip().split("$")
            game_info.append([num + 1, name, price[1], game_evaluation_general[num], game_evaluation_positive_percentage[num], game_evaluation_total_count[num], jump_link[num]])
        num = num + 1


def save_data(game_info):
    save_path = "F:/Baruch College/Project/Steam.csv"
    df = pd.DataFrame(game_info, columns=['Rank', 'Name', 'Current_Price(USD)', 'General_Evaluation', 'Positive_Percentage', 'Review_Total_Count', 'Links'])
    df.to_csv(save_path, index=0, encoding = 'utf-8-sig')
    print("The files has been successfully saved！")


if __name__ == "__main__":
    Game_info = []  # 游戏全部信息
    Turn_link = []  # 翻页链接
    Jump_link = []  # 游戏详情页面链接
    General_evaluation = []  # 游戏好评率和评价
    Positive_Percentage = []
    Review_Total_Count = []
    for i in range(1, 11):
        Turn_link.append(
            "https://store.steampowered.com/search/?filter=globaltopsellers&page=1&os=win" + str("&page=" + str(i)))
        run(Game_info, Jump_link, General_evaluation, Positive_Percentage, Review_Total_Count, get_text(Turn_link[i - 1]))
    save_data(Game_info)
import requests
from bs4 import BeautifulSoup
import concurrent.futures

# マルシンURL
url = 'https://ana-slo.com/%E3%83%9B%E3%83%BC%E3%83%AB%E3%83%87%E3%83%BC%E3%82%BF/%E6%84%9B%E7%9F%A5%E7%9C%8C/%E3%83%9E%E3%83%AB%E3%82%B7%E3%83%B3777-%E3%83%87%E3%83%BC%E3%82%BF%E4%B8%80%E8%A6%A7/'


def getEndNumber(url, index, endNumber):
    child_r = requests.get(url)
    child_r.encoding = child_r.apparent_encoding
    child_soup = BeautifulSoup(child_r.text, 'lxml')
    # class： avg_get_medals_tableを探す
    child_table = child_soup.find('div', id='tab01_last_digit_' + endNumber)
    # class：table_cellsのtdタグを全て探す
    child_row = child_table.find_all('td', class_='table_cells')
    # 該当末尾の差枚を取得していく
    child_data = []
    cell_number = 2
    while(cell_number < len(child_row)):
        child_data.append(child_row[cell_number].text)
        cell_number += 10
    # 文字列の"+"と","を除去
    number_data = []
    for j in range(len(child_data)):
        child_data[j] = child_data[j].replace(',', '')
        child_data[j] = child_data[j].replace('+', '')

    # リストの中身を数値に変換して別のリストに格納
    number_data = [int(str) for str in child_data]
    # リストの中身を足し合わせる
    return (index, sum(number_data))


def getTitleEndNumber(url, index, endNumber, titleStr):
    child_r = requests.get(url)
    child_r.encoding = child_r.apparent_encoding
    child_soup = BeautifulSoup(child_r.text, 'lxml')
    # class： avg_get_medals_tableを探す
    child_table = child_soup.find('div', id='tab01_last_digit_' + endNumber)
    # class：table_cellsのtdタグを全て探す
    child_row = child_table.find_all('td', class_=['fixed01','table_cells'])
    # 該当末尾の差枚を取得していく
    child_data = []
    cell_number = 0
    while(cell_number < len(child_row)):
        if (titleStr in child_row[cell_number].text):
            child_data.append(child_row[cell_number + 3].text)
        cell_number += 11
    # 文字列の"+"と","を除去
    number_data = []
    for j in range(len(child_data)):
        child_data[j] = child_data[j].replace(',', '')
        child_data[j] = child_data[j].replace('+', '')
    # リストの中身を数値に変換して別のリストに格納
    number_data = [int(str) for str in child_data]
    # リストの中身を足し合わせる
    return (index, sum(number_data))


def end_number_message(choiceDate, endNumber):
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    # HTMLのパース
    soup = BeautifulSoup(r.text, 'lxml')
    # class： date-tableを探す
    table = soup.find('div', class_='date-table')
    # class：table-data-cellのtdタグを全て探す
    lst_row = table.find_all('div', class_='table-data-cell')

    # 日付の配列と引数の文字列比較(部分一致)
    flag = False
    cell_number = 0
    urls = []
    while (cell_number < len(lst_row)):
        if choiceDate in lst_row[cell_number].find('a').get('href'):
            flag = True
            urls.append(lst_row[cell_number].find('a').get('href'))
        cell_number += 5

    if flag == False:
        return '日付がありません'

    total_result = []
    # リンク先に飛んで差数を拾ってくる
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls)) as executor:
        # 各URLに対して処理を実行
        futures = [executor.submit(getEndNumber, url, i, endNumber)
                   for i, url in enumerate(urls)]
        # 各処理の結果を取得して合計
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                total_result.append(result)
            except Exception as e:
                print(f'Error occurred: {e}')

        # indexの大きい順序でデータを整列させる
        total_result = sorted(total_result, key=lambda x: x[0], reverse=True)
        # indexの値を日にちに変更
        date = 1
        for i in range(len(total_result)):
            total_result[i] = (date, total_result[i][1])
            date += 1
    return (total_result)


def end_title_number_message(choiceDate, endNumber, titleStr):
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    # HTMLのパース
    soup = BeautifulSoup(r.text, 'lxml')
    # class： date-tableを探す
    table = soup.find('div', class_='date-table')
    # class：table-data-cellのtdタグを全て探す
    lst_row = table.find_all('div', class_='table-data-cell')
    # 日付の配列と引数の文字列比較(部分一致)
    flag = False
    cell_number = 0
    urls = []
    while (cell_number < len(lst_row)):
        if choiceDate in lst_row[cell_number].find('a').get('href'):
            flag = True
            urls.append(lst_row[cell_number].find('a').get('href'))
        cell_number += 5
    if flag == False:
        return '日付がありません'

    total_result = []
    # リンク先に飛んで差数を拾ってくる
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls)) as executor:
        # 各URLに対して処理を実行
        futures = [executor.submit(
            getTitleEndNumber, url, i, endNumber, titleStr) for i, url in enumerate(urls)]
        # 各処理の結果を取得して合計
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                total_result.append(result)
            except Exception as e:
                print(f'Error occurred: {e}')

        # indexの大きい順序でデータを整列させる
        total_result = sorted(total_result, key=lambda x: x[0], reverse=True)
        # indexの値を日にちに変更
        date = 1
        for i in range(len(total_result)):
            total_result[i] = (date, total_result[i][1])
            date += 1
    return(total_result)


def create_title_message(text, title):
    csv = 'タイトル,台番号,差枚\n'
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    # HTMLのパース
    soup = BeautifulSoup(r.text, 'lxml')
    # class： date-tableを探す
    table = soup.find('div', class_='date-table')
    # class：table-data-cellのtdタグを全て探す
    lst_row = table.find_all('div', class_='table-data-cell')
    # 日付の配列と引数の文字列比較(部分一致)
    flag = False
    cell_number = 0
    while (cell_number < len(lst_row)):
        if text in lst_row[cell_number].find('a').get('href'):
            flag = True
            date = lst_row[cell_number].find('a').get('href')
            break
        cell_number += 5

    if flag == False:
        print("debug_message_search_null")
        return csv

    # リンク先に飛んで差数を拾ってくる
    child_r = requests.get(date)
    child_r.encoding = child_r.apparent_encoding
    child_soup = BeautifulSoup(child_r.text, 'lxml')
    # class： fixed_get_medals_tableを探す
    child_table = child_soup.find(
        'table', class_='fixed_get_medals_table', id='all_data_table')
    # class：table_cellsのtdタグを全て探す
    child_row = child_table.find_all('td')

    cell_number = 0
    while (cell_number < len(child_row)):
        if title in child_row[cell_number].text:
            # 文字列の"+"と","を除去
            content_title = (child_row[cell_number].text).replace(',', '')
            content_title = content_title.replace(',', '')
            content_stand = (child_row[cell_number + 1].text).replace(',', '')
            content_stand = content_stand.replace(',', '')
            content_count = (child_row[cell_number + 3].text).replace(',', '')
            content_count = content_count.replace(',', '')
            csv += content_title + ',' + content_stand + ',' + content_count + '\n'
        cell_number += 11

    # デバッグ用
    print(csv)
    return csv


def create_message(text):
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    # HTMLのパース
    soup = BeautifulSoup(r.text, 'lxml')
    # class： date-tableを探す
    table = soup.find('div', class_='date-table')
    # class：table-data-cellのtdタグを全て探す
    lst_row = table.find_all('div', class_='table-data-cell')

    # 日付の配列と引数の文字列比較(部分一致)
    flag = False
    date = ''
    cell_number = 0
    while (cell_number < len(lst_row)):
        if text in lst_row[cell_number].find('a').get('href'):
            flag = True
            date = lst_row[cell_number].find('a').get('href')
            break
        cell_number += 5

    if flag == False:
        return '日付がありません'

    # リンク先に飛んで差数を拾ってくる
    child_r = requests.get(date)
    child_r.encoding = child_r.apparent_encoding
    child_soup = BeautifulSoup(child_r.text, 'lxml')
    # class： avg_get_medals_tableを探す
    child_table = child_soup.find('table', class_='fixed_get_medals_table')
    # class：table_cellsのtdタグを全て探す
    child_row = child_table.find_all('td', class_='table_cells')
    # 全台の差枚を取得していく
    child_data = []
    # 全台の総ゲームを取得していく
    game_data = []
    cell_number = 1
    while (cell_number < len(child_row)):
        game_data.append(child_row[cell_number].text)
        child_data.append(child_row[cell_number + 1].text)
        cell_number += 10
    # 文字列の"+"と","を除去
    # "-"はそのままでいけるか？
    number_list = []
    game_list = []
    for j in range(len(child_data)):
        child_data[j] = child_data[j].replace(',', '')
        child_data[j] = child_data[j].replace('+', '')
        game_data[j] = game_data[j].replace(',', '')
        game_data[j] = game_data[j].replace('+', '')

    # リストの中身を数値に変換して別のリストに格納
    number_list = [int(str) for str in child_data]
    game_list = [int(str) for str in game_data]
    return [sum(number_list), sum(game_list)]


def getTotalDate(url, index, endNumber):
    child_r = requests.get(url)
    child_r.encoding = child_r.apparent_encoding
    child_soup = BeautifulSoup(child_r.text, 'lxml')
    # class： avg_get_medals_tableを探す
    child_table = child_soup.find('div', id='tab01_last_digit_' + endNumber)
    # class：table_cellsのtdタグを全て探す
    child_row = child_table.find_all('td', class_='table_cells')
    # 該当末尾の差枚を取得していく
    child_data = []
    cell_number = 2
    while(cell_number < len(child_row)):
        child_data.append(child_row[cell_number].text)
        cell_number += 10
    # 文字列の"+"と","を除去
    number_data = []
    for j in range(len(child_data)):
        child_data[j] = child_data[j].replace(',', '')
        child_data[j] = child_data[j].replace('+', '')

    # リストの中身を数値に変換して別のリストに格納
    number_data = [int(str) for str in child_data]
    # リストの中身を足し合わせる
    return (index, sum(number_data))


def total_date_message(choiceDate, endNumber):
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    # HTMLのパース
    soup = BeautifulSoup(r.text, 'lxml')
    # class： date-tableを探す
    table = soup.find('div', class_='date-table')
    # class：table-data-cellのtdタグを全て探す
    lst_row = table.find_all('div', class_='table-data-cell')

    # 日付の配列と引数の文字列比較(部分一致)
    flag = False
    cell_number = 0
    urls = []
    while (cell_number < len(lst_row)):
        if choiceDate in lst_row[cell_number].find('a').get('href'):
            flag = True
            urls.append(lst_row[cell_number].find('a').get('href'))
        cell_number += 5

    if flag == False:
        return '日付がありません'

    total_result = []
    # リンク先に飛んで差数を拾ってくる
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls)) as executor:
        # 各URLに対して処理を実行
        futures = [executor.submit(getTotalDate, url, i, endNumber)
                   for i, url in enumerate(urls)]
        # 各処理の結果を取得して合計
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                total_result.append(result)
            except Exception as e:
                print(f'Error occurred: {e}')

        # indexの大きい順序でデータを整列させる
        total_result = sorted(total_result, key=lambda x: x[0], reverse=True)
        # indexの値を日にちに変更
        date = 1
        for i in range(len(total_result)):
            total_result[i] = (date, total_result[i][1])
            date += 1

    return (total_result)

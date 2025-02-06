import discord
import pykakasi
import matplotlib.pyplot as plt
import japanize_matplotlib
import io
import datetime as dt
import re
import report_generator

# discordのトークン
TOKEN = ''
client = discord.Client(intents=discord.Intents.all())
# 前日の収支を返すパターン
pattern = r'\d{4}-\d{2}-\d{2}'
# 前日のタイトル毎の収支を返すパターン
title_pattern = r'\d{4}-\d{2}-\d{2}_\S+'
# ひと月の末尾収支を返すパターン(タイトル別)
end_title_pattern = r'\d{4}-\d{2}_\d{1}_\S+'
# ひと月の末尾収支を返すパターン
end_pattern = r'\d{4}-\d{2}_\d{1}'

# 曜日
__WEEKDAY = ('月', '火', '水', '木', '金', '土', '日')
# 日本語をローマ字変換するための設定
kakasi = pykakasi.kakasi()
kakasi.setMode('H', 'a')
kakasi.setMode('K', 'a')
kakasi.setMode('J', 'a')
conversion = kakasi.getConverter()
# 日本語フォントを設定
plt.rcParams['font.family'] = 'Yu Gothic'  # Windowsの場合は 'Yu Gothic'、Linuxの場合は 'IPAGothic' を指定


@client.event
async def on_ready():
  print('報告botがサーバーにログインしました！')

@client.event
# テキストを打ち込んだら反応する場所
async def on_message(message):
  if message.author.bot:
    return
  # テスト用メッセージ
  if message.content == '!ready':
    await message.channel.send('【テスト動作】報告botが参加したよ！')
    return

  # 前日のタイトル毎の収支を返す
  elif re.match(title_pattern, message.content):
    # 日付とタイトルに分割
    str = (message.content).split('_')
    choiceDate = str[0]
    title = str[1]
    splitDate = (choiceDate).split('-')

    data = report_generator.create_title_message(choiceDate, title)
    if bool(data) == False:
      embed = discord.Embed(  # Embedを定義する
        title="ERROR!!",  # タイトル
        color=0xff0000,  # フレーム色指定(今回は赤)
        description="検索結果が0件です",  # Embedの説明文 必要に応じて
      )
      await message.channel.send(embed=embed)
    else:
      date = dt.date(int(splitDate[0]), int(splitDate[1].lstrip('0')),
                     int(splitDate[2].lstrip('0')))
      date_str = splitDate[0] + '年' + splitDate[1] + '月' + splitDate[
        2] + '日 (' + __WEEKDAY[date.weekday()] + ')'

      await message.channel.send(date_str)
      await message.channel.send('「' + title + '」の検索結果')
      with io.StringIO(data) as file:
        await message.channel.send(file=discord.File(
          file, filename=date_str + conversion.do(title) + '.csv'))

  # 前日の収支を返す
  elif re.match(pattern, message.content):
    text = (message.content).split('-')
    str = report_generator.create_message(message.content)
    if str == '日付がありません':
      embed = discord.Embed(
        title="ERROR!!",
        color=0xff0000,
        description="お店の収支が手に入りませんでした",
      )
      await message.channel.send(embed=embed)
    else:
      date = dt.date(int(text[0]), int(text[1].lstrip('0')),
                     int(text[2].lstrip('0')))
      embed = discord.Embed(
        title=text[0] + '年' + text[1] + '月' + text[2] + '日 (' +
        __WEEKDAY[date.weekday()] + ')',
        color=0x00ff00,
      )
      embed.add_field(name="収支", value=str[0])  # フィールドを追加。
      embed.add_field(name="総ゲーム数", value=str[1])
      await message.channel.send(embed=embed)

  elif re.match(end_title_pattern, message.content):
    str = (message.content).split('_')
    choiceDate = str[0]
    endNumber = str[1]
    titleStr = str[2]
    splitDate = (choiceDate).split('-')
    datas = report_generator.end_title_number_message(choiceDate, endNumber, titleStr)
    # 結果のリストを解析して、x軸とy軸の値を取得します
    x = [data[0] for data in datas]
    y = [data[1] for data in datas]
    # 以前のグラフを削除
    plt.clf()
    # グラフを作成
    plt.plot(x, y, marker='o')
    # グラフのタイトルと軸ラベルを設定
    plt.title("[" + titleStr + "]" + '末尾' + endNumber + '番の遷移(' + choiceDate + ')')
    plt.xlabel('日にち')
    plt.ylabel('Value')
    plt.xticks(x)
    # 格子線を描く
    plt.grid()
    # グラフの保存
    plt.savefig('graph.png')
    # グラフ画像をDiscordに送信
    file = discord.File('graph.png')
    await message.channel.send(file=file)

  elif re.match(end_pattern, message.content):
    str = (message.content).split('_')
    choiceDate = str[0]
    endNumber = str[1]
    splitDate = (choiceDate).split('-')
    datas = report_generator.end_number_message(choiceDate, endNumber)
    # 結果のリストを解析して、x軸とy軸の値を取得します
    x = [data[0] for data in datas]
    y = [data[1] for data in datas]
    # 以前のグラフを削除
    plt.clf()
    # グラフを作成
    plt.plot(x, y, marker='o')
    # グラフのタイトルと軸ラベルを設定
    plt.title('末尾' + endNumber + '番の遷移(' + choiceDate + ')')
    plt.xlabel('日にち')
    plt.ylabel('Value')
    plt.xticks(x)
    # 格子線を描く
    plt.grid()
    # グラフの保存
    plt.savefig('graph.png')
    # グラフ画像をDiscordに送信
    file = discord.File('graph.png')
    await message.channel.send(file=file)

client.run(TOKEN)

test
test2

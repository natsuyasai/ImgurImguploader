# -*- coding: utf-8 -*-
from imgurpython import ImgurClient
import configparser
import requests
import sys
import pyperclip
import webbrowser

# iniファイル定義
INI_FILE_NAME: str = 'auth.ini'
INI_SECTION_TOKEN: str = 'token'
INI_CLIENT_ID: str = 'client_id'
INI_CLIENT_SECRET: str = 'client_secret'
INI_REFRESH_TOKEN: str = 'refresh_toke'
INI_ACCESS_TOKE: str = 'access_toke'



def main(arg: list):
    # 認証
    client = authenticate()
    # アップロード実行
    while (True):
        img_path = input('Input file path -> ')
        if img_path == 'x':
            break
        img_url = client.upload_from_path(img_path, anon=False)['link']
        pyperclip.copy(img_url)
        print(img_url)




def authenticate():
    # iniファイル読み込み
    config: ConfigParser = configparser.ConfigParser()
    config.read(INI_FILE_NAME)
    client_id: str = config.get(INI_SECTION_TOKEN, INI_CLIENT_ID)
    client_secret: str = config.get(INI_SECTION_TOKEN, INI_CLIENT_SECRET)
    # クライアント生成
    if(config.has_option(INI_SECTION_TOKEN, INI_REFRESH_TOKEN)):
        # 既にトークン取得済みならそれを使用する
        refresh_toke: str = config.get(INI_SECTION_TOKEN, INI_REFRESH_TOKEN)
        access_toke: str = config.get(INI_SECTION_TOKEN, INI_ACCESS_TOKE)
        client = ImgurClient(client_id, client_secret,
                             access_toke, refresh_toke)
    else:
        client = ImgurClient(client_id, client_secret)
        # 認証
        authorization_url = client.get_auth_url('pin')
        webbrowser.open(authorization_url)
        print("Go to the following URL: {0}".format(authorization_url))
        pin = input("Enter pin code: ")
        credentials = client.authorize(pin, 'pin')
        client.set_user_auth(credentials['access_token'],
                             credentials['refresh_token'])
        refresh_toke = credentials['refresh_token']
        access_toke = credentials['access_token']
        # iniファイル書き出し
        config.set(INI_SECTION_TOKEN, 'refresh_toke', refresh_toke)
        config.set(INI_SECTION_TOKEN, 'access_toke', access_toke)
        with open(INI_FILE_NAME, 'w') as inifile:
            config.write(inifile)
    return client

if __name__ == "__main__":
    main(sys.argv)

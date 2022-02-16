# Notion Test

https://scrapbox.io/ci7lus/Notion(%E9%9D%9E%E5%85%AC%E9%96%8B)API%E3%81%A7%E7%94%BB%E5%83%8F%E3%82%92%E3%82%A2%E3%83%83%E3%83%97%E3%83%AD%E3%83%BC%E3%83%89%E3%81%99%E3%82%8B

を参考に Notion をいじってみる。


## 準備

### pipenv

[pipenv](https://pipenv-ja.readthedocs.io/ja/translate-ja/) を使用しています。

```sh
pip install pipenv
```

を事前におこなっておくこと。

### .env

```sh
cp default.env .env
```

をおこなったあと、 `.env` の設定をおこなう。

Notion の token_v2 の取得方法はこちら参照: https://www.notion.so/How-to-get-your-token-d7a3421b851f406380fb9ff429cd5d47


## 実行

```sh
pipenv shell
```

を立ち上げて

```sh
pipenv install
```

をおこないます。


### esa にアップロードされた画像を Notion に上げ直し

```sh
python esa-image-to-notion 1234567890abcdef1234567890abcdef
```

この実行時に出力される esa_notion_mapping 変数の中身を  
`mapping.txt` として保存します。次の工程で使います。

### リンクを esa から Notion のものに変換

トップディレクトリに `mapping.txt` を先に用意しておきます。

```sh
python esa-link-to-notion 1234567890abcdef1234567890abcdef
```

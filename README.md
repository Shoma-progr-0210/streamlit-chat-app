# Chat APP with Streamlit

## これはなに？

対話型AIチャットアプリです。  

## 環境構築

対話型AIの使用のため、アカウントが必要です。
現在は以下のAIに対応しています。

- [OpenAI ChatGPT](https://openai.com/chatgpt)
- [Google Bard](https://bard.google.com/)

※Google Bardはブラウザのクッキーを使用します。


Dockerコンテナを使用するか、同様の環境をローカルに構築してください。  

- Python3.11
- Pythonパッケージ(requirements.txt参照)
- Streamlitがサポートしているブラウザ：[What browsers does Streamlit support?](https://docs.streamlit.io/knowledge-base/using-streamlit/supported-browsers)

### Dockerコンテナを使用する

まず、`openai.env`にChatGPTのAPIキーを記載します。

Dockerコンテナを使用する場合は、以下です。

```bash
docker compose build
docker compose up -d
```

```bash
docker exec -it chatapp bash
```
### APIの認証情報を環境変数に登録

コマンドで適宜登録します。
※Dockerコンテナで`openai.env`を記載した場合は`OPENAI_API_KEY`は登録済みのため不要

```bash
export OPENAI_API_KEY=YOUR_API_KEY
export GOOGLE_BARD_TOKEN=YOUR_TOKEN
```

### アプリの起動

```bash
streamlit run app.py
```

## アプリへのアクセス

ブラウザを使用して[http://localhost:8501](http://localhost:8501)へアクセス

## 注意事項

以下のエラーが出た場合は、Google Bardにシークレットブラウザで再ログインしてからトークンを再取得し、APIの認証情報を環境変数に登録の手順で環境変数を更新してください。

```text
Exception: SNlM0e value not found. Double-check __Secure-1PSID value or pass it as token='xxxxx'.
```

## References

[Deploy Streamlit using Docker](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker)

[Streamlitを使ってChatGPTのようなチャットアプリを簡単に作る](https://zenn.dev/nishijima13/articles/3b1a50b8728261)

[BardをPythonで使う方法](https://note.com/masayuki_abe/n/nf22f8a6b023a)

[Logos list - Google](https://about.google/brand-resource-center/logos-list/)

[logos - OepnAI](https://openai.com/brand#logos)

[dsdanielpark/Bard-API - GitHub](https://github.com/dsdanielpark/Bard-API)

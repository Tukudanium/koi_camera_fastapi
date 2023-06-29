# KOI_CAMERA_FASTAPI

Connect 2022 in Koriyama, with UDC にて郡山市長賞を受賞した「鯉カメラ」の画像変換部分を、FastAPIでリプレースしたもの。

## 概要

「郡山の鯉を知ろう、食べよう、楽しもう」というテーマでの作品。
そもそも鯉に対して興味を抱いていない人は鯉料理に関係したアプリの時点でアクセスしないと思われるので、直接的に鯉料理やお土産品等を前面に出してのPRは無意味と考えた。
そこで、snowのような顔認識での顔差し替えアプリを作成して面白味でユーザーに別方面での利用価値を与えたうえで、アプリ内で郡山の行っている養殖鯉関連のキャンペーンについて宣伝するといったアプローチを試みた。

## 使い方

仮想環境起動

```powershell
env\Scripts\Activate.ps1
```

仮想環境ライブラリコピー

```powershell
pip install -r requirements.txt
```

デバッグ

```powershell
uvicorn main:app --reload
```

デバッグ時のswaggerURL

<http://localhost:8000/docs>


```html
<input type="file">
```

などで取得した画像ファイルをPOSTで送信することで、変換された画像のbase64文字列が返される。  
base64からの変換も一応実装しているが、文字列が長すぎて途中で切れてしまうので対策を考え中。

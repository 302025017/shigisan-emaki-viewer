# 信貴山縁起絵巻 鑑賞支援Webアプリケーション
## プレゼンテーション用 技術解説資料

---

## 📋 目次

1. [システム全体概要](#1-システム全体概要)
2. [技術アーキテクチャ](#2-技術アーキテクチャ)
3. [ファイル構成と役割](#3-ファイル構成と役割)
4. [データ構造の詳細](#4-データ構造の詳細)
5. [バックエンド（Python/Flask）の仕組み](#5-バックエンドpythonflaskの仕組み)
6. [フロントエンド（HTML/CSS/JavaScript）の仕組み](#6-フロントエンドhtmlcssjavascriptの仕組み)
7. [動作フロー（ユーザーの行動とシステムの反応）](#7-動作フロー)
8. [主要な機能の実装詳細](#8-主要な機能の実装詳細)

---

## 1. システム全体概要

### 📌 このアプリケーションの目的

国立国会図書館で公開されている『信貴山縁起絵巻』という古い絵巻物を、初心者が学習するためのWebアプリケーションです。

**通常の方法：**
```
絵巻物を眺める → わからない → 本を読む → また わからない...
```

**このアプリケーション：**
```
疑問に思ったことを質問 → システムが説明 → スムーズに理解できる
```

### 🎯 システムの特徴

| 特徴 | 説明 |
|------|------|
| **シンプル** | 質問と応答だけに徹底 |
| **完全オフライン** | インターネット接続不要 |
| **誰でも使える** | 初学者向けの親しみやすいUI |
| **正確** | AI任せではなく、確実な情報を表示 |

### 👥 ターゲットユーザー

- 美術館や博物館の学習者
- 授業で古美術を学ぶ学生
- 文化財に興味がある初心者

---

## 2. 技術アーキテクチャ

### 🏗️ システムの構成図

```
┌─────────────────────────────────────────────────────┐
│                    Webブラウザ                        │
│  ┌──────────────────────────────────────────────┐  │
│  │    HTML（見た目）+ CSS（デザイン）             │  │
│  │    + JavaScript（動作）                      │  │
│  └──────────────────────────────────────────────┘  │
└────────────────┬────────────────────────────────────┘
                 │
         HTTP通信（JSON形式）
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│           Flask（Webサーバー）                        │
│  ┌──────────────────────────────────────────────┐  │
│  │ 1. ブラウザからの要求を受け取る               │  │
│  │ 2. データを処理する                          │  │
│  │ 3. 応答をブラウザに返す                      │  │
│  └──────────────────────────────────────────────┘  │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
    ┌────────────────────────────┐
    │  場面データ（Python辞書）    │
    │  ・scene_06-08             │
    │  ・scene_17-20             │
    │  ・scene_20-21             │
    └────────────────────────────┘
```

### 🔄 通信の仕組み（簡潔版）

```
ユーザーがボタンをクリック
       ▼
JavaScriptが要求を作成
       ▼
Webサーバー（Flask）に送信
       ▼
Flaskが処理（データベース検索など）
       ▼
結果をJSON形式で返す
       ▼
JavaScriptが結果を受け取る
       ▼
HTMLを動的に更新して画面に表示
```

---

## 3. ファイル構成と役割

### 📁 プロジェクトの全体構成

```
Mirubun/                          ← プロジェクトフォルダ
│
├── Chat_bot.py                   ← ⭐ メインプログラム（Flaskサーバー）
├── requirements.txt              ← 必要なPythonパッケージ一覧
├── README.md                     ← 使い方ドキュメント
│
└── templates/                    ← Webページ用フォルダ
    └── index.html                ← ⭐ Webページ（HTML/CSS/JavaScript）
```

### 各ファイルの詳細役割

#### 📄 Chat_bot.py（約200行）

**役割：** アプリケーションの脳（ビジネスロジック）

```python
# 例：この中に書かれていること
✓ 3つの場面データを定義
✓ ユーザーの質問を受け取る
✓ データベース（辞書）から答えを探す
✓ 答えをブラウザに返す
✓ 場面切り替え時に履歴をリセット
```

**使用言語：** Python

#### 🌐 templates/index.html（約500行）

**役割：** 画面（ユーザーが見て操作する部分）

```html
構成：
1. <head>...</head>       ← ページの設定
2. <style>...</style>     ← デザイン（CSS）
3. <body>...</body>       ← 画面の内容
4. <script>...</script>   ← 動作（JavaScript）
```

**使用言語：** HTML5（構造）+ CSS3（デザイン）+ JavaScript（動作）

#### 📋 requirements.txt（2行）

**役割：** 必要な外部ツールのリスト

```
Flask==3.0.0
Werkzeug==3.0.1
```

「このプログラムを動かすには、このバージョンのFlaskが必要ですよ」という指示書

#### 📖 README.md

**役割：** 使い方マニュアル

---

## 4. データ構造の詳細

### 🗂️ 場面データの構成

このアプリケーションは、**Python の辞書（dict）** という データ構造を使ってデータを管理しています。

#### 場面データの階層構造

```
SCENES_DATA
│
├── scene_06-08
│   ├── scene_id: "scene_06-08"
│   ├── title: "信貴山縁起[1] 第6-8コマ"
│   ├── reference_url: "https://dl.ndl.go.jp/pid/2574276/1/6"
│   └── questions: {
│       "この場面では一体何が起きているのですか？": "答え1",
│       "なぜ蔵が空を飛んでいるのでしょうか？": "答え2",
│       "このシーンの見どころは何ですか？": "答え3"
│   }
│
├── scene_17-20
│   ├── scene_id: "scene_17-20"
│   ├── title: "信貴山縁起[1] 第17-20コマ"
│   ├── reference_url: "https://dl.ndl.go.jp/pid/2574276/1/17"
│   └── questions: {
│       "ここはどこで、何が起きているのですか？": "答え1",
│       ...
│   }
│
└── scene_20-21
    ├── scene_id: "scene_20-21"
    ├── title: "信貴山縁起[3] 第20-21コマ"
    ├── reference_url: "https://dl.ndl.go.jp/pid/2574278/1/20"
    └── questions: {
        "この巨大な像は何ですか？": "答え1",
        ...
    }
```

### 📝 具体例：信貴山縁起[1] 第6-8コマのデータ

```python
SCENES_DATA = {
    "scene_06-08": {                          ← 場面ID（ユニークキー）
        "scene_id": "scene_06-08",            ← 場面を特定するID
        "title": "信貴山縁起[1] 第6-8コマ",    ← ユーザーに表示する名前
        "reference_url": "https://dl.ndl.go.jp/pid/2574276/1/6",  ← 国立国会図書館のURL
        "questions": {                        ← 質問と答えの辞書
            "この場面では一体何が起きているのですか？": 
                "強欲な長者の**「米蔵（こめぐら）」が、空を飛んで持ち去られている場面**です。\n\n画面の上部に見えるのは蔵の底の部分で、その下にある小さな「鉢（はち）」が、巨大な蔵を支えて空へ運び出しています。下にいる人々は、自分たちの目の前で起きた信じられない光景に驚き、慌てふためいて追いかけているところです。",
            "なぜ蔵が空を飛んでいるのでしょうか？": 
                "僧侶・**命蓮（みょうれん）の「法力（ほうりき）」**によるものです。\n\n信貴山で修行していた命蓮は、ふもとの長者のもとへ「托鉢（たくはつ）」のために魔法の鉢を飛ばしていました。長者はいつもその鉢に米を入れて布施していましたが、ある日、面倒に思った長者が鉢を蔵の中に閉じ込めてしまいます。 すると、怒った（あるいは困った）鉢が蔵をまるごと持ち上げ、命蓮の待つ信貴山の山頂へと飛び去ってしまったのです。",
            "このシーンの見どころは何ですか？": """この場面の最大の見どころは、人々の豊かな表情（面貌表現）と躍動感です。

            
・驚愕の表情: 目を丸くし、口を大きく開けて見上げる人々の一人ひとりが、異なるポーズで驚きを表現しています。

・追いかける人々: 画面右側には、馬に乗って急いで追いかける長者や、それについていく従者たちが描かれています。

・漫画的表現: 現代の日本の漫画のルーツとも言われるほど、キャラクターの感情がダイレクトに伝わる筆致が特徴です。""",
        }
    }
}
```

### 🔍 データ検索の流れ

```
ユーザー入力: "この場面では一体何が起きているのですか？"
       ↓
入力を正規化（空白削除など）
       ↓
SCENES_DATA["scene_06-08"]["questions"] を検索
       ↓
キーが完全一致？
  ├─ YES → 対応する値（答え）を返す
  └─ NO  → 定型文「対応していません」を返す
```

---

## 5. バックエンド（Python/Flask）の仕組み

### 🚀 Flask とは

**Flask** = Pythonで簡単にWebサーバーを作るためのツール

```
      通常のプログラム              Webアプリケーション
          
    実行 → 結果を表示 →終了       常に起動 → リクエスト来る
                                   ↓
                            データ処理 → 応答を返す
                                   ↓
                            また待機...
```

### 📌 Flask の基本的な仕組み

```python
# 1. Flaskを導入
from flask import Flask
app = Flask(__name__)

# 2. ルート（URLと処理の対応）を定義
@app.route("/")                    # "/" にアクセスされたら
def index():
    return "ウェブページを表示"    # この処理を実行

@app.route("/api/ask", methods=["POST"])  # "/api/ask" にPOST送信されたら
def ask_question():
    return "答えを返す"             # この処理を実行

# 3. サーバー起動
if __name__ == "__main__":
    app.run()                       # Webサーバーを起動
```

### 🔧 本アプリケーションの主要な処理

#### 処理1：初期ページ表示

```python
@app.route("/")
def index():
    """初期画面を表示"""
    # 3つの場面リストを作成
    scenes_list = [
        {"scene_id": "scene_06-08", "title": "信貴山縁起[1] 第6-8コマ"},
        {"scene_id": "scene_17-20", "title": "信貴山縁起[1] 第17-20コマ"},
        {"scene_id": "scene_20-21", "title": "信貴山縁起[3] 第20-21コマ"},
    ]
    # HTMLテンプレートを見つけて、データを埋め込んで返す
    return render_template("index.html", scenes=scenes_list)
```

**流れ：**
```
ユーザーがブラウザで http://127.0.0.1:5000 にアクセス
       ↓
Flaskの index() 関数が実行される
       ↓
index.html を探して、場面リストを埋め込む
       ↓
完成したHTMLをブラウザに返す
```

#### 処理2：場面を変更する

```python
@app.route("/api/scene", methods=["POST"])
def change_scene():
    """場面を変更するエンドポイント"""
    # ブラウザから送られてきたデータを取得
    data = request.get_json()
    scene_id = data.get("scene_id")
    
    # その場面が存在するか確認
    if scene_id not in SCENES_DATA:
        return jsonify({"success": False, "error": "不正な場面IDです"}), 400
    
    # 状態を更新（現在の場面を変更、履歴をリセット）
    app_state.set_scene(scene_id)
    scene_data = SCENES_DATA[scene_id]
    
    # ブラウザに結果を JSON 形式で返す
    return jsonify({
        "success": True,
        "scene_id": scene_id,
        "title": scene_data["title"],
        "reference_url": scene_data["reference_url"]
    })
```

**流れ：**
```
ユーザーがドロップダウンで「信貴山縁起[1] 第6-8コマ」を選択
       ↓
JavaScriptが "/api/scene" に POST 送信（scene_id: "scene_06-08"）
       ↓
Flaskの change_scene() 関数が実行
       ↓
SCENES_DATA から "scene_06-08" のデータを取得
       ↓
JSON形式で返す
       ↓
JavaScriptが JSON を受け取って画面を更新
```

#### 処理3：質問に答える

```python
@app.route("/api/ask", methods=["POST"])
def ask_question():
    """質問に応答するエンドポイント"""
    # 場面が選択されているか確認
    if app_state.current_scene_id is None:
        return jsonify({"success": False, "error": "場面が選択されていません"}), 400
    
    # ブラウザから送られた質問を取得
    data = request.get_json()
    user_input = data.get("message", "")
    
    # 入力を正規化（空白削除、改行削除）
    normalized_input = normalize_input(user_input)
    
    # 空の入力は処理しない
    if not normalized_input:
        return jsonify({"success": False, "error": "空の入力は処理されません"}), 400
    
    # ユーザーメッセージを履歴に記録
    app_state.add_message("user", normalized_input)
    
    # 応答を生成（完全一致判定）
    response = get_response(normalized_input, app_state.current_scene_id)
    
    # システムメッセージを履歴に記録
    app_state.add_message("assistant", response)
    
    # 結果を返す
    return jsonify({
        "success": True,
        "user_message": normalized_input,
        "assistant_response": response,
        "chat_history": app_state.get_chat_history()
    })
```

**流れ：**
```
ユーザーが質問を入力して「送信」をクリック
       ↓
JavaScriptが "/api/ask" に POST 送信（message: "質問内容"）
       ↓
Flaskの ask_question() 関数が実行
       ↓
normalize_input() で入力を整形
       ↓
get_response() で対応する答えを検索
       ↓
JSON形式で結果を返す
       ↓
JavaScriptが受け取った答えと質問をチャット表示
```

### 🎯 主要なユーティリティ関数

#### normalize_input（入力を整形）

```python
def normalize_input(user_input):
    """ユーザー入力を正規化（前後の空白削除、改行削除）"""
    normalized = user_input.strip()        # 前後の空白を削除
    normalized = normalized.replace("\n", "").replace("\r", "")  # 改行を削除
    return normalized
```

**例：**
```
入力: "  この場面では一体何が起きているのですか？  \n"
       ↓
出力: "この場面では一体何が起きているのですか？"
```

#### get_response（質問に答える）

```python
def get_response(normalized_input, scene_id):
    """入力に対する応答を取得（完全一致判定）"""
    if scene_id not in SCENES_DATA:
        return None
    
    # 現在の場面の質問リストを取得
    scene_questions = SCENES_DATA[scene_id]["questions"]
    
    # キーの完全一致を確認
    if normalized_input in scene_questions:
        return scene_questions[normalized_input]
    
    # 一致しない場合は定型文を返す
    return "申し訳ありません。\nこの質問には現在対応していません。"
```

**例：**
```
入力: "この場面では一体何が起きているのですか？"
場面: "scene_06-08"
       ↓
scene_06-08 の questions を検索
       ↓
完全一致する！
       ↓
対応する答え: "強欲な長者の「米蔵（こめぐら）」が、空を飛んで持ち去られている場面です..."
```

### 💾 AppState（状態管理クラス）

```python
class AppState:
    def __init__(self):
        self.current_scene_id = None      # 現在選択中の場面ID
        self.chat_history = []            # 対話履歴
    
    def set_scene(self, scene_id):
        """場面を変更し、対話履歴を初期化"""
        self.current_scene_id = scene_id
        self.chat_history = []            # ← 重要：場面変更で履歴をリセット
    
    def add_message(self, role, content):
        """対話履歴にメッセージを追加"""
        self.chat_history.append({"role": role, "content": content})
    
    def get_chat_history(self):
        """対話履歴を取得"""
        return self.chat_history
```

**役割：**
- アプリケーション全体の状態（今どの場面を見ているか）を記憶
- ユーザーとの対話をすべて記録

---

## 6. フロントエンド（HTML/CSS/JavaScript）の仕組み

### 🎨 HTML5（構造）

HTMLはWebページの「骨組み」を定義します。

```html
<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="UTF-8">
    <title>信貴山縁起絵巻 鑑賞支援システム</title>
  </head>
  <body>
    <header><h1>タイトル</h1></header>
    <div class="scene-selector">
      <select id="scene-select">
        <option value="">-- 場面を選択 --</option>
                <option value="scene_06-08">信貴山縁起[1] 第6-8コマ</option>
                <option value="scene_17-20">信貴山縁起[1] 第17-20コマ</option>
                <option value="scene_20-21">信貴山縁起[3] 第20-21コマ</option>
      </select>
    </div>
    <div class="chat-container">
      <div id="chat-messages">チャット表示エリア</div>
      <input id="user-input" placeholder="質問を入力...">
      <button id="send-button">送信</button>
    </div>
  </body>
</html>
```

**主な要素：**
- `<select>` : ドロップダウンメニュー（場面選択）
- `<div id="chat-messages">` : チャット表示エリア
- `<input>` : テキスト入力欄
- `<button>` : 送信ボタン

### 🎭 CSS3（見た目・デザイン）

CSSはHTMLの要素をどのように見せるかを定義します。

```css
/* 例1：ボタンのスタイル */
.chat-input-area button {
    padding: 10px 20px;            /* 内側の余白 */
    background-color: #3498db;     /* 背景色（青） */
    color: white;                  /* 文字色（白） */
    border: none;                  /* 枠線なし */
    border-radius: 4px;            /* 角を丸くする */
    cursor: pointer;               /* マウスカーソルをポインタに */
}

/* 例2：ボタンをホバーしたときのスタイル */
.chat-input-area button:hover:not(:disabled) {
    background-color: #2980b9;     /* 濃い青に変わる */
}

/* 例3：無効化されたボタン */
.chat-input-area button:disabled {
    background-color: #95a5a6;     /* グレーになる */
    cursor: not-allowed;           /* マウスカーソルを禁止に */
}
```

**デザイン上の工夫：**
- チャットの背景色を変えて視認性向上（ユーザー：青、システム：グレー）
- ボタンをホバーすると色が変わるフィードバック
- 無効な状態では見た目と動作で「使えない」ことを表現
- レスポンシブデザイン（スマートフォンでも見やすく）

### ⚙️ JavaScript（動作・ロジック）

JavaScriptはユーザーの操作に応じて画面を動的に変更します。

#### イベントリスナー（ユーザー操作を待機）

```javascript
// 場面選択ドロップダウンが変更されたら
sceneSelect.addEventListener("change", handleSceneChange);

// 送信ボタンがクリックされたら
sendButton.addEventListener("click", handleSendMessage);

// テキスト入力欄でEnterキーが押されたら
userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter" && !sendButton.disabled) {
        handleSendMessage();
    }
});
```

#### 場面変更の処理（async/await）

```javascript
async function handleSceneChange() {
    const sceneId = sceneSelect.value;
    
    // 場面が非選択状態
    if (!sceneId) {
        currentSceneId = null;
        userInput.disabled = true;      // 入力を無効化
        sendButton.disabled = true;     // ボタンを無効化
        sceneInfo.style.display = "none";
        // プレースホルダーテキストを表示
        chatMessages.innerHTML = `<div class="placeholder-message">
            場面を選択すると、質問ができるようになります
        </div>`;
        return;
    }
    
    try {
        // Flaskサーバーに PUT/POST リクエストを送信
        const response = await fetch("/api/scene", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ scene_id: sceneId }),
        });
        
        // サーバーから JSON 形式で結果を受け取る
        const data = await response.json();
        
        if (data.success) {
            currentSceneId = data.scene_id;
            sceneTitle.textContent = data.title;
            referenceUrl.href = data.reference_url;
            
            // 入力を有効化
            userInput.disabled = false;
            sendButton.disabled = false;
            
            // チャットをリセット
            chatMessages.innerHTML = `<div class="placeholder-message">
                ${data.title}について質問してください
            </div>`;
        }
    } catch (error) {
        console.error("エラー:", error);
        showError("場面の読み込みに失敗しました");
    }
}
```

**流れの詳細：**
```
1. ユーザーが「信貴山縁起[1] 第6-8コマ」を選択
   ↓
2. handleSceneChange() 関数が実行
   ↓
3. サーバーに非同期通信（fetch）でリクエスト送信
   ↓
4. await で結果が返るまで待機
   ↓
5. JSON形式の結果を受け取る
   ↓
6. 画面の状態を更新（ボタン有効化、テキスト更新など）
```

#### 質問送信の処理

```javascript
async function handleSendMessage() {
    const message = userInput.value.trim();
    
    // 空の入力チェック
    if (!message) return;
    
    // 場面が選択されているか確認
    if (!currentSceneId) {
        showError("場面を選択してください");
        return;
    }
    
    try {
        // 入力フィールドをクリア、ボタンを無効化
        userInput.value = "";
        sendButton.disabled = true;
        userInput.disabled = true;
        
        // サーバーに質問を送信
        const response = await fetch("/api/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: message }),
        });
        
        // 結果を受け取る
        const data = await response.json();
        
        if (data.success) {
            // チャット履歴を表示
            displayChatHistory(data.chat_history);
        }
    } catch (error) {
        console.error("エラー:", error);
        showError("質問の処理に失敗しました");
    } finally {
        // ボタンと入力欄を復帰
        userInput.disabled = false;
        sendButton.disabled = false;
        userInput.focus();  // 次の入力のためにフォーカス
    }
}
```

#### チャット履歴の表示

```javascript
function displayChatHistory(history) {
    chatMessages.innerHTML = "";  // チャット欄をクリア
    
    // 履歴の各メッセージをループで処理
    history.forEach((message) => {
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${message.role}`;  // "user" or "assistant"
        
        const contentDiv = document.createElement("div");
        contentDiv.className = "message-content";
        contentDiv.textContent = message.content;
        
        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
    });
    
    // スクロールを最下部に移動（最新メッセージを見えるようにする）
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
```

**視覚的な工夫：**
```
ユーザーメッセージ  ← 右側に青で表示
←左側にグレーで表示  システムメッセージ
```

---

## 7. 動作フロー

### 📊 完全なユーザーインタラクション図

```
【ステップ1】ページを開く
┌─────────────────────────────────────────┐
│ ユーザー: ブラウザで http://127.0.0.1:5000 を開く
└────────────────┬────────────────────────┘
                 │
                 ▼
        Flask: index() 関数実行
                 │
                 ▼
    ┌─────────────────────────────────┐
    │ HTML（ドロップダウンなし状態）   │
    │ 入力欄：無効化                   │
    │ 送信ボタン：無効化               │
    └─────────────────────────────────┘
                 │
                 ▼
    【プレースホルダーテキスト】
    「場面を選択すると、質問ができるようになります」
```

```
【ステップ2】場面を選択
┌─────────────────────────────────────────┐
│ ユーザー: ドロップダウンから「信貴山縁起[1] 第17-20コマ」を選択
└────────────────┬────────────────────────┘
                 │
                 ▼
    JavaScript: handleSceneChange() 実行
                 │
    ┌────────────┴────────────┐
    ▼                         ▼
    Flaskに              {'scene_id': 'scene_17-20'}
  POST送信             を JSON形式で送信
                       
                       ▼
    Flask: change_scene() 関数実行
    
    ┌─────────────────────────────────┐
        │ 1. SCENES_DATA["scene_17-20"]を検索 │
    │ 2. 状態を更新                    │
        │    - current_scene_id = scene_17-20 │
    │    - chat_history = []           │
    │ 3. データを返す（質問リスト含む） │
    └─────────────────────────────────┘
                 │
                 ▼
    {
      "success": true,
            "scene_id": "scene_17-20",
            "title": "信貴山縁起[1] 第17-20コマ",
      "reference_url": "https://...",
      "questions": {
                "ここはどこで、何が起きているのですか？": "...",
                "右側に立っている数珠を持った人物は誰ですか？": "...",
        ...
      }
    }
    
    を JSON形式で返す
                 │
                 ▼
    JavaScript: 結果を受け取る
                 │
    ┌─────────────────────────────────┐
    │ 1. プルダウンを質問で埋める      │
    │ 2. プルダウンを有効化            │
    │ 3. 送信ボタンを有効化            │
    │ 4. 場面情報を表示                │
    │ 5. プレースホルダーを更新        │
    │    「信貴山縁起[1] 第17-20コマについて質問を選択してください」
    └─────────────────────────────────┘
                 │
                 ▼
    ┌─────────────────────────────────┐
    │ ✓ ドロップダウン：「信貴山縁起[1] 第17-20コマ」    │
    │ ✓ 質問選択欄：質問リストが表示   │
    │ ✓ 参照URL表示                     │
    │ ✓ 送信ボタン：使用可能            │
    └─────────────────────────────────┘
```

```
【ステップ3】質問を選択して送信
┌─────────────────────────────────────────┐
│ ユーザー: 質問プルダウンから
│ 「ここはどこで、何が起きているのですか？」
│ を選択して「送信」ボタンをクリック
└────────────────┬────────────────────────┘
                 │
                 ▼
    JavaScript: handleSendMessage() 実行
                 │
    ┌──────────┬──────────────────────┐
    │          │                      │
    ▼          ▼                      ▼
 プルダウン   ボタン              Flaskに POST送信
 をリセット   を無効化
              
                                {
                                  'question': 'その質問',
                                                                    'scene_id': 'scene_17-20'
                                }
                                を JSON形式で送信
                                 │
                                 ▼
                Flask: ask_question() 関数実行
                
                ┌─────────────────────────────────┐
                │ 1. scene_idとquestionを受け取る  │
                │                               │
                │ 2. SCENES_DATA[scene_id]から    │
                │    questions[question]を検索   │
                │    ↓ 完全一致で高速取得        │
                │                               │
                │ 3. チャット履歴に追加          │
                │    - ユーザー質問              │
                │    - システム回答              │
                │                               │
                │ 4. データを返す                │
                └─────────────────────────────────┘
                 │
                 ▼
                JSON形式で返す：
                {
                  "success": true,
                  "question": "質問...",
                  "answer": "答え..."
                }
                 │
                 ▼
    JavaScript: 結果を受け取る
                 │
    1. ユーザー質問をチャットに追加
    2. システム回答をチャットに追加
    3. スクロールを最下部に移動
                 │
                 ▼
    ┌─────────────────────────────────┐
    │ ユーザー: 「この場面では一体何が...」（青） │
    │ システム: 「画面の上部に見えるのは...」（グレー） │
    └─────────────────────────────────┘
```

### 🎬 複数回の質問のシーケンス

```
1回目の質問
  ユーザー: 「質問1」
  システム: 「答え1」
  ↓
  チャット表示: 質問1 → 答え1

2回目の質問
  ユーザー: 「質問2」
  ↓ 新しいメッセージがさらに追加
  ↓
  チャット表示: 質問1 → 答え1 → 質問2 → 答え2

3回目の質問
  ユーザー: 「質問3」
  ↓
  チャット表示: 質問1 → 答え1 → 質問2 → 答え2 → 質問3 → 答え3
```

### 🔄 場面を変更したとき

```
信貴山縁起[1] 第17-20コマで質問を重ねた後...
チャット表示:
  質問1 → 答え1
  質問2 → 答え2

ユーザー: 「信貴山縁起[3] 第20-21コマ」に切り替え
  ↓
Flask: app_state.set_scene("scene_20-21") 実行
  ↓
    current_scene_id = "scene_20-21"
  chat_history = []  ← リセット！
  ↓
JavaScript: 画面を更新
  ↓
プレースホルダー: 「信貴山縁起[3] 第20-21コマについて質問を選択してください」
質問プルダウン: 信貴山縁起[3] 第20-21コマの質問リストで更新
  ↓
新しく質問
    question: 「信貴山縁起[3] 第20-21コマの質問」
    answer: 「信貴山縁起[3] 第20-21コマの答え」
```

---

## 8. 主要な機能の実装詳細

### ✨ 機能1：完全一致判定

**実装コード：**

```python
def get_response(normalized_input, scene_id):
    """入力に対する応答を取得（完全一致判定）"""
    if scene_id not in SCENES_DATA:
        return None
    
    scene_questions = SCENES_DATA[scene_id]["questions"]
    
    # キーの完全一致を確認 ← ここが重要
    if normalized_input in scene_questions:
        return scene_questions[normalized_input]
    
    # 一致しない場合は定型文を返す
    return "申し訳ありません。\nこの質問には現在対応していません。"
```

**例1：完全一致する場合**

```
登録されている質問キー:
    "この場面では一体何が起きているのですか？"

ユーザー入力:
    "この場面では一体何が起きているのですか？"

正規化後:
    "この場面では一体何が起きているのですか？"

結果:
  キー存在 → 対応する答えを返す ✓
```

**例2：一致しない場合**

```
ユーザー入力:
    "この場面について教えてください"

正規化後:
    "この場面について教えてください"

登録されているキー一覧で検索:
    ✗ "この場面では一体何が起きているのですか？"
    ✗ "なぜ蔵が空を飛んでいるのでしょうか？"
    ✗ "このシーンの見どころは何ですか？"

結果:
  キー未存在 → 定型文を返す ✓
```

**なぜ完全一致にしたか？**

1. **予測可能** - ユーザーが何を入力しても、システムの動作が明確
2. **正確** - 曖昧な自然言語処理をしない
3. **シンプル** - 実装が簡単で理解しやすい
4. **授業用途に最適** - ランダムな回答がない

### ✨ 機能2：プルダウン選択による質問管理

**変更内容：**
```
【変更前】
ユーザーテキスト入力 → 正規化処理 → キー検索 → 一致/不一致判定 → 応答

【変更後】
ユーザープルダウン選択 → 直接キー確定 → 即座に応答
```

**実装コード（JavaScript側）：**

```javascript
async function handleSceneChange() {
    // 場面選択時に質問リストを取得
    const data = await fetch("/api/scene", {...}).then(r => r.json());
    
    // プルダウンに質問を設定
    userInput.innerHTML = '<option value="">-- 質問を選択してください --</option>';
    Object.keys(data.questions).forEach((question) => {
        const option = document.createElement("option");
        option.value = question;
        option.textContent = question;
        userInput.appendChild(option);
    });
}
```

**実装コード（Python側）：**

```python
@app.route("/api/scene", methods=["POST"])
def change_scene():
    scene_data = SCENES_DATA[scene_id]
    
    return jsonify({
        "success": True,
        "scene_id": scene_id,
        "title": scene_data["title"],
        "reference_url": scene_data["reference_url"],
        "questions": scene_data["questions"]  # ← 質問リスト返送
    })
```

**メリット：**
```
✓ ユーザーが確実に有効な質問を選択
✓ テキスト入力による曖昧さなし
✓ 自動補完や形態素解析不要
✓ 処理が高速（辞書検索）
✓ バグが少ない（厳密な選択）
```

### ✨ 機能3：状態管理（場面切り替え時に履歴をリセット）

**実装コード：**

```python
class AppState:
    def set_scene(self, scene_id):
        """場面を変更し、対話履歴を初期化"""
        self.current_scene_id = scene_id
        self.chat_history = []  # ← ここが重要
```

**仕様の理由：**

```
シナリオ：ユーザーが場面を切り替えた

【信貴山縁起[1] 第17-20コマでの会話】
Q: 「ここはどこで、何が起きているのですか？」
A: 「信貴山の山頂にある命蓮の庵で、長者たちが蔵を返してほしいと懇願しています。」

Q: 「右側に立っている数珠を持った人物は誰ですか？」
A: 「主人公の僧侶、命蓮です。」

【ユーザーが信貴山縁起[3] 第20-21コマに切り替え】

【信貴山縁起[3] 第20-21コマでの会話】
← 信貴山縁起[1] 第17-20コマの会話は全削除される
← 新しく信貴山縁起[3] 第20-21コマについての対話を開始

理由：
- ユーザーの関心が変わった
- 混乱を避けるため
- UI上もリセットして明確さを保つ
```

### ✨ 機能4：UIの有効/無効化

**実装コード（JavaScript側）：**

```javascript
async function handleSceneChange() {
    const sceneId = sceneSelect.value;
    
    if (!sceneId) {
        // 場面未選択時は無効化
        userInput.disabled = true;
        sendButton.disabled = true;
    } else {
        // 場面選択後は有効化
        userInput.disabled = false;
        sendButton.disabled = false;
    }
}

async function handleSendMessage() {
    if (!currentSceneId) {
        // 場面が選択されていないなら処理を中止
        showError("場面を選択してください");
        return;
    }
    // ...処理...
}
```

**視覚的な表現：**

```
【場面未選択時】
┌─────────────────┐
│ 質問欄：グレー   │  ← クリック不可、選択不可
│ ボタン：グレー   │  ← クリック不可
└─────────────────┘

【場面選択後】
┌─────────────────┐
│ 質問欄：白       │  ← クリック可、選択可
│ ボタン：青       │  ← クリック可
└─────────────────┘
```

---

## 📊 技術スタック一覧表

| レイヤー | 技術 | 役割 | 言語 |
|---------|------|------|------|
| **フロントエンド** | HTML5 | ページ構造 | HTML |
| | CSS3 | デザイン・レイアウト | CSS |
| | JavaScript | インタラクション | JavaScript |
| **バックエンド** | Flask | Webサーバー | Python |
| **データ** | Python dict | データ管理 | Python |
| **通信** | JSON | データフォーマット | - |
| **HTTP** | RESTful API | 通信プロトコル | - |

---

## 🎓 このシステムから学べる事柄

### 初級レベル

- ✓ HTMLの基本構造
- ✓ CSSによるスタイリング
- ✓ JavaScriptの基本（DOM操作、イベントリスナー）
- ✓ Pythonの基本（関数、辞書、クラス）

### 中級レベル

- ✓ REST API の基本
- ✓ 非同期通信（async/await）
- ✓ JSON データ形式
- ✓ Flask フレームワーク
- ✓ クライアント・サーバーアーキテクチャ

### 上級レベル

- ✓ 状態管理の設計
- ✓ エラーハンドリング
- ✓ UI/UX デザイン原則
- ✓ レスポンシブデザイン

---

## 🔍 コードの特徴

### シンプルさ

- 不要な複雑さを排除
- 1つの関数は1つの役割に限定
- 変数名は日本語で意図を明確に

### 読みやすさ

- コメントを適切に配置
- インデント統一
- 関数名で処理内容を表現

### 保守性

- 場面データは分離（SCENES_DATA）
- 状態管理をクラス化（AppState）
- ビジネスロジックとUI分離

---

## 🚀 本アプリケーションの拡張可能性

このアプリケーションを基盤に、以下のような拡張が可能です：

### 短期拡張

- 場面データを追加（SCENES_DATA に新しい scene_XX を追加）
- 質問・回答を追加
- 背景色などのテーマカラー変更

### 中期拡張

- ユーザーのスコア管理
- 学習進度の記録
- 難易度設定

### 長期拡張

- データベース連携（SQLite など）
- ユーザー認証機能
- 学習統計ダッシュボード

---

## 📝 まとめ

このアプリケーションは：

1. **シンプルな設計** で初学者にも理解しやすい
2. **完全オフライン** で安全で確実な動作
3. **プレゼンテーション対応** で学習効果を最大化
4. **拡張可能** な構造で将来の改良も容易
5. **実践的** なWeb開発技術を学べる教材

として設計・実装されています。

---

ご質問やプレゼンテーション時のご不明な点があればお知らせください！

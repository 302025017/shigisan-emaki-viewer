"""
信貴山縁起絵巻 鑑賞支援Webアプリケーション
国立国会図書館デジタルコレクションの作品を鑑賞する学習者向けの質問応答システム
"""

from flask import Flask, render_template, request, jsonify
import os
import json

app = Flask(__name__)

# ========================
# 場面データ定義
# ========================
SCENES_DATA = {
    "scene_07": {
        "scene_id": "scene_07",
        "title": "信貴山縁起[1] 第7コマ",
        "reference_url": "https://dl.ndl.go.jp/pid/2574276/1/7",
        "questions": {
            "この場面では一体何が起きているのですか？": "強欲な長者の**「米蔵（こめぐら）」が、空を飛んで持ち去られている場面**です。\n\n画面の上部に見えるのは蔵の底の部分で、その下にある小さな「鉢（はち）」が、巨大な蔵を支えて空へ運び出しています。下にいる人々は、自分たちの目の前で起きた信じられない光景に驚き、慌てふためいて追いかけているところです。",
            "なぜ蔵が空を飛んでいるのでしょうか？": "僧侶・**命蓮（みょうれん）の「法力（ほうりき）」**によるものです。\n\n信貴山で修行していた命蓮は、ふもとの長者のもとへ「托鉢（たくはつ）」のために魔法の鉢を飛ばしていました。長者はいつもその鉢に米を入れて布施していましたが、ある日、面倒に思った長者が鉢を蔵の中に閉じ込めてしまいます。 すると、怒った（あるいは困った）鉢が蔵をまるごと持ち上げ、命蓮の待つ信貴山の山頂へと飛び去ってしまったのです。",
            "このシーンの見どころは何ですか？": """この場面の最大の見どころは、人々の豊かな表情（面貌表現）と躍動感です。

            
・驚愕の表情: 目を丸くし、口を大きく開けて見上げる人々の一人ひとりが、異なるポーズで驚きを表現しています。

・追いかける人々: 画面右側には、馬に乗って急いで追いかける長者や、それについていく従者たちが描かれています。

・漫画的表現: 現代の日本の漫画のルーツとも言われるほど、キャラクターの感情がダイレクトに伝わる筆致が特徴です。""",
        }
    },
    "scene_17": {
        "scene_id": "scene_17",
        "title": "信貴山縁起[1] 第17コマ",
        "reference_url": "https://dl.ndl.go.jp/pid/2574276/1/17",
        "questions": {
            "ここはどこで、何が起きているのですか？": """信貴山の山頂にある命蓮の庵（いおり）の前です。

ふもとから必死で追いかけてきた長者たちが、ようやく命蓮に追いつき、「どうか蔵を返してください」と泣きながら懇願している場面です。画面左側には、無事に（？）山頂に到着した蔵と、そこからこぼれ出た大量の米俵が描かれています。""",
            "右側に立っている数珠を持った人物は誰ですか？": """この物語の主人公である僧侶、**命蓮（みょうれん）**です。

彼は慌てふためく長者たちを前に、非常に落ち着いた様子で描かれています。超自然的な力（法力）を操る高僧としての威厳と、どこか世俗を越越したような雰囲気が、その立ち姿から伝わってきます。""",
            "鉢の上に乗っている米俵と、そこにいる人は何をしているのですか？": """これは命蓮が長者に**「米を返すための準備」を命じている場面**です。

長者が「蔵を返してほしい」と頼んだのに対し、命蓮は「蔵を返すのは難しいが、中身の米は返してあげよう」と答えます。 そして、**「この鉢の上に米俵を一つ載せなさい」**と指示しました。画像中央では、長者の従者が不思議そうに、あるいは恐る恐る鉢の上の米俵に触れています。この一俵が「リーダー」となって、他の数千俵を連れて空を飛ぶことになるのです。""",
            "画面全体の構成で注目すべきポイントは？": """「静」と「動」の対比、そして人々の心理描写です。

・命蓮の静けさ： 画面右側で泰然と自若に立つ命蓮。

・長者たちの動揺： 地面にひれ伏したり、膝をついたりして必死に頼み込む長者一行。彼らのポーズからは、自分たちの常識が通用しない世界に来てしまった困惑と、すがるような気持ちが読み取れます。

・米俵の存在感： 蔵から溢れんばかりに描かれた米俵は、長者の富の象徴であると同時に、これから起きる「さらなる奇跡（米俵の飛行）」を予感させる装置になっています。""",
        }
    },
    "scene_20": {
        "scene_id": "scene_20",
        "title": "信貴山縁起[3] 第20コマ",
        "reference_url": "https://dl.ndl.go.jp/pid/2574278/1/20",
        "questions": {
            "この巨大な像は何ですか？": """奈良・東大寺の「大仏様（盧舎那仏）」です。

この場面から、物語は命蓮の姉である**「尼公（あまぎみ）」**を主人公としたエピソードに移ります。信濃国（現在の長野県）に住んでいた尼公は、20年も音信不通だった弟の命蓮を探すため、はるばる奈良までやってきました。""",
            "下の方にいる小さな人物は誰ですか？": """弟を探して旅をする、命蓮の姉（尼公）です。

彼女は大仏様の前で、「どうか弟の居場所を教えてください」と一心不乱に祈り続け、そのままお堂にこもります（参籠）。巨大な大仏と、その足元で小さくうずくまる尼公の対比が、彼女の切実な願いと仏様の広大な慈悲を視覚的に表現しています。""",
            "この後、彼女はどうやって弟を見つけるのですか？": """大仏様からのお告げ（夢）によって居場所を知ります。

明け方、尼公の夢に大仏様が現れ、**「ここから未申（ひつじさる：南西）の方角に紫の雲がたなびく山がある。そこを訪ねなさい」**と教えられます。その言葉に従って彼女が向かった先が、命蓮のいる信貴山でした。""",
            "同じ姿の人が複数描かれているのは何故ですか？": """これは「異時同図法（いじどうずほう）」という、日本の絵巻物特有のストーリーテリング技法だからです。

現代の漫画でいうところの**「コマ割り」をせず、一つの背景の中に時間の経過を同時に描き込む手法**です。一人の人物が時間の経過とともに移動し、行動する様子を、パラパラ漫画のように一つの画面の中に並べて表現しています。""",
        }
    }
}

# ========================
# アプリケーション状態管理
# ========================
class AppState:
    def __init__(self):
        self.current_scene_id = None
        self.chat_history = []
    
    def set_scene(self, scene_id):
        """場面を変更し、対話履歴を初期化"""
        self.current_scene_id = scene_id
        self.chat_history = []
    
    def add_message(self, role, content):
        """対話履歴にメッセージを追加"""
        self.chat_history.append({"role": role, "content": content})
    
    def get_chat_history(self):
        """対話履歴を取得"""
        return self.chat_history
    
    def reset_chat(self):
        """対話履歴をリセット"""
        self.chat_history = []


app_state = AppState()

# ========================
# ユーティリティ関数
# ========================
def normalize_input(user_input):
    """ユーザー入力を正規化（前後の空白削除、改行削除）"""
    normalized = user_input.strip()
    normalized = normalized.replace("\n", "").replace("\r", "")
    return normalized


def get_response(normalized_input, scene_id):
    """入力に対する応答を取得（完全一致判定）"""
    if scene_id not in SCENES_DATA:
        return None
    
    scene_questions = SCENES_DATA[scene_id]["questions"]
    
    # キーの完全一致を確認
    if normalized_input in scene_questions:
        return scene_questions[normalized_input]
    
    # 一致しない場合は定型文を返す
    return "申し訳ありません。\nこの質問には現在対応していません。"


# ========================
# ルート定義
# ========================
@app.route("/")
def index():
    """初期画面を表示"""
    # 場面リストを作成
    scenes_list = [
        {"scene_id": "scene_07", "title": "信貴山縁起[1] 第7コマ"},
        {"scene_id": "scene_17", "title": "信貴山縁起[1] 第17コマ"},
        {"scene_id": "scene_20", "title": "信貴山縁起[3] 第20コマ"},
    ]
    return render_template("index.html", scenes=scenes_list)


@app.route("/api/scene", methods=["POST"])
def change_scene():
    """場面を変更するエンドポイント"""
    data = request.get_json()
    scene_id = data.get("scene_id")
    
    if scene_id not in SCENES_DATA:
        return jsonify({"success": False, "error": "不正な場面IDです"}), 400
    
    app_state.set_scene(scene_id)
    scene_data = SCENES_DATA[scene_id]
    
    return jsonify({
        "success": True,
        "scene_id": scene_id,
        "title": scene_data["title"],
        "reference_url": scene_data["reference_url"],
        "questions": scene_data["questions"]
    })


@app.route("/api/ask", methods=["POST"])
def ask_question():
    """質問に応答するエンドポイント"""
    if app_state.current_scene_id is None:
        return jsonify({"success": False, "error": "場面が選択されていません"}), 400
    
    data = request.get_json()
    question = data.get("question", "")
    scene_id = data.get("scene_id")
    
    # 空文字列チェック
    if not question:
        return jsonify({"success": False, "error": "質問を選択してください"}), 400
    
    # シーン情報の取得
    if scene_id not in SCENES_DATA:
        return jsonify({"success": False, "error": "不正な場面IDです"}), 400
    
    scene_data = SCENES_DATA[scene_id]
    
    # 質問に対する回答を検索
    answer = scene_data["questions"].get(question)
    
    if answer is None:
        return jsonify({"success": False, "error": "この質問に対する回答が見つかりません"}), 400
    
    # ユーザーメッセージを履歴に追加
    app_state.add_message("user", question)
    
    # システムメッセージを履歴に追加
    app_state.add_message("assistant", answer)
    
    return jsonify({
        "success": True,
        "question": question,
        "answer": answer
    })


@app.route("/api/chat_history", methods=["GET"])
def get_chat_history():
    """現在の対話履歴を取得"""
    return jsonify({
        "chat_history": app_state.get_chat_history()
    })


# ========================
# エラーハンドリング
# ========================
@app.errorhandler(404)
def not_found_error(error):
    """404エラーハンドリング"""
    return jsonify({"error": "ページが見つかりません"}), 404


@app.errorhandler(500)
def internal_error(error):
    """500エラーハンドリング"""
    return jsonify({"error": "サーバーエラーが発生しました"}), 500


# ========================
# メイン実行
# ========================
if __name__ == "__main__":
    # テンプレートディレクトリの確認
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    if not os.path.exists(template_dir):
        os.makedirs(template_dir)
    
    # Flaskアプリケーション実行
    app.run(debug=True, host="127.0.0.1", port=5000)

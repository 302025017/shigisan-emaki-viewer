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
    "scene_04": {
        "scene_id": "scene_04",
        "title": "第4コマ",
        "reference_url": "https://dl.ndl.go.jp/pid/2574276/1/4",
        "questions": {
            "第4コマではどのような場面が描かれていますか？": "第4コマでは、信貴山の寺で起こった超自然現象の場面が描かれています。",
            "主人公の僧侶は何をしていますか？": "僧侶は信心深く、経を読誦し祈りを捧げています。",
            "この場面の背景にはどのような建造物が見えますか？": "背景には信貴山の寺院建築が描かれています。",
        }
    },
    "scene_07": {
        "scene_id": "scene_07",
        "title": "第7コマ",
        "reference_url": "https://dl.ndl.go.jp/pid/2574276/1/7",
        "questions": {
            "第7コマではどのような出来事が起きていますか？": "第7コマでは、鬼が金銀財宝を運ぶ場面が描かれています。",
            "運ばれている荷物は何ですか？": "鬼が運んでいるのは金銀財宝や宝物です。",
            "この場面では何匹の鬼が登場していますか？": "複数の鬼が協力して財宝を運んでいる場面が描かれています。",
        }
    },
    "scene_17": {
        "scene_id": "scene_17",
        "title": "第17コマ",
        "reference_url": "https://dl.ndl.go.jp/pid/2574276/1/17",
        "questions": {
            "第17コマはどのような場面ですか？": "第17コマは、物語の重要な転換点となる場面を描いています。",
            "この場面での人物の行動は何ですか？": "人物たちが信仰による恩恵を受ける場面が描かれています。",
            "背景に見える景色は何ですか？": "背景には信貴山の周囲の自然景観が広がっています。",
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
        {"scene_id": "scene_04", "title": "第4コマ"},
        {"scene_id": "scene_07", "title": "第7コマ"},
        {"scene_id": "scene_17", "title": "第17コマ"},
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
        "reference_url": scene_data["reference_url"]
    })


@app.route("/api/ask", methods=["POST"])
def ask_question():
    """質問に応答するエンドポイント"""
    if app_state.current_scene_id is None:
        return jsonify({"success": False, "error": "場面が選択されていません"}), 400
    
    data = request.get_json()
    user_input = data.get("message", "")
    
    # 入力の正規化
    normalized_input = normalize_input(user_input)
    
    # 空文字列チェック
    if not normalized_input:
        return jsonify({"success": False, "error": "空の入力は処理されません"}), 400
    
    # ユーザーメッセージを履歴に追加
    app_state.add_message("user", normalized_input)
    
    # 応答を取得
    response = get_response(normalized_input, app_state.current_scene_id)
    
    # システムメッセージを履歴に追加
    app_state.add_message("assistant", response)
    
    return jsonify({
        "success": True,
        "user_message": normalized_input,
        "assistant_response": response,
        "chat_history": app_state.get_chat_history()
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

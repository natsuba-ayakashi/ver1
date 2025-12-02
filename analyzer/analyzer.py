from analyzer.analyzer_ccfolia import analyze_ccfolia
from analyzer.analyzer_old import analyze_old

# 共通設定（両形式で使う）
config = {
    "min_rolls": 2,              # 最低判定数（これ未満は集計に出さない）
    "exclude_tags": [],          # 除外するタグ（セクション名など）
    "show_skill_stats": True,    # 技能別集計を出すか
    "show_unknown_details": True # 不明技能詳細を出すか
}

def analyze_log(file_path):
    """
    ログファイルを読み込み、形式を判定して適切な解析関数に渡す。
    戻り値は dict:
      {
        "summary_text": 出力テキスト,
        "colored_entries": 色付け対象行,
        "character_colors": {表示名:カラーコード},
        "display_names": {正規化名:表示名}
      }
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 形式判定
    if "ccfolia" in content or "ここふぉりあ" in content:
        return analyze_ccfolia(content, config)
    elif "<style>" in content and ".p0" in content:
        # CSSクラス pX が含まれている場合は旧フォーマット形式と判定
        return analyze_old(content, config)
    else:
        raise ValueError("未知のログ形式です")
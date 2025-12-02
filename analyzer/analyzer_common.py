import re
import unicodedata

# キャラ名正規化：全角半角統一＋空白除去
def normalize_name(name: str) -> str:
    if not name:
        return "不明キャラ"
    normalized = unicodedata.normalize("NFKC", name).strip()
    return re.sub(r"\s+", "", normalized)

# 表示用キャラ名：括弧を除去して見やすく
def display_name(name: str) -> str:
    if not name:
        return "不明キャラ"
    normalized = unicodedata.normalize("NFKC", name).strip()
    return re.sub(r"[\(（].*?[\)）]", "", normalized).strip()

# 能力値判定の表記統一
def _normalize_ability_skill(skill: str) -> str:
    m = re.match(r"^(STR|CON|POW|DEX|APP|SIZ|INT|EDU|SAN)([×x*]\d+)?$", skill, re.IGNORECASE)
    if m:
        base = m.group(1).upper()
        mult = m.group(2)
        if mult:
            mult = mult.replace("x", "×").replace("*", "×")
            return base + mult
        return base
    return skill

# 技能名抽出
def extract_skill_name(text: str) -> str:
    # 特例：正気度、アイデア、幸運
    if "正気度" in text:
        return "正気度ロール"
    if "アイデア" in text:
        return "アイデア"
    if "幸運" in text:
        return "幸運"

    # 【技能名】形式
    m = re.search(r"【([^】]+)】", text)
    if m:
        return _normalize_ability_skill(m.group(1).strip())

    # CCB<=xx 技能名形式
    m = re.search(r"CCB<=\s*[\d/+\-*]+(?:\s*[-+*/]\s*\d+)?\s+([^\[\(＞\n\r]{1,})", text)
    if m:
        return _normalize_ability_skill(m.group(1).strip())

    return "不明技能"

# 技能値抽出
def extract_skill_value(text: str) -> int | None:
    m = re.search(r"CCB<=\s*(\d+)", text)
    if m:
        return int(m.group(1))
    return None

# 全角対応で幅揃え
def pad_zen(text: str, width: int) -> str:
    count = sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in text)
    pad = max(0, width - count)
    return text + " " * pad

# 技能別集計出力
def render_skill_stats(name_out, skills, config):
    lines = []
    lines.append(f"\n{name_out} の技能判定：")

    if config.get("show_skill_values", False):
        # 拡張表（技能値／成功／失敗も表示）
        lines.append(
            f"{pad_zen('技能名', 20)}  {pad_zen('技能値', 6)}  {pad_zen('判定数', 8)}  "
            f"{pad_zen('成功', 6)}  {pad_zen('失敗', 6)}  {pad_zen('クリティカル', 12)}  {pad_zen('ファンブル', 10)}"
        )
        lines.append("-"*90)
        for skill, sdata in skills.items():
            # フィルタ設定
            if config.get("only_show_crit_fumble", False):
                if sdata["critical"] == 0 and sdata["fumble"] == 0:
                    continue
            raw_display = next(iter(sdata["raw_names"])) if sdata["raw_names"] else skill
            val = sdata["value"] if sdata["value"] is not None else "-"
            lines.append(
                f"{pad_zen(raw_display, 20)}  "
                f"{str(val).rjust(6)}  "
                f"{str(sdata['total']).rjust(8)}  "
                f"{str(sdata['success']).rjust(6)}  "
                f"{str(sdata['fail']).rjust(6)}  "
                f"{str(sdata['critical']).rjust(12)}  "
                f"{str(sdata['fumble']).rjust(10)}"
            )
    else:
        # 簡易表（以前の仕様）
        lines.append(
            f"{pad_zen('技能名', 20)}  {pad_zen('判定数', 8)}  "
            f"{pad_zen('クリティカル', 12)}  {pad_zen('ファンブル', 10)}"
        )
        lines.append("-"*60)
        for skill, sdata in skills.items():
            if config.get("only_show_crit_fumble", False):
                if sdata["critical"] == 0 and sdata["fumble"] == 0:
                    continue
            raw_display = next(iter(sdata["raw_names"])) if sdata["raw_names"] else skill
            lines.append(
                f"{pad_zen(raw_display, 20)}  "
                f"{str(sdata['total']).rjust(8)}  "
                f"{str(sdata['critical']).rjust(12)}  "
                f"{str(sdata['fumble']).rjust(10)}"
            )

    return lines
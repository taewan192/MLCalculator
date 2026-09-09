import math
import json
import re
import sys
import tkinter as tk
from dataclasses import asdict, dataclass
from pathlib import Path
from tkinter import messagebox, ttk


def get_app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


APP_DIR = get_app_dir()
SAVE_FILE = APP_DIR / "millionlords_player_stats.json"
SLOT_NAMES = {1: "Player Stats"}

SETTINGS_FILE = APP_DIR / "millionlords_settings.json"
LANGUAGE_NAMES = {
    "ko": "한국어", "en": "English", "ja": "日本語", "zh": "中文（简体）",
    "hi": "हिन्दी", "fil": "Filipino", "th": "ไทย", "vi": "Tiếng Việt", "ru": "Русский",
}
LANGUAGE_FONTS = {"ko": "Malgun Gothic", "en": "Segoe UI", "ja": "Yu Gothic",
                  "zh": "Microsoft YaHei", "hi": "Nirmala UI", "fil": "Segoe UI",
                  "th": "Leelawadee UI", "vi": "Segoe UI", "ru": "Segoe UI"}
CURRENT_LANGUAGE = "en"
UI_FONT = LANGUAGE_FONTS[CURRENT_LANGUAGE]
TRANSLATIONS = {
  "ko": {
    "Player Stats": "Player Stats",
    "도시 계산기": "도시 계산기",
    "설정": "설정",
    "언어": "언어",
    "플레이어 능력치 계산 및 저장": "플레이어 능력치 계산 및 저장",
    "장비 + 레벨 + 병력": "장비 + 레벨 + 병력",
    "장비 공격력 (%)": "장비 공격력 (%)",
    "레벨": "레벨",
    "병력": "병력",
    "계산": "계산",
    "저장": "저장",
    "공격력 직접 입력": "공격력 직접 입력",
    "공격력": "공격력",
    "결과": "결과",
    "계산 대기": "계산 대기",
    "저장 완료": "저장 완료",
    "목표 레벨 없음": "목표 레벨 없음",
    "목표 레벨 {level}": "목표 레벨 {level}",
    "목표 레벨 비용": "목표 레벨 비용",
    "보유 골드로 업그레이드": "보유 골드로 업그레이드",
    "도시 수": "도시 수",
    "현재 도시 레벨": "현재 도시 레벨",
    "목표 도시 레벨": "목표 도시 레벨",
    "보유 골드": "보유 골드",
    "초기화": "초기화",
    "도달 도시 레벨": "도달 도시 레벨",
    "총 필요 골드 / 사용 골드": "총 필요 골드 / 사용 골드",
    "남은 골드": "남은 골드",
    "도시당 성벽": "도시당 성벽",
    "도시당 승점": "도시당 승점",
    "총 획득 승점": "총 획득 승점",
    "입력 오류": "입력 오류",
    "공격력 또는 병력은 예: 55G, 42.2T, 1.5P 처럼 입력하세요.": "공격력 또는 병력은 예: 55G, 42.2T, 1.5P 처럼 입력하세요.",
    "공격력을 입력하세요.": "공격력을 입력하세요.",
    "공격력은 0 이상이어야 합니다.": "공격력은 0 이상이어야 합니다.",
    "레벨을 입력하세요.": "레벨을 입력하세요.",
    "레벨은 1 이상이어야 합니다.": "레벨은 1 이상이어야 합니다.",
    "도시 수와 현재 레벨은 1 이상의 정수로 입력하세요.": "도시 수와 현재 레벨은 1 이상의 정수로 입력하세요.",
    "목표 레벨은 현재 레벨보다 높아야 합니다.": "목표 레벨은 현재 레벨보다 높아야 합니다.",
    "보유 골드는 0 이상의 유한한 숫자로 입력하세요.": "보유 골드는 0 이상의 유한한 숫자로 입력하세요.",
    "입력값으로 계산할 수 없습니다. 레벨과 골드를 확인하세요.": "입력값으로 계산할 수 없습니다. 레벨과 골드를 확인하세요.",
    "입력값을 확인하세요: {error}": "입력값을 확인하세요: {error}",
    "유효한 숫자를 입력하세요.": "유효한 숫자를 입력하세요.",
    "파일을 저장하지 못했습니다. 폴더의 쓰기 권한을 확인하세요.": "파일을 저장하지 못했습니다. 폴더의 쓰기 권한을 확인하세요.",
    "언어를 선택하면 모든 화면에 즉시 적용됩니다.": "언어를 선택하면 모든 화면에 즉시 적용됩니다.",
    "언어 설정이 자동으로 저장됩니다.": "언어 설정이 자동으로 저장됩니다.",
    "언어 설정을 저장하지 못했습니다. 이번 실행에만 적용됩니다.": "언어 설정을 저장하지 못했습니다. 이번 실행에만 적용됩니다."
  },
  "en": {
    "Player Stats": "Player Stats",
    "도시 계산기": "City Calculator",
    "설정": "Settings",
    "언어": "Language",
    "플레이어 능력치 계산 및 저장": "Calculate and save player stats",
    "장비 + 레벨 + 병력": "Equipment + Level + Troops",
    "장비 공격력 (%)": "Equipment attack (%)",
    "레벨": "Level",
    "병력": "Troops",
    "계산": "Calculate",
    "저장": "Save",
    "공격력 직접 입력": "Direct attack input",
    "공격력": "Attack power",
    "결과": "Result",
    "계산 대기": "Ready to calculate",
    "저장 완료": "Saved",
    "목표 레벨 없음": "No target level",
    "목표 레벨 {level}": "Target level {level}",
    "목표 레벨 비용": "Cost to target level",
    "보유 골드로 업그레이드": "Upgrade with available gold",
    "도시 수": "Number of cities",
    "현재 도시 레벨": "Current city level",
    "목표 도시 레벨": "Target city level",
    "보유 골드": "Available gold",
    "초기화": "Reset",
    "도달 도시 레벨": "Reached city level",
    "총 필요 골드 / 사용 골드": "Total gold cost",
    "남은 골드": "Remaining gold",
    "도시당 성벽": "Wall per city",
    "도시당 승점": "VP per city",
    "총 획득 승점": "Total VP gained",
    "입력 오류": "Input error",
    "공격력 또는 병력은 예: 55G, 42.2T, 1.5P 처럼 입력하세요.": "Enter attack power or troops like 55G, 42.2T, or 1.5P.",
    "공격력을 입력하세요.": "Enter attack power.",
    "공격력은 0 이상이어야 합니다.": "Attack must be zero or greater.",
    "레벨을 입력하세요.": "Enter a level.",
    "레벨은 1 이상이어야 합니다.": "Level must be at least 1.",
    "도시 수와 현재 레벨은 1 이상의 정수로 입력하세요.": "Enter whole numbers of at least 1 for cities and current level.",
    "목표 레벨은 현재 레벨보다 높아야 합니다.": "Target level must exceed the current level.",
    "보유 골드는 0 이상의 유한한 숫자로 입력하세요.": "Gold must be a finite number of zero or greater.",
    "입력값으로 계산할 수 없습니다. 레벨과 골드를 확인하세요.": "Cannot calculate. Check the level and gold.",
    "입력값을 확인하세요: {error}": "Check your input: {error}",
    "유효한 숫자를 입력하세요.": "Enter a valid number.",
    "파일을 저장하지 못했습니다. 폴더의 쓰기 권한을 확인하세요.": "Could not save the file. Check folder write permissions.",
    "언어를 선택하면 모든 화면에 즉시 적용됩니다.": "Select a language to apply it to all screens immediately.",
    "언어 설정이 자동으로 저장됩니다.": "Your language preference is saved automatically.",
    "언어 설정을 저장하지 못했습니다. 이번 실행에만 적용됩니다.": "Could not save the language. It applies to this session only."
  },
  "ja": {
    "Player Stats": "プレイヤー能力値",
    "도시 계산기": "都市計算機",
    "설정": "設定",
    "언어": "言語",
    "플레이어 능력치 계산 및 저장": "プレイヤー能力値を計算・保存",
    "장비 + 레벨 + 병력": "装備 + レベル + 兵力",
    "장비 공격력 (%)": "装備攻撃力 (%)",
    "레벨": "レベル",
    "병력": "兵力",
    "계산": "計算",
    "저장": "保存",
    "공격력 직접 입력": "攻撃力を直接入力",
    "공격력": "攻撃力",
    "결과": "結果",
    "계산 대기": "計算待ち",
    "저장 완료": "保存しました",
    "목표 레벨 없음": "目標レベルなし",
    "목표 레벨 {level}": "目標レベル {level}",
    "목표 레벨 비용": "目標レベルまでの費用",
    "보유 골드로 업그레이드": "所持ゴールドで強化",
    "도시 수": "都市数",
    "현재 도시 레벨": "現在の都市レベル",
    "목표 도시 레벨": "目標都市レベル",
    "보유 골드": "所持ゴールド",
    "초기화": "リセット",
    "도달 도시 레벨": "到達都市レベル",
    "총 필요 골드 / 사용 골드": "必要・使用ゴールド",
    "남은 골드": "残りゴールド",
    "도시당 성벽": "都市ごとの城壁",
    "도시당 승점": "都市ごとの勝利ポイント",
    "총 획득 승점": "獲得勝利ポイント合計",
    "입력 오류": "入力エラー",
    "공격력 또는 병력은 예: 55G, 42.2T, 1.5P 처럼 입력하세요.": "攻撃力・兵力は 55G、42.2T、1.5P の形式で入力してください。",
    "공격력을 입력하세요.": "攻撃力を入力してください。",
    "공격력은 0 이상이어야 합니다.": "攻撃力は0以上にしてください。",
    "레벨을 입력하세요.": "レベルを入力してください。",
    "레벨은 1 이상이어야 합니다.": "レベルは1以上にしてください。",
    "도시 수와 현재 레벨은 1 이상의 정수로 입력하세요.": "都市数と現在レベルは1以上の整数で入力してください。",
    "목표 레벨은 현재 레벨보다 높아야 합니다.": "目標レベルは現在レベルより高くしてください。",
    "보유 골드는 0 이상의 유한한 숫자로 입력하세요.": "ゴールドは0以上の有限の数値で入力してください。",
    "입력값으로 계산할 수 없습니다. 레벨과 골드를 확인하세요.": "計算できません。レベルとゴールドを確認してください。",
    "입력값을 확인하세요: {error}": "入力を確認してください: {error}",
    "유효한 숫자를 입력하세요.": "有効な数値を入力してください。",
    "파일을 저장하지 못했습니다. 폴더의 쓰기 권한을 확인하세요.": "保存できませんでした。フォルダーの書き込み権限を確認してください。",
    "언어를 선택하면 모든 화면에 즉시 적용됩니다.": "言語を選択するとすべての画面にすぐ反映されます。",
    "언어 설정이 자동으로 저장됩니다.": "言語設定は自動保存されます。",
    "언어 설정을 저장하지 못했습니다. 이번 실행에만 적용됩니다.": "言語設定を保存できませんでした。今回の起動中のみ適用されます。"
  },
  "zh": {
    "Player Stats": "玩家属性",
    "도시 계산기": "城市计算器",
    "설정": "设置",
    "언어": "语言",
    "플레이어 능력치 계산 및 저장": "计算并保存玩家属性",
    "장비 + 레벨 + 병력": "装备 + 等级 + 兵力",
    "장비 공격력 (%)": "装备攻击力 (%)",
    "레벨": "等级",
    "병력": "兵力",
    "계산": "计算",
    "저장": "保存",
    "공격력 직접 입력": "直接输入攻击力",
    "공격력": "攻击力",
    "결과": "结果",
    "계산 대기": "等待计算",
    "저장 완료": "已保存",
    "목표 레벨 없음": "无目标等级",
    "목표 레벨 {level}": "目标等级 {level}",
    "목표 레벨 비용": "目标等级费用",
    "보유 골드로 업그레이드": "使用现有金币升级",
    "도시 수": "城市数量",
    "현재 도시 레벨": "当前城市等级",
    "목표 도시 레벨": "目标城市等级",
    "보유 골드": "现有金币",
    "초기화": "重置",
    "도달 도시 레벨": "可达城市等级",
    "총 필요 골드 / 사용 골드": "所需／使用金币总额",
    "남은 골드": "剩余金币",
    "도시당 성벽": "每座城市城墙",
    "도시당 승점": "每座城市胜利点",
    "총 획득 승점": "获得胜利点总数",
    "입력 오류": "输入错误",
    "공격력 또는 병력은 예: 55G, 42.2T, 1.5P 처럼 입력하세요.": "请按 55G、42.2T、1.5P 的格式输入攻击力或兵力。",
    "공격력을 입력하세요.": "请输入攻击力。",
    "공격력은 0 이상이어야 합니다.": "攻击力必须大于或等于0。",
    "레벨을 입력하세요.": "请输入等级。",
    "레벨은 1 이상이어야 합니다.": "等级必须至少为1。",
    "도시 수와 현재 레벨은 1 이상의 정수로 입력하세요.": "城市数量和当前等级必须是至少为1的整数。",
    "목표 레벨은 현재 레벨보다 높아야 합니다.": "目标等级必须高于当前等级。",
    "보유 골드는 0 이상의 유한한 숫자로 입력하세요.": "金币必须为大于或等于0的有限数值。",
    "입력값으로 계산할 수 없습니다. 레벨과 골드를 확인하세요.": "无法计算，请检查等级和金币。",
    "입력값을 확인하세요: {error}": "请检查输入：{error}",
    "유효한 숫자를 입력하세요.": "请输入有效数字。",
    "파일을 저장하지 못했습니다. 폴더의 쓰기 권한을 확인하세요.": "无法保存文件，请检查文件夹写入权限。",
    "언어를 선택하면 모든 화면에 즉시 적용됩니다.": "选择语言后将立即应用到所有界面。",
    "언어 설정이 자동으로 저장됩니다.": "语言设置会自动保存。",
    "언어 설정을 저장하지 못했습니다. 이번 실행에만 적용됩니다.": "无法保存语言设置，仅在本次运行中生效。"
  },
  "hi": {
    "Player Stats": "खिलाड़ी के आँकड़े",
    "도시 계산기": "शहर कैलकुलेटर",
    "설정": "सेटिंग्स",
    "언어": "भाषा",
    "플레이어 능력치 계산 및 저장": "खिलाड़ी के आँकड़ों की गणना और सेव करें",
    "장비 + 레벨 + 병력": "उपकरण + स्तर + सैनिक",
    "장비 공격력 (%)": "उपकरण की आक्रमण शक्ति (%)",
    "레벨": "स्तर",
    "병력": "सैनिक",
    "계산": "गणना करें",
    "저장": "सेव करें",
    "공격력 직접 입력": "आक्रमण शक्ति सीधे दर्ज करें",
    "공격력": "आक्रमण शक्ति",
    "결과": "परिणाम",
    "계산 대기": "गणना के लिए तैयार",
    "저장 완료": "सेव हो गया",
    "목표 레벨 없음": "कोई लक्ष्य स्तर नहीं",
    "목표 레벨 {level}": "लक्ष्य स्तर {level}",
    "목표 레벨 비용": "लक्ष्य स्तर की लागत",
    "보유 골드로 업그레이드": "उपलब्ध सोने से अपग्रेड",
    "도시 수": "शहरों की संख्या",
    "현재 도시 레벨": "शहर का वर्तमान स्तर",
    "목표 도시 레벨": "शहर का लक्ष्य स्तर",
    "보유 골드": "उपलब्ध सोना",
    "초기화": "रीसेट करें",
    "도달 도시 레벨": "प्राप्त शहर स्तर",
    "총 필요 골드 / 사용 골드": "कुल आवश्यक / खर्च सोना",
    "남은 골드": "बचा हुआ सोना",
    "도시당 성벽": "प्रति शहर दीवार",
    "도시당 승점": "प्रति शहर विजय अंक",
    "총 획득 승점": "कुल प्राप्त विजय अंक",
    "입력 오류": "इनपुट त्रुटि",
    "공격력 또는 병력은 예: 55G, 42.2T, 1.5P 처럼 입력하세요.": "आक्रमण शक्ति या सैनिक 55G, 42.2T या 1.5P जैसे दर्ज करें।",
    "공격력을 입력하세요.": "आक्रमण शक्ति दर्ज करें।",
    "공격력은 0 이상이어야 합니다.": "आक्रमण शक्ति शून्य या अधिक होनी चाहिए।",
    "레벨을 입력하세요.": "स्तर दर्ज करें।",
    "레벨은 1 이상이어야 합니다.": "स्तर कम से कम 1 होना चाहिए।",
    "도시 수와 현재 레벨은 1 이상의 정수로 입력하세요.": "शहरों की संख्या और वर्तमान स्तर कम से कम 1 के पूर्णांक होने चाहिए।",
    "목표 레벨은 현재 레벨보다 높아야 합니다.": "लक्ष्य स्तर वर्तमान स्तर से अधिक होना चाहिए।",
    "보유 골드는 0 이상의 유한한 숫자로 입력하세요.": "सोना शून्य या अधिक की सीमित संख्या होनी चाहिए।",
    "입력값으로 계산할 수 없습니다. 레벨과 골드를 확인하세요.": "गणना नहीं हो सकी। स्तर और सोना जाँचें।",
    "입력값을 확인하세요: {error}": "इनपुट जाँचें: {error}",
    "유효한 숫자를 입력하세요.": "मान्य संख्या दर्ज करें।",
    "파일을 저장하지 못했습니다. 폴더의 쓰기 권한을 확인하세요.": "फ़ाइल सेव नहीं हुई। फ़ोल्डर में लिखने की अनुमति जाँचें।",
    "언어를 선택하면 모든 화면에 즉시 적용됩니다.": "भाषा चुनते ही सभी स्क्रीन पर लागू हो जाएगी।",
    "언어 설정이 자동으로 저장됩니다.": "भाषा सेटिंग अपने आप सेव होती है।",
    "언어 설정을 저장하지 못했습니다. 이번 실행에만 적용됩니다.": "भाषा सेव नहीं हुई। यह केवल इस सत्र में लागू होगी।"
  },
  "fil": {
    "Player Stats": "Mga Stat ng Manlalaro",
    "도시 계산기": "Kalkulador ng Lungsod",
    "설정": "Mga Setting",
    "언어": "Wika",
    "플레이어 능력치 계산 및 저장": "Kalkulahin at i-save ang mga stat",
    "장비 + 레벨 + 병력": "Kagamitan + Antas + Hukbo",
    "장비 공격력 (%)": "Atake ng kagamitan (%)",
    "레벨": "Antas",
    "병력": "Hukbo",
    "계산": "Kalkulahin",
    "저장": "I-save",
    "공격력 직접 입력": "Direktang ilagay ang atake",
    "공격력": "Lakas ng atake",
    "결과": "Resulta",
    "계산 대기": "Handa nang magkalkula",
    "저장 완료": "Na-save na",
    "목표 레벨 없음": "Walang target na antas",
    "목표 레벨 {level}": "Target na antas {level}",
    "목표 레벨 비용": "Gastos sa target na antas",
    "보유 골드로 업그레이드": "Mag-upgrade gamit ang ginto",
    "도시 수": "Bilang ng lungsod",
    "현재 도시 레벨": "Kasalukuyang antas ng lungsod",
    "목표 도시 레벨": "Target na antas ng lungsod",
    "보유 골드": "Magagamit na ginto",
    "초기화": "I-reset",
    "도달 도시 레벨": "Naabot na antas ng lungsod",
    "총 필요 골드 / 사용 골드": "Kabuuang gastos sa ginto",
    "남은 골드": "Natitirang ginto",
    "도시당 성벽": "Pader bawat lungsod",
    "도시당 승점": "Puntos ng tagumpay bawat lungsod",
    "총 획득 승점": "Kabuuang puntos na nakuha",
    "입력 오류": "Maling input",
    "공격력 또는 병력은 예: 55G, 42.2T, 1.5P 처럼 입력하세요.": "Ilagay ang atake o hukbo gaya ng 55G, 42.2T, o 1.5P.",
    "공격력을 입력하세요.": "Ilagay ang lakas ng atake.",
    "공격력은 0 이상이어야 합니다.": "Dapat zero o higit pa ang atake.",
    "레벨을 입력하세요.": "Ilagay ang antas.",
    "레벨은 1 이상이어야 합니다.": "Dapat hindi bababa sa 1 ang antas.",
    "도시 수와 현재 레벨은 1 이상의 정수로 입력하세요.": "Dapat buong bilang na 1 o higit pa ang lungsod at kasalukuyang antas.",
    "목표 레벨은 현재 레벨보다 높아야 합니다.": "Dapat mas mataas ang target kaysa sa kasalukuyang antas.",
    "보유 골드는 0 이상의 유한한 숫자로 입력하세요.": "Dapat may hangganan at zero o higit pa ang halaga ng ginto.",
    "입력값으로 계산할 수 없습니다. 레벨과 골드를 확인하세요.": "Hindi makalkula. Suriin ang antas at ginto.",
    "입력값을 확인하세요: {error}": "Suriin ang input: {error}",
    "유효한 숫자를 입력하세요.": "Maglagay ng wastong numero.",
    "파일을 저장하지 못했습니다. 폴더의 쓰기 권한을 확인하세요.": "Hindi na-save ang file. Suriin ang pahintulot sa pagsulat sa folder.",
    "언어를 선택하면 모든 화면에 즉시 적용됩니다.": "Pumili ng wika upang agad itong ilapat sa lahat ng screen.",
    "언어 설정이 자동으로 저장됩니다.": "Awtomatikong nase-save ang napiling wika.",
    "언어 설정을 저장하지 못했습니다. 이번 실행에만 적용됩니다.": "Hindi na-save ang wika. Para lamang ito sa kasalukuyang sesyon."
  },
  "th": {
    "Player Stats": "สถิติผู้เล่น",
    "도시 계산기": "เครื่องคำนวณเมือง",
    "설정": "การตั้งค่า",
    "언어": "ภาษา",
    "플레이어 능력치 계산 및 저장": "คำนวณและบันทึกสถิติผู้เล่น",
    "장비 + 레벨 + 병력": "อุปกรณ์ + ระดับ + กองทัพ",
    "장비 공격력 (%)": "พลังโจมตีจากอุปกรณ์ (%)",
    "레벨": "ระดับ",
    "병력": "กองทัพ",
    "계산": "คำนวณ",
    "저장": "บันทึก",
    "공격력 직접 입력": "ป้อนพลังโจมตีโดยตรง",
    "공격력": "พลังโจมตี",
    "결과": "ผลลัพธ์",
    "계산 대기": "พร้อมคำนวณ",
    "저장 완료": "บันทึกแล้ว",
    "목표 레벨 없음": "ไม่มีระดับเป้าหมาย",
    "목표 레벨 {level}": "ระดับเป้าหมาย {level}",
    "목표 레벨 비용": "ค่าใช้จ่ายถึงระดับเป้าหมาย",
    "보유 골드로 업그레이드": "อัปเกรดด้วยทองที่มี",
    "도시 수": "จำนวนเมือง",
    "현재 도시 레벨": "ระดับเมืองปัจจุบัน",
    "목표 도시 레벨": "ระดับเมืองเป้าหมาย",
    "보유 골드": "ทองที่มี",
    "초기화": "รีเซ็ต",
    "도달 도시 레벨": "ระดับเมืองที่ไปถึง",
    "총 필요 골드 / 사용 골드": "ทองที่ต้องใช้ทั้งหมด",
    "남은 골드": "ทองที่เหลือ",
    "도시당 성벽": "กำแพงต่อเมือง",
    "도시당 승점": "คะแนนชัยชนะต่อเมือง",
    "총 획득 승점": "คะแนนชัยชนะที่ได้รับทั้งหมด",
    "입력 오류": "ข้อมูลไม่ถูกต้อง",
    "공격력 또는 병력은 예: 55G, 42.2T, 1.5P 처럼 입력하세요.": "ป้อนพลังโจมตีหรือกองทัพ เช่น 55G, 42.2T หรือ 1.5P",
    "공격력을 입력하세요.": "กรุณาป้อนพลังโจมตี",
    "공격력은 0 이상이어야 합니다.": "พลังโจมตีต้องไม่ต่ำกว่า 0",
    "레벨을 입력하세요.": "กรุณาป้อนระดับ",
    "레벨은 1 이상이어야 합니다.": "ระดับต้องไม่น้อยกว่า 1",
    "도시 수와 현재 레벨은 1 이상의 정수로 입력하세요.": "จำนวนเมืองและระดับปัจจุบันต้องเป็นจำนวนเต็มตั้งแต่ 1 ขึ้นไป",
    "목표 레벨은 현재 레벨보다 높아야 합니다.": "ระดับเป้าหมายต้องสูงกว่าระดับปัจจุบัน",
    "보유 골드는 0 이상의 유한한 숫자로 입력하세요.": "ทองต้องเป็นจำนวนที่มีค่าจำกัดและไม่ต่ำกว่า 0",
    "입력값으로 계산할 수 없습니다. 레벨과 골드를 확인하세요.": "คำนวณไม่ได้ กรุณาตรวจสอบระดับและทอง",
    "입력값을 확인하세요: {error}": "ตรวจสอบข้อมูล: {error}",
    "유효한 숫자를 입력하세요.": "กรุณาป้อนตัวเลขที่ถูกต้อง",
    "파일을 저장하지 못했습니다. 폴더의 쓰기 권한을 확인하세요.": "บันทึกไฟล์ไม่ได้ กรุณาตรวจสอบสิทธิ์เขียนในโฟลเดอร์",
    "언어를 선택하면 모든 화면에 즉시 적용됩니다.": "เลือกภาษาเพื่อใช้กับทุกหน้าจอทันที",
    "언어 설정이 자동으로 저장됩니다.": "การตั้งค่าภาษาจะถูกบันทึกโดยอัตโนมัติ",
    "언어 설정을 저장하지 못했습니다. 이번 실행에만 적용됩니다.": "บันทึกภาษาไม่ได้ จะใช้เฉพาะครั้งนี้เท่านั้น"
  },
  "vi": {
    "Player Stats": "Chỉ số người chơi",
    "도시 계산기": "Tính toán thành phố",
    "설정": "Cài đặt",
    "언어": "Ngôn ngữ",
    "플레이어 능력치 계산 및 저장": "Tính và lưu chỉ số người chơi",
    "장비 + 레벨 + 병력": "Trang bị + Cấp + Quân",
    "장비 공격력 (%)": "Tấn công trang bị (%)",
    "레벨": "Cấp",
    "병력": "Quân số",
    "계산": "Tính toán",
    "저장": "Lưu",
    "공격력 직접 입력": "Nhập trực tiếp sức tấn công",
    "공격력": "Sức tấn công",
    "결과": "Kết quả",
    "계산 대기": "Sẵn sàng tính",
    "저장 완료": "Đã lưu",
    "목표 레벨 없음": "Không có cấp mục tiêu",
    "목표 레벨 {level}": "Cấp mục tiêu {level}",
    "목표 레벨 비용": "Chi phí đến cấp mục tiêu",
    "보유 골드로 업그레이드": "Nâng cấp bằng vàng hiện có",
    "도시 수": "Số thành phố",
    "현재 도시 레벨": "Cấp thành phố hiện tại",
    "목표 도시 레벨": "Cấp thành phố mục tiêu",
    "보유 골드": "Vàng hiện có",
    "초기화": "Đặt lại",
    "도달 도시 레벨": "Cấp thành phố đạt được",
    "총 필요 골드 / 사용 골드": "Tổng vàng cần / đã dùng",
    "남은 골드": "Vàng còn lại",
    "도시당 성벽": "Tường mỗi thành phố",
    "도시당 승점": "Điểm chiến thắng mỗi thành phố",
    "총 획득 승점": "Tổng điểm chiến thắng nhận được",
    "입력 오류": "Lỗi nhập liệu",
    "공격력 또는 병력은 예: 55G, 42.2T, 1.5P 처럼 입력하세요.": "Nhập sức tấn công hoặc quân số như 55G, 42.2T hoặc 1.5P.",
    "공격력을 입력하세요.": "Vui lòng nhập sức tấn công.",
    "공격력은 0 이상이어야 합니다.": "Sức tấn công phải từ 0 trở lên.",
    "레벨을 입력하세요.": "Vui lòng nhập cấp.",
    "레벨은 1 이상이어야 합니다.": "Cấp phải ít nhất là 1.",
    "도시 수와 현재 레벨은 1 이상의 정수로 입력하세요.": "Số thành phố và cấp hiện tại phải là số nguyên từ 1 trở lên.",
    "목표 레벨은 현재 레벨보다 높아야 합니다.": "Cấp mục tiêu phải cao hơn cấp hiện tại.",
    "보유 골드는 0 이상의 유한한 숫자로 입력하세요.": "Vàng phải là số hữu hạn từ 0 trở lên.",
    "입력값으로 계산할 수 없습니다. 레벨과 골드를 확인하세요.": "Không thể tính. Hãy kiểm tra cấp và vàng.",
    "입력값을 확인하세요: {error}": "Kiểm tra dữ liệu: {error}",
    "유효한 숫자를 입력하세요.": "Vui lòng nhập số hợp lệ.",
    "파일을 저장하지 못했습니다. 폴더의 쓰기 권한을 확인하세요.": "Không thể lưu tệp. Hãy kiểm tra quyền ghi thư mục.",
    "언어를 선택하면 모든 화면에 즉시 적용됩니다.": "Chọn ngôn ngữ để áp dụng ngay cho tất cả màn hình.",
    "언어 설정이 자동으로 저장됩니다.": "Lựa chọn ngôn ngữ được lưu tự động.",
    "언어 설정을 저장하지 못했습니다. 이번 실행에만 적용됩니다.": "Không thể lưu ngôn ngữ. Chỉ áp dụng trong phiên này."
  },
  "ru": {
    "Player Stats": "Характеристики игрока",
    "도시 계산기": "Калькулятор городов",
    "설정": "Настройки",
    "언어": "Язык",
    "플레이어 능력치 계산 및 저장": "Расчёт и сохранение характеристик",
    "장비 + 레벨 + 병력": "Снаряжение + Уровень + Войска",
    "장비 공격력 (%)": "Атака снаряжения (%)",
    "레벨": "Уровень",
    "병력": "Войска",
    "계산": "Рассчитать",
    "저장": "Сохранить",
    "공격력 직접 입력": "Прямой ввод силы атаки",
    "공격력": "Сила атаки",
    "결과": "Результат",
    "계산 대기": "Готово к расчёту",
    "저장 완료": "Сохранено",
    "목표 레벨 없음": "Нет целевого уровня",
    "목표 레벨 {level}": "Целевой уровень {level}",
    "목표 레벨 비용": "Стоимость целевого уровня",
    "보유 골드로 업그레이드": "Улучшение на имеющееся золото",
    "도시 수": "Количество городов",
    "현재 도시 레벨": "Текущий уровень города",
    "목표 도시 레벨": "Целевой уровень города",
    "보유 골드": "Имеющееся золото",
    "초기화": "Сбросить",
    "도달 도시 레벨": "Достигнутый уровень города",
    "총 필요 골드 / 사용 골드": "Всего золота нужно / потрачено",
    "남은 골드": "Остаток золота",
    "도시당 성벽": "Стена каждого города",
    "도시당 승점": "Очки победы за город",
    "총 획득 승점": "Всего получено очков победы",
    "입력 오류": "Ошибка ввода",
    "공격력 또는 병력은 예: 55G, 42.2T, 1.5P 처럼 입력하세요.": "Введите силу атаки или войска в формате 55G, 42.2T или 1.5P.",
    "공격력을 입력하세요.": "Введите силу атаки.",
    "공격력은 0 이상이어야 합니다.": "Атака должна быть неотрицательной.",
    "레벨을 입력하세요.": "Введите уровень.",
    "레벨은 1 이상이어야 합니다.": "Уровень должен быть не ниже 1.",
    "도시 수와 현재 레벨은 1 이상의 정수로 입력하세요.": "Количество городов и текущий уровень должны быть целыми числами от 1.",
    "목표 레벨은 현재 레벨보다 높아야 합니다.": "Целевой уровень должен быть выше текущего.",
    "보유 골드는 0 이상의 유한한 숫자로 입력하세요.": "Золото должно быть конечным неотрицательным числом.",
    "입력값으로 계산할 수 없습니다. 레벨과 골드를 확인하세요.": "Расчёт невозможен. Проверьте уровень и золото.",
    "입력값을 확인하세요: {error}": "Проверьте ввод: {error}",
    "유효한 숫자를 입력하세요.": "Введите корректное число.",
    "파일을 저장하지 못했습니다. 폴더의 쓰기 권한을 확인하세요.": "Не удалось сохранить файл. Проверьте права записи в папку.",
    "언어를 선택하면 모든 화면에 즉시 적용됩니다.": "Выбранный язык сразу применяется ко всем экранам.",
    "언어 설정이 자동으로 저장됩니다.": "Выбранный язык сохраняется автоматически.",
    "언어 설정을 저장하지 못했습니다. 이번 실행에만 적용됩니다.": "Не удалось сохранить язык. Он применён только на этот сеанс."
  }
}



TRANSLATIONS["ko"]["Player Stats"] = "플레이어 스텟"
_THEME_KEYS = ["화면 스타일", "화이트 모드", "다크 모드", "언어와 화면을 나에게 맞게", "밝고 선명한 화면", "편안한 어두운 화면", "설정이 자동으로 저장됩니다.", "설정을 저장하지 못했습니다. 이번 실행에만 적용됩니다."]
_THEME_TEXT = {
 "ko": _THEME_KEYS,
 "en": ["Appearance", "White mode", "Dark mode", "Make the language and appearance yours", "Bright and clear", "Comfortably dark", "Settings are saved automatically.", "Could not save settings. Applied for this session only."],
 "ja": ["画面スタイル", "ホワイトモード", "ダークモード", "言語と画面を自分好みに", "明るく鮮明な画面", "落ち着いた暗い画面", "設定は自動保存されます。", "設定を保存できませんでした。今回のみ適用されます。"],
 "zh": ["外观", "白色模式", "深色模式", "自定义语言与外观", "明亮清晰", "舒适暗色", "设置会自动保存。", "无法保存设置，仅本次运行生效。"],
 "hi": ["दिखावट", "व्हाइट मोड", "डार्क मोड", "भाषा और दिखावट अपनी पसंद से चुनें", "उजली और स्पष्ट स्क्रीन", "आरामदायक गहरी स्क्रीन", "सेटिंग्स अपने आप सेव होती हैं।", "सेटिंग्स सेव नहीं हुईं। केवल इस सत्र में लागू हैं।"],
 "fil": ["Hitsura", "Puting mode", "Madilim na mode", "Iangkop ang wika at hitsura sa iyo", "Maliwanag at malinaw", "Komportableng madilim", "Awtomatikong nase-save ang mga setting.", "Hindi na-save ang mga setting. Para lamang sa sesyong ito."],
 "th": ["รูปแบบหน้าจอ", "โหมดสว่าง", "โหมดมืด", "ปรับภาษาและหน้าจอให้เป็นแบบคุณ", "สว่างและชัดเจน", "มืดสบายตา", "บันทึกการตั้งค่าโดยอัตโนมัติ", "บันทึกการตั้งค่าไม่ได้ ใช้เฉพาะครั้งนี้เท่านั้น"],
 "vi": ["Giao diện", "Chế độ sáng", "Chế độ tối", "Tùy chỉnh ngôn ngữ và giao diện", "Sáng và rõ nét", "Tối dịu mắt", "Cài đặt được lưu tự động.", "Không thể lưu cài đặt. Chỉ áp dụng trong phiên này."],
 "ru": ["Оформление", "Светлый режим", "Тёмный режим", "Настройте язык и оформление под себя", "Светлый и чёткий экран", "Комфортный тёмный экран", "Настройки сохраняются автоматически.", "Не удалось сохранить настройки. Применены только на этот сеанс."],
}
for _language, _values in _THEME_TEXT.items():
    TRANSLATIONS[_language].update(zip(_THEME_KEYS, _values))

# Map the original light palette to an accessible dark palette.
DARK_COLORS = {
 "#eef3f8": "#101827", "white": "#1b2638", "#ffffff": "#1b2638",
 "#f8fafc": "#111c2d", "#f0f6ff": "#111c2d", "#d9e2ec": "#34445d",
 "#bfdbfe": "#38547b", "#e8eef6": "#26364d", "#dce6f2": "#324863",
 "#dbeafe": "#203858", "#fff4d6": "#3c3020", "#e0e7ff": "#302d50",
 "#dcfce7": "#193c32", "#17202a": "#edf3fc", "#111827": "#edf3fc",
 "#6b7785": "#b3c0d2", "#475569": "#b9c7dc", "#1e40af": "#a8caff",
 "#92400e": "#ffd382", "#4338ca": "#c3b9ff", "#166534": "#91e5b8",
 "#b45309": "#ffd382", "#137f82": "#7be0d1",
}


def translate(text):
    text = str(text)
    catalog = TRANSLATIONS[CURRENT_LANGUAGE]
    if text in catalog:
        return catalog[text]
    match = re.fullmatch(r"목표 레벨 (\d+)", text)
    if match:
        return catalog["목표 레벨 {level}"].format(level=match.group(1))
    prefix = "입력값을 확인하세요: "
    if text.startswith(prefix):
        return catalog["입력값을 확인하세요: {error}"].format(error=translate(text[len(prefix):]))
    return text


def error_message(exc):
    if str(exc) in TRANSLATIONS["ko"]:
        return str(exc)
    if isinstance(exc, OSError):
        return "파일을 저장하지 못했습니다. 폴더의 쓰기 권한을 확인하세요."
    return "유효한 숫자를 입력하세요."


class LocalizedStringVar(tk.StringVar):
    """Keep the original message so language changes preserve result values."""
    def __init__(self, master=None, value=""):
        self.source_text = value
        super().__init__(master, value=translate(value))

    def set(self, value):
        self.source_text = str(value)
        super().set(translate(value))

    def refresh(self):
        super().set(translate(self.source_text))




LEVEL_ATTACK_RAW = [
    (61, "3.94M"), (62, "4.73M"), (63, "5.68M"), (64, "6.81M"), (65, "8.18M"),
    (66, "9.81M"), (67, "11.78M"), (68, "14.13M"), (69, "16.96M"), (70, "20.35M"),
    (71, "24.42M"), (72, "29.3M"), (73, "35.16M"), (74, "42.2M"), (75, "50.63M"),
    (76, "60.76M"), (77, "72.91M"), (78, "87.5M"), (79, "105M"), (80, "126M"),
    (81, "151M"), (82, "181M"), (83, "218M"), (84, "261M"), (85, "314M"),
    (86, "376M"), (87, "451M"), (88, "542M"), (89, "650M"), (90, "780M"),
    (91, "936M"), (92, "1.12G"), (93, "1.35G"), (94, "1.62G"), (95, "1.94G"),
    (96, "2.33G"), (97, "2.80G"), (98, "3.35G"), (99, "4.03G"), (100, "4.83G"),
    (101, "5.80G"), (102, "6.96G"), (103, "8.35G"), (104, "10.02G"), (105, "12.02G"),
    (106, "14.42G"), (107, "17.31G"), (108, "20.77G"), (109, "24.92G"), (110, "29.91G"),
    (111, "35.89G"), (112, "43.07G"), (113, "51.68G"), (114, "62.02G"), (115, "74.42G"),
    (116, "89.31G"), (117, "107.17G"), (118, "128.61G"), (119, "154.33G"), (120, "185.19G"),
    (121, "222.3G"), (122, "266.7G"), (123, "320.0G"), (124, "384.0G"), (125, "460.8G"),
    (126, "553.0G"), (127, "663.6G"), (128, "796.3G"), (129, "955.5G"), (130, "1.14T"),
    (131, "1.37T"), (132, "1.65T"), (133, "1.98T"), (134, "2.38T"), (135, "2.85T"),
    (136, "3.42T"), (137, "4.11T"), (138, "4.93T"), (139, "5.92T"), (140, "7.10T"),
    (141, "8.52T"), (142, "10.2T"), (143, "12.24T"), (144, "14.7T"), (145, "17.62T"),
    (146, "21.15T"), (147, "25.38T"), (148, "30.45T"), (149, "36.55T"), (150, "43.86T"),
    (151, "52.63T"), (152, "63.3T"), (153, "75.9T"), (154, "91.1T"), (155, "109.2T"),
    (156, "131T"), (157, "157.2T"), (158, "189T"), (159, "226.4T"), (160, "271.7T"),
    (161, "326.1T"), (162, "391.3T"), (163, "469.6T"), (164, "563.5T"), (165, "677T"),
    (166, "811.4T"), (167, "975T"), (168, "1.17P"), (169, "1.40P"), (170, "1.68P"),
    (171, "2.02P"), (172, "2.42P"), (173, "2.90P"), (174, "3.48P"), (175, "4.18P"),
    (176, "5.03P"), (177, "6.02P"), (178, "7.24P"), (179, "8.68P"), (180, "10.41P"),
    (181, "12.5P"), (182, "15P"), (183, "18P"), (184, "21.92P"), (185, "25.9P"),
    (186, "31.10P"), (187, "37.32P"), (188, "44.79P"), (189, "53.75P"), (190, "64.50P"),
    (191, "77.39P"), (192, "92.87P"), (193, "111.45P"), (194, "133.74P"), (195, "160.48P"),
    (196, "192.58P"), (197, "231.10P"), (198, "277.32P"), (199, "332.78P"), (200, "399.34P"),
]


UNIT_MAP = {
    "M": 1e6,
    "G": 1e9,
    "T": 1e12,
    "P": 1e15,
    "ㅁ": 1e6,
    "ㄱ": 1e9,
    "ㅎ": 1e9,
    "ㅌ": 1e12,
    "ㅍ": 1e15,
}

LEVEL_TO_RAW = dict(LEVEL_ATTACK_RAW)


def parse_power(text: str) -> float:
    value = (text or "").strip().replace(",", "")
    match = re.fullmatch(r"(\d+(?:\.\d+)?)\s*([mMgGtTpPㅁㄱㅎㅌㅍ])", value)
    if not match:
        raise ValueError("공격력 또는 병력은 예: 55G, 42.2T, 1.5P 처럼 입력하세요.")
    number, unit = match.groups()
    multiplier = UNIT_MAP[unit.upper() if unit.isascii() else unit]
    return float(number) * multiplier


def parse_percent(text: str) -> float:
    value = (text or "").strip().replace(" ", "").replace("%", "")
    if not value:
        raise ValueError("공격력을 입력하세요.")
    percent = float(value)
    if percent < 0:
        raise ValueError("공격력은 0 이상이어야 합니다.")
    return percent


def apply_attack_percent(base_power: float, attack_percent: float) -> float:
    return base_power * ((attack_percent + 100.0) / 100.0)


LEVEL_ATTACK = [(level, parse_power(power)) for level, power in LEVEL_ATTACK_RAW]


def find_max_level(power: float) -> int | None:
    best = None
    for level, required in LEVEL_ATTACK:
        if power >= required:
            best = level
        else:
            break
    return best


def target_level_text(power: float) -> str:
    level = find_max_level(power)
    if level is None:
        return "목표 레벨 없음"
    return f"목표 레벨 {level}"


def calculate_from_troops(troops_text: str, attack_percent: float) -> str:
    troops = parse_power(troops_text)
    final_power = apply_attack_percent(troops, attack_percent)
    return target_level_text(final_power)


def calculate_from_direct_power(power_text: str) -> str:
    return target_level_text(parse_power(power_text))


def calculate_level_attack(level: int) -> float:
    if level < 1:
        raise ValueError("레벨은 1 이상이어야 합니다.")
    return (level - 1) * 4.0


@dataclass
class SlotData:
    equipment_attack: str = ""
    level: str = ""
    troops: str = ""
    direct_power: str = ""


def slot_from_raw(raw: dict) -> SlotData:
    return SlotData(
        equipment_attack=str(raw.get("equipment_attack", "")),
        level=str(raw.get("level", "")),
        troops=str(raw.get("troops", "")),
        direct_power=str(raw.get("direct_power", raw.get("manual_attack", ""))),
    )


class PlayerStatsPanel(tk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.colors = {
            "bg": "#eef3f8",
            "card": "#ffffff",
            "border": "#d9e2ec",
            "text": "#17202a",
            "muted": "#6b7785",
            "primary": "#2563eb",
            "primary_hover": "#1d4ed8",
            "dark": "#111827",
            "input": "#f8fafc",
            "slot": "#e8eef6",
        }

        self.configure(bg=self.colors["bg"])

        self.slots = self.load_slots()
        self.current_slot = 1
        self.vars = {
            "equipment_attack": tk.StringVar(),
            "level": tk.StringVar(),
            "troops": tk.StringVar(),
            "direct_power": tk.StringVar(),
        }
        self.slot_loaded = False
        self.result_var = LocalizedStringVar(self, value="계산 대기")

        self.build_ui()
        self.select_slot(1)

    def load_slots(self) -> dict[int, SlotData]:
        if not SAVE_FILE.exists():
            return {idx: SlotData() for idx in SLOT_NAMES}
        try:
            raw = json.loads(SAVE_FILE.read_text(encoding="utf-8"))
            return {idx: slot_from_raw(raw.get(str(idx), {})) for idx in SLOT_NAMES}
        except Exception:
            return {idx: SlotData() for idx in SLOT_NAMES}

    def save_slots(self) -> None:
        data = {str(idx): asdict(slot) for idx, slot in self.slots.items()}
        SAVE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def build_ui(self) -> None:
        root = tk.Frame(self, bg=self.colors["bg"])
        root.pack(fill="both", expand=True, padx=22, pady=18)
        root.columnconfigure(0, weight=3, uniform="main")
        root.columnconfigure(1, weight=2, uniform="main")
        root.rowconfigure(2, weight=1)

        title_row = tk.Frame(root, bg=self.colors["bg"])
        title_row.grid(row=0, column=0, columnspan=2, sticky="ew")
        tk.Label(
            title_row,
            text="Player Stats",
            bg=self.colors["bg"],
            fg=self.colors["text"],
            font=(UI_FONT, 19, "bold"),
        ).pack(side="left")
        tk.Label(
            title_row,
            text="플레이어 능력치 계산 및 저장",
            bg=self.colors["bg"],
            fg=self.colors["muted"],
            font=(UI_FONT, 10),
        ).pack(side="right", pady=(7, 0))

        slot_bar = tk.Frame(root, bg=self.colors["slot"], highlightbackground=self.colors["border"], highlightthickness=1)
        slot_bar.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(15, 14))
        slot_bar.columnconfigure(0, weight=1)
        self.slot_buttons: dict[int, tk.Button] = {}
        for idx in SLOT_NAMES:
            button = tk.Button(
                slot_bar,
                text=SLOT_NAMES[idx],
                command=lambda slot=idx: self.select_slot(slot),
                bd=0,
                relief="flat",
                cursor="hand2",
                font=(UI_FONT, 11, "bold"),
                pady=10,
            )
            button.grid(row=0, column=idx - 1, sticky="ew", padx=3, pady=3)
            self.slot_buttons[idx] = button

        combined = self.make_panel(root, "장비 + 레벨 + 병력", 2, 0)
        self.add_labeled_entry(combined, "장비 공격력 (%)", "equipment_attack", 1, self.calculate_combined)
        self.add_labeled_entry(combined, "레벨", "level", 2, self.calculate_combined)
        self.add_labeled_entry(combined, "병력", "troops", 3, self.calculate_combined)

        button_row = tk.Frame(combined, bg=self.colors["card"])
        button_row.grid(row=4, column=0, columnspan=2, sticky="ew", padx=14, pady=(6, 14))
        self.make_button(button_row, "계산", self.calculate_combined, "primary").pack(side="left", fill="x", expand=True)
        self.make_button(button_row, "저장", self.store_current_inputs, "secondary").pack(side="left", fill="x", expand=True, padx=(8, 0))

        side = tk.Frame(root, bg=self.colors["bg"])
        side.grid(row=2, column=1, sticky="nsew", padx=(14, 0))
        side.columnconfigure(0, weight=1)
        side.rowconfigure(1, weight=1)

        direct = self.make_panel(side, "공격력 직접 입력", 0, 0, padx=0, pady=(0, 12))
        self.add_labeled_entry(direct, "공격력", "direct_power", 1, self.calculate_direct)
        self.make_button(direct, "계산", self.calculate_direct, "primary").grid(
            row=2, column=0, columnspan=2, sticky="ew", padx=14, pady=(6, 14)
        )

        result_panel = self.make_panel(side, "결과", 1, 0, padx=0, pady=0, sticky="nsew")
        result_panel.rowconfigure(1, weight=1)
        tk.Label(
            result_panel,
            textvariable=self.result_var,
            bg=self.colors["card"],
            fg=self.colors["primary"],
            font=(UI_FONT, 22, "bold"),
            wraplength=300,
            anchor="center",
        ).grid(row=1, column=0, columnspan=2, sticky="nsew", padx=14, pady=(12, 18))

        for frame in (combined, direct):
            frame.columnconfigure(1, weight=1)

    def make_panel(
        self,
        parent: tk.Frame,
        title: str,
        row: int,
        column: int,
        padx: int | tuple[int, int] = 0,
        pady: int | tuple[int, int] = 0,
        sticky: str = "nsew",
    ) -> tk.Frame:
        panel = tk.Frame(
            parent,
            bg=self.colors["card"],
            highlightbackground=self.colors["border"],
            highlightthickness=1,
        )
        panel.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady)
        tk.Label(
            panel,
            text=title,
            bg=self.colors["card"],
            fg=self.colors["text"],
            font=(UI_FONT, 13, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=14, pady=(14, 10))
        return panel

    def add_labeled_entry(self, parent: tk.Frame, label: str, key: str, row: int, enter_command) -> None:
        tk.Label(
            parent,
            text=label,
            bg=self.colors["card"],
            fg=self.colors["muted"],
            font=(UI_FONT, 10, "bold"),
        ).grid(row=row, column=0, sticky="w", padx=(14, 12), pady=6)
        entry = tk.Entry(
            parent,
            textvariable=self.vars[key],
            bg=self.colors["input"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.colors["border"],
            highlightcolor=self.colors["primary"],
            font=(UI_FONT, 12),
        )
        entry.grid(row=row, column=1, sticky="ew", padx=(0, 14), pady=6, ipady=8)
        entry.bind("<KeyRelease>", lambda _event: self.store_current_inputs(silent=True))
        entry.bind("<Return>", lambda _event: enter_command())

    def make_button(self, parent: tk.Frame, text: str, command, kind: str) -> tk.Button:
        if kind == "primary":
            bg = self.colors["primary"]
            fg = "#ffffff"
            active_bg = self.colors["primary_hover"]
        else:
            bg = self.colors["slot"]
            fg = self.colors["text"]
            active_bg = "#dce6f2"
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=active_bg,
            activeforeground=fg,
            bd=0,
            relief="flat",
            cursor="hand2",
            font=(UI_FONT, 11, "bold"),
            pady=10,
        )

    def select_slot(self, slot: int) -> None:
        if self.slot_loaded:
            self.store_current_inputs(silent=True)
        self.current_slot = slot
        data = self.slots[slot]
        for key, var in self.vars.items():
            var.set(getattr(data, key))
        for idx, button in self.slot_buttons.items():
            if idx == slot:
                button.configure(bg=self.colors["primary"], fg="#ffffff", activebackground=self.colors["primary_hover"])
            else:
                button.configure(bg=self.colors["slot"], fg=self.colors["text"], activebackground="#dce6f2")
        self.result_var.set("계산 대기")
        self.slot_loaded = True

    def store_current_inputs(self, silent: bool = False) -> None:
        self.slots[self.current_slot] = SlotData(**{key: var.get() for key, var in self.vars.items()})
        self.save_slots()
        if not silent:
            self.result_var.set("저장 완료")

    def calculate_combined(self) -> None:
        try:
            equipment_attack = parse_percent(self.vars["equipment_attack"].get())
            level_text = self.vars["level"].get().strip()
            if not level_text:
                raise ValueError("레벨을 입력하세요.")
            level = int(level_text)
            if level < 1:
                raise ValueError("레벨은 1 이상이어야 합니다.")

            total_attack = equipment_attack + calculate_level_attack(level)
            result = calculate_from_troops(self.vars["troops"].get(), total_attack)
            self.store_current_inputs(silent=True)
            self.result_var.set(result)
        except Exception as exc:
            messagebox.showerror(translate("입력 오류"), translate(error_message(exc)), parent=self)

    def calculate_direct(self) -> None:
        try:
            result = calculate_from_direct_power(self.vars["direct_power"].get())
            self.store_current_inputs(silent=True)
            self.result_var.set(result)
        except Exception as exc:
            messagebox.showerror(translate("입력 오류"), translate(error_message(exc)), parent=self)


# City calculation functions reconstructed from the supplied Python bytecode.
# The original formulas and result formatting are preserved.
UNIT_FACTORS = {"U": 1, "K": 1000, "M": 1000000, "G": 1000000000, "T": 1000000000000}


def js_round(value: float) -> int:
    return math.floor(value + 0.5)


def format_unit(value: float) -> str:
    value = math.floor(value)
    unit = ""
    num = float(value)
    for suffix, factor in (("T", 10**12), ("G", 10**9), ("M", 10**6), ("K", 1000)):
        if value >= factor:
            unit = suffix
            num = value / factor
            break
    if num >= 100:
        num = js_round(num)
    elif num >= 10:
        num = js_round(num * 10) / 10
    else:
        num = js_round(num * 100) / 100
    if float(num).is_integer():
        return f"{int(num)}{unit}"
    return f"{num:g}{unit}"


@dataclass(frozen=True)
class CityCostResult:
    total_cost: str
    city_wall: str
    new_city_vp: str
    total_vp_won: str


@dataclass(frozen=True)
class CityUpgradeResult:
    new_city_level: int | str
    city_wall: str
    total_cost: str
    remaining_gold: str
    new_city_vp: str
    total_vp_won: str


def calculate_city_cost(number_of_cities: int, starting_level: int, target_level: int) -> CityCostResult:
    if number_of_cities < 1 or starting_level < 1 or target_level < starting_level + 1:
        return CityCostResult(*(["NaN"] * 4))
    city_wall = 70 * 1.2 ** (target_level - 1)
    new_city_vp = 20 * 1.115 ** (target_level - 1)
    total_cost = number_of_cities * (50 * (1.2 ** (target_level - 1) - 1.2 ** (starting_level - 1)))
    total_vp_won = number_of_cities * (20 * 1.115 ** (target_level - 1) - 20 * 1.115 ** (starting_level - 1))
    return CityCostResult(format_unit(total_cost), format_unit(city_wall), format_unit(new_city_vp), format_unit(total_vp_won))


def calculate_city_upgrade(number_of_cities: int, starting_level: int, gold_amount: float, gold_unit: str) -> CityUpgradeResult:
    unit_factor = UNIT_FACTORS.get(gold_unit, 1)
    if number_of_cities < 1 or starting_level < 1 or gold_amount < 0:
        return CityUpgradeResult(*(["NaN"] * 6))
    total_gold = gold_amount * unit_factor
    try:
        new_city_level = math.floor(math.log(total_gold / (number_of_cities * 10 / 0.2) + 1.2 ** (starting_level - 1)) / math.log(1.2) + 1)
    except (ValueError, OverflowError, ZeroDivisionError):
        return CityUpgradeResult(*(["NaN"] * 6))
    city_wall = 70 * 1.2 ** (new_city_level - 1)
    total_cost = number_of_cities * (50 * (1.2 ** (new_city_level - 1) - 1.2 ** (starting_level - 1)))
    remaining_gold = total_gold - total_cost
    new_city_vp = 20 * 1.115 ** (new_city_level - 1)
    total_vp_won = number_of_cities * (20 * 1.115 ** (new_city_level - 1) - 20 * 1.115 ** (starting_level - 1))
    if remaining_gold < 0 or total_cost < 0:
        return CityUpgradeResult(*(["NaN"] * 6))
    return CityUpgradeResult(new_city_level, format_unit(city_wall), format_unit(total_cost), format_unit(remaining_gold), format_unit(new_city_vp), format_unit(total_vp_won))


class CityCalculatorPanel(tk.Frame):
    """City upgrade cost and available-gold calculators in a shared window."""

    def __init__(self, master):
        super().__init__(master, bg="#eef3f8")
        self.mode = tk.StringVar(self, value="cost")
        self.inputs = {key: tk.StringVar(self, value=value) for key, value in {
            "cities": "1", "start": "1", "target": "2", "gold": "100", "unit": "G"
        }.items()}
        self.results = {key: tk.StringVar(self, value="—") for key in (
            "new_city_level", "total_cost", "remaining_gold", "city_wall", "new_city_vp", "total_vp_won"
        )}
        self.status = LocalizedStringVar(self, value="")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        heading = tk.Frame(self, bg="#eef3f8")
        heading.grid(row=0, column=0, sticky="ew", padx=22, pady=(18, 10))
        tk.Label(heading, text="도시 계산기", font=(UI_FONT, 19, "bold"), bg="#eef3f8", fg="#17202a").pack(side="left")
        modes = tk.Frame(self, bg="#eef3f8")
        modes.grid(row=1, column=0, sticky="ew", padx=22, pady=(0, 14))
        for text, value in (("목표 레벨 비용", "cost"), ("보유 골드로 업그레이드", "gold")):
            ttk.Radiobutton(modes, text=text, variable=self.mode, value=value, command=self.change_mode, style="CityMode.Toolbutton", cursor="hand2").pack(side="left", padx=(0, 8))
        body = tk.Frame(self, bg="#eef3f8")
        body.grid(row=2, column=0, sticky="nsew", padx=22, pady=(0, 18))
        body.columnconfigure(0, weight=2, uniform="city")
        body.columnconfigure(1, weight=3, uniform="city")
        body.rowconfigure(0, weight=1)
        form = tk.Frame(body, bg="white", highlightbackground="#d9e2ec", highlightthickness=1)
        form.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        form.columnconfigure(0, weight=1)
        self.field_rows = {}
        fields = (("cities", "도시 수"), ("start", "현재 도시 레벨"), ("target", "목표 도시 레벨"), ("gold", "보유 골드"))
        for row, (key, label) in enumerate(fields):
            field = tk.Frame(form, bg="white")
            field.grid(row=row, column=0, sticky="ew", padx=16, pady=(12, 0))
            field.columnconfigure(0, weight=1)
            tk.Label(field, text=label, bg="white", fg="#6b7785", font=(UI_FONT, 10, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 5))
            entry = tk.Entry(field, textvariable=self.inputs[key], font=(UI_FONT, 12),
                             bg="#f0f6ff", fg="#17202a", relief="flat", highlightthickness=1,
                             highlightbackground="#bfdbfe", highlightcolor="#2563eb", insertbackground="#2563eb")
            entry.grid(row=1, column=0, sticky="ew", ipady=5)
            entry.bind("<Return>", lambda _event: self.calculate())
            if key == "gold":
                ttk.Combobox(field, textvariable=self.inputs["unit"], values=list(UNIT_FACTORS), state="readonly", width=4).grid(row=1, column=1, padx=(6, 0), sticky="ns")
            self.field_rows[key] = field
        buttons = tk.Frame(form, bg="white")
        buttons.grid(row=4, column=0, sticky="ew", padx=16, pady=18)
        ttk.Button(buttons, text="계산", command=self.calculate, style="CityPrimary.TButton").pack(side="left", fill="x", expand=True)
        ttk.Button(buttons, text="초기화", command=self.reset, style="CitySecondary.TButton").pack(side="left", fill="x", expand=True, padx=(8, 0))
        result_frame = tk.Frame(body, bg="white", highlightbackground="#d9e2ec", highlightthickness=1)
        result_frame.grid(row=0, column=1, sticky="nsew")
        result_frame.columnconfigure(0, weight=1)
        result_frame.columnconfigure(1, weight=1)
        labels = (("new_city_level", "도달 도시 레벨"), ("total_cost", "총 필요 골드 / 사용 골드"),
                  ("remaining_gold", "남은 골드"), ("city_wall", "도시당 성벽"),
                  ("new_city_vp", "도시당 승점"), ("total_vp_won", "총 획득 승점"))
        for row, (key, label) in enumerate(labels):
            result_frame.rowconfigure(row, weight=1)
            background, accent = {
                "new_city_level": ("#dbeafe", "#1d4ed8"),
                "total_cost": ("#fff4d6", "#92400e"),
                "remaining_gold": ("#fff4d6", "#92400e"),
                "city_wall": ("#e0e7ff", "#4338ca"),
                "new_city_vp": ("#dcfce7", "#166534"),
                "total_vp_won": ("#dcfce7", "#166534"),
            }[key]
            card = tk.Frame(result_frame, bg=background)
            card.grid(row=row, column=0, columnspan=2, sticky="nsew", padx=10, pady=4)
            card.columnconfigure(0, weight=1)
            card.columnconfigure(1, weight=1)
            card.rowconfigure(0, weight=1)
            tk.Label(card, text=label, bg=background, fg=accent, font=(UI_FONT, 10, "bold"), anchor="w", wraplength=250, justify="left").grid(row=0, column=0, sticky="ew", padx=12, pady=6)
            tk.Label(card, textvariable=self.results[key], bg=background, fg=accent, font=(UI_FONT, 20, "bold"), anchor="e").grid(row=0, column=1, sticky="ew", padx=12, pady=6)
        tk.Label(self, textvariable=self.status, bg="#eef3f8", fg="#b45309", font=(UI_FONT, 10), wraplength=850).grid(row=3, column=0, sticky="ew", padx=22, pady=(0, 12))
        self.change_mode()

    def change_mode(self):
        self.field_rows["target"].grid_remove()
        self.field_rows["gold"].grid_remove()
        self.field_rows["target" if self.mode.get() == "cost" else "gold"].grid()
        self.clear_results()

    def clear_results(self):
        for value in self.results.values():
            value.set("—")
        self.status.set("")

    def reset(self):
        for key, value in {"cities": "1", "start": "1", "target": "2", "gold": "100", "unit": "G"}.items():
            self.inputs[key].set(value)
        self.clear_results()

    def calculate(self):
        self.clear_results()
        try:
            cities = int(self.inputs["cities"].get().strip())
            start = int(self.inputs["start"].get().strip())
            if cities < 1 or start < 1:
                raise ValueError("도시 수와 현재 레벨은 1 이상의 정수로 입력하세요.")
            if self.mode.get() == "cost":
                target = int(self.inputs["target"].get().strip())
                if target <= start:
                    raise ValueError("목표 레벨은 현재 레벨보다 높아야 합니다.")
                result = calculate_city_cost(cities, start, target)
                values = asdict(result)
                values["new_city_level"] = target
            else:
                gold = float(self.inputs["gold"].get().strip().replace(",", ""))
                if not math.isfinite(gold) or gold < 0:
                    raise ValueError("보유 골드는 0 이상의 유한한 숫자로 입력하세요.")
                values = asdict(calculate_city_upgrade(cities, start, gold, self.inputs["unit"].get()))
            if "NaN" in values.values():
                raise ValueError("입력값으로 계산할 수 없습니다. 레벨과 골드를 확인하세요.")
            for key, value in values.items():
                self.results[key].set(str(value))
        except (ValueError, OverflowError, ZeroDivisionError) as exc:
            self.status.set("입력값을 확인하세요: " + error_message(exc))


class SettingsPanel(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, bg="#eef3f8")
        hero = tk.Frame(self, bg="#dbeafe")
        hero.pack(fill="x", padx=22, pady=(18, 16))
        tk.Label(hero, text="설정", bg="#dbeafe", fg="#1e40af", font=(UI_FONT, 22, "bold")).pack(anchor="w", padx=22, pady=(14, 4))
        tk.Label(hero, text="언어와 화면을 나에게 맞게", bg="#dbeafe", fg="#475569", font=(UI_FONT, 11)).pack(anchor="w", padx=22, pady=(0, 16))
        body = tk.Frame(self, bg="#eef3f8")
        body.pack(fill="both", expand=True, padx=22)
        body.columnconfigure(0, weight=1, uniform="settings")
        body.columnconfigure(1, weight=1, uniform="settings")
        body.rowconfigure(0, weight=1)
        language_card = tk.Frame(body, bg="white", highlightbackground="#bfdbfe", highlightthickness=1)
        language_card.grid(row=0, column=0, sticky="nsew", padx=(0, 9))
        appearance = tk.Frame(body, bg="white", highlightbackground="#bfdbfe", highlightthickness=1)
        appearance.grid(row=0, column=1, sticky="nsew", padx=(9, 0))
        for card, title in ((language_card, "언어"), (appearance, "화면 스타일")):
            tk.Frame(card, bg="#2563eb", height=4).pack(fill="x")
            tk.Label(card, text=title, bg="white", fg="#2563eb", font=(UI_FONT, 15, "bold")).pack(anchor="w", padx=20, pady=(20, 14))
        tk.Label(language_card, text="언어를 선택하면 모든 화면에 즉시 적용됩니다.", bg="white", fg="#475569", font=(UI_FONT, 11), wraplength=420, justify="left").pack(anchor="w", padx=20, pady=(0, 20))
        self.language = tk.StringVar(self, value=LANGUAGE_NAMES[CURRENT_LANGUAGE])
        self.selector = ttk.Combobox(language_card, textvariable=self.language, values=list(LANGUAGE_NAMES.values()), state="readonly", font=("Segoe UI", 13), width=26)
        self.selector.pack(fill="x", padx=20, pady=(0, 18), ipady=8)
        self.selector.bind("<<ComboboxSelected>>", lambda _event: app.change_language(list(LANGUAGE_NAMES)[self.selector.current()]))
        self.theme = tk.StringVar(self, value=app.theme)
        self.theme_buttons = {}
        for mode, title, subtitle in (("light", "화이트 모드", "밝고 선명한 화면"), ("dark", "다크 모드", "편안한 어두운 화면")):
            row = tk.Frame(appearance, bg="#eef3f8")
            row.pack(fill="x", padx=20, pady=(0, 12))
            button = ttk.Radiobutton(row, text=title, value=mode, variable=self.theme,
                                    style="CityMode.Toolbutton", command=lambda m=mode: app.change_theme(m))
            button.pack(fill="x", padx=8, pady=(8, 0))
            self.theme_buttons[mode] = button
            tk.Label(row, text=subtitle, bg="#eef3f8", fg="#475569", font=(UI_FONT, 10)).pack(anchor="w", padx=16, pady=(6, 10))
        self.notice = LocalizedStringVar(self, value="설정이 자동으로 저장됩니다.")
        tk.Label(self, textvariable=self.notice, bg="#eef3f8", fg="#166534", font=(UI_FONT, 10), wraplength=1000, justify="left").pack(anchor="w", padx=24, pady=16)


class MillionLordsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        global CURRENT_LANGUAGE, UI_FONT
        self.theme = "light"
        try:
            saved = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
            self.theme = "dark" if saved.get("theme") == "dark" else "light"
            language = saved.get("language", "en")
            CURRENT_LANGUAGE = language if language in LANGUAGE_NAMES else "en"
        except (OSError, ValueError, AttributeError, TypeError):
            CURRENT_LANGUAGE = "en"
        UI_FONT = LANGUAGE_FONTS[CURRENT_LANGUAGE]
        self.geometry("1180x660")
        self.minsize(1120, 620)
        self.configure(bg="#eef3f8")
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Pages.TNotebook", background="#eef3f8", borderwidth=0)
        style.layout("Pages.TNotebook.Tab", [])
        style.configure("CityPrimary.TButton", background="#2563eb", foreground="white", borderwidth=0)
        style.map("CityPrimary.TButton", background=[("active", "#1d4ed8"), ("pressed", "#1e40af")])
        style.configure("CitySecondary.TButton", background="#dbeafe", foreground="#1e40af", borderwidth=0)
        style.map("CitySecondary.TButton", background=[("active", "#bfdbfe")])
        style.configure("CityMode.Toolbutton", background="#dbeafe", foreground="#1e40af",
                        font=(UI_FONT, 11, "bold"), padding=(18, 11), borderwidth=0)
        style.map("CityMode.Toolbutton", background=[("selected", "#2563eb"), ("active", "#bfdbfe")],
                  foreground=[("selected", "white")])
        style.configure("TButton", font=(UI_FONT, 10), padding=(10, 8))
        style.configure("TRadiobutton", background="#eef3f8", font=(UI_FONT, 11))
        navigation = tk.Frame(self, bg="#eef3f8", height=68)
        navigation.pack(fill="x", padx=22, pady=(10, 0))
        navigation.pack_propagate(False)
        self.nav_buttons = []
        for index, title in enumerate(("Player Stats", "도시 계산기", "설정")):
            button = tk.Button(navigation, text=title, command=lambda i=index: self.select_page(i),
                               relief="flat", bd=0, cursor="hand2", activebackground="#1d4ed8",
                               activeforeground="white")
            button.pack(side="left", padx=(0, 10), anchor="s")
            self.nav_buttons.append(button)
        self.tabs = ttk.Notebook(self, style="Pages.TNotebook")
        self.tabs.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.player_stats = PlayerStatsPanel(self.tabs)
        self.city_calculator = CityCalculatorPanel(self.tabs)
        self.tabs.add(self.player_stats, text="Player Stats")
        self.tabs.add(self.city_calculator, text="도시 계산기")
        self.settings = SettingsPanel(self.tabs, self)
        self.tabs.add(self.settings, text="설정")
        self.translated_widgets = []
        self.collect_translated_widgets(self)
        self.theme_widgets = []
        self.collect_theme_widgets(self)
        self.refresh_language()
        self.apply_theme()
        self.tabs.bind("<<NotebookTabChanged>>", self.update_navigation)
        self.select_page(0)

    def collect_translated_widgets(self, parent):
        for widget in parent.winfo_children():
            if "text" in widget.keys() and not ("textvariable" in widget.keys() and widget.cget("textvariable")):
                source = str(widget.cget("text"))
                if source in TRANSLATIONS["ko"]:
                    self.translated_widgets.append((widget, source))
            self.collect_translated_widgets(widget)

    def change_language(self, language):
        global CURRENT_LANGUAGE, UI_FONT
        if language not in LANGUAGE_NAMES:
            return
        CURRENT_LANGUAGE = language
        UI_FONT = LANGUAGE_FONTS[language]
        self.refresh_language()
        self.save_settings()

    def save_settings(self):
        try:
            SETTINGS_FILE.write_text(json.dumps({"language": CURRENT_LANGUAGE, "theme": self.theme}, ensure_ascii=False, indent=2), encoding="utf-8")
            self.settings.notice.set("설정이 자동으로 저장됩니다.")
        except OSError:
            self.settings.notice.set("설정을 저장하지 못했습니다. 이번 실행에만 적용됩니다.")

    def change_theme(self, theme):
        if theme not in ("light", "dark"):
            return
        self.theme = theme
        self.settings.theme.set(theme)
        self.apply_theme()
        self.save_settings()

    def themed_color(self, color, option="background"):
        if self.theme != "dark":
            return color
        if option in ("foreground", "activeforeground", "insertbackground"):
            if color.lower() in ("white", "#ffffff"):
                return "#ffffff"
            if color == "#2563eb" or color == "#1d4ed8":
                return "#8dbaff"
        return DARK_COLORS.get(color.lower(), color)

    def collect_theme_widgets(self, widget):
        options = {}
        for option in ("background", "foreground", "activebackground", "activeforeground", "highlightbackground", "highlightcolor", "insertbackground"):
            if option in widget.keys():
                options[option] = str(widget.cget(option))
        self.theme_widgets.append((widget, options))
        for child in widget.winfo_children():
            self.collect_theme_widgets(child)

    def apply_theme(self):
        for widget, options in self.theme_widgets:
            widget.configure(**{key: self.themed_color(value, key) for key, value in options.items()})
        style = ttk.Style(self)
        dark = self.theme == "dark"
        bg, card, text = ("#101827", "#1b2638", "#edf3fc") if dark else ("#eef3f8", "white", "#17202a")
        style.configure("Pages.TNotebook", background=bg)
        style.configure("CitySecondary.TButton", background=self.themed_color("#dbeafe"), foreground=self.themed_color("#1e40af"))
        style.map("CitySecondary.TButton", background=[("active", self.themed_color("#bfdbfe"))])
        style.configure("CityMode.Toolbutton", background=self.themed_color("#dbeafe"), foreground=self.themed_color("#1e40af"))
        style.map("CityMode.Toolbutton", background=[("selected", "#2563eb"), ("active", self.themed_color("#bfdbfe"))], foreground=[("selected", "white")])
        style.configure("TCombobox", fieldbackground=card, background=card, foreground=text, arrowcolor=text)
        style.map("TCombobox", fieldbackground=[("readonly", card)], foreground=[("readonly", text)], selectbackground=[("readonly", card)], selectforeground=[("readonly", text)])
        self.option_add("*TCombobox*Listbox.background", card)
        self.option_add("*TCombobox*Listbox.foreground", text)
        self.option_add("*TCombobox*Listbox.selectBackground", "#2563eb")
        self.option_add("*TCombobox*Listbox.selectForeground", "white")
        for key in ("bg", "card", "border", "text", "muted", "input", "slot"):
            source = {"bg": "#eef3f8", "card": "#ffffff", "border": "#d9e2ec", "text": "#17202a", "muted": "#6b7785", "input": "#f8fafc", "slot": "#e8eef6"}[key]
            self.player_stats.colors[key] = self.themed_color(source)
        self.update_navigation()

    def refresh_language(self):
        for widget, source in self.translated_widgets:
            widget.configure(text=translate(source))
        self.player_stats.result_var.refresh()
        self.city_calculator.status.refresh()
        self.settings.notice.refresh()
        self.settings.language.set(LANGUAGE_NAMES[CURRENT_LANGUAGE])
        self.title("Million Lords - " + translate("Player Stats") + " / " + translate("도시 계산기"))
        for index, source in enumerate(("Player Stats", "도시 계산기", "설정")):
            self.tabs.tab(index, text=translate(source))
        from tkinter import font as tkfont
        def update_fonts(parent):
            for widget in parent.winfo_children():
                if "font" in widget.keys() and widget != self.settings.selector:
                    actual = tkfont.Font(self, font=widget.cget("font")).actual()
                    widget.configure(font=(UI_FONT, actual["size"], actual["weight"]))
                update_fonts(widget)
        update_fonts(self)
        style = ttk.Style(self)
        style.configure("TButton", font=(UI_FONT, 10))
        style.configure("CityMode.Toolbutton", font=(UI_FONT, 11, "bold"))
        self.update_navigation()

    def select_page(self, index):
        self.tabs.select(index)
        self.update_navigation()

    def update_navigation(self, _event=None):
        selected = self.tabs.index(self.tabs.select())
        for index, button in enumerate(self.nav_buttons):
            active = index == selected
            button.configure(
                font=(UI_FONT, 14 if active else 11, "bold"),
                padx=28 if active else 18, pady=14 if active else 8,
                bg="#2563eb" if active else self.themed_color("#dbeafe"),
                fg="white" if active else self.themed_color("#475569"),
            )


if __name__ == "__main__":
    MillionLordsApp().mainloop()

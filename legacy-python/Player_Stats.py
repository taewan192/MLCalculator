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


class AttackCalculatorApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
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

        self.title("Million Lords - Player Stats")
        self.geometry("790x480")
        self.minsize(760, 410)
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
        self.result_var = tk.StringVar(value="계산 대기")

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
            font=("Malgun Gothic", 19, "bold"),
        ).pack(side="left")
        tk.Label(
            title_row,
            text="플레이어 능력치 계산 및 저장",
            bg=self.colors["bg"],
            fg=self.colors["muted"],
            font=("Malgun Gothic", 10),
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
                font=("Malgun Gothic", 11, "bold"),
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
            font=("Malgun Gothic", 28, "bold"),
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
            font=("Malgun Gothic", 13, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=14, pady=(14, 10))
        return panel

    def add_labeled_entry(self, parent: tk.Frame, label: str, key: str, row: int, enter_command) -> None:
        tk.Label(
            parent,
            text=label,
            bg=self.colors["card"],
            fg=self.colors["muted"],
            font=("Malgun Gothic", 10, "bold"),
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
            font=("Malgun Gothic", 12),
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
            font=("Malgun Gothic", 11, "bold"),
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
            messagebox.showerror("입력 오류", str(exc))

    def calculate_direct(self) -> None:
        try:
            result = calculate_from_direct_power(self.vars["direct_power"].get())
            self.store_current_inputs(silent=True)
            self.result_var.set(result)
        except Exception as exc:
            messagebox.showerror("입력 오류", str(exc))


if __name__ == "__main__":
    AttackCalculatorApp().mainloop()

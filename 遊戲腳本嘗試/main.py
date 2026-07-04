import time
import threading
import sys
import tkinter as tk
from tkinter import ttk
from pynput import keyboard, mouse


class GameHelperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("遊戲助手 (20組智慧組合鍵+一鍵清除) ULTIMATE")
        self.root.geometry("960x580")  # 微調高度以容納一鍵控制按鈕
        self.root.resizable(False, False)

        self.running = False
        self.recording_entry = None

        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()

        # UI 頂部標題
        tk.Label(root, text="遊戲輔助腳本大師 (專業完全體)", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(root, text="快捷鍵：[F10] 啟動所有勾選功能  |  [F11] 全部停止", font=("Arial", 11, "italic"),
                 fg="gray").pack(pady=2)

        # ------------------ 功能一：滑鼠連點區域 ------------------
        click_frame = tk.LabelFrame(root, text=" 滑鼠連點設定 ", font=("Arial", 10, "bold"), padx=10, pady=5)
        click_frame.pack(fill="x", padx=15, pady=5)

        self.click_enable = tk.BooleanVar(value=False)
        tk.Checkbutton(click_frame, text="啟用滑鼠連點", variable=self.click_enable, font=("Arial", 10)).grid(row=0,
                                                                                                              column=0,
                                                                                                              sticky="w")

        self.left_var = tk.BooleanVar(value=True)
        self.right_var = tk.BooleanVar(value=False)
        tk.Checkbutton(click_frame, text="左鍵", variable=self.left_var).grid(row=0, column=1, padx=10)
        tk.Checkbutton(click_frame, text="右鍵", variable=self.right_var).grid(row=0, column=2, padx=10)

        tk.Label(click_frame, text="點擊間隔(秒):").grid(row=0, column=3, padx=5)
        self.click_delay_entry = tk.Entry(click_frame, width=8)
        self.click_delay_entry.insert(0, "0.1")
        self.click_delay_entry.grid(row=0, column=4)

        # ------------------ 功能二：20組自動施放技能區域 ------------------
        skills_main_frame = tk.LabelFrame(root, text=" 自動施放技能設定 (可搭配 CTRL/SHIFT/ALT 組合鍵) ",
                                          font=("Arial", 10, "bold"), padx=10, pady=5)
        skills_main_frame.pack(fill="both", expand=True, padx=15, pady=5)

        # 【核心新增】：一鍵快捷控制按鈕列
        ctrl_bar = tk.Frame(skills_main_frame)
        ctrl_bar.pack(fill="x", anchor="w", padx=5, pady=2)

        tk.Button(ctrl_bar, text=" 全選技能 ", command=self.select_all_skills, bg="#e1f5fe", font=("Arial", 9)).pack(
            side="left", padx=2)
        tk.Button(ctrl_bar, text=" 全部取消勾選 ", command=self.clear_all_skills, bg="#ffebee", fg="red",
                  font=("Arial", 9, "bold")).pack(side="left", padx=5)

        # 建立左、右排版
        left_column = tk.Frame(skills_main_frame)
        left_column.pack(side="left", fill="both", expand=True, padx=5)

        right_column = tk.Frame(skills_main_frame)
        right_column.pack(side="right", fill="both", expand=True, padx=5)

        self.skills_data = []

        # 迴圈產生 20 個技能格子
        for i in range(1, 21):
            target_column = left_column if i <= 10 else right_column
            row_frame = tk.Frame(target_column)
            row_frame.pack(fill="x", pady=2)

            # 1. 啟用打勾方塊
            enable_var = tk.BooleanVar(value=False)
            chk = tk.Checkbutton(row_frame, text=f"技能 {i:02d}", variable=enable_var, width=7, anchor="w")
            chk.pack(side="left")

            # 2. 組合鍵下拉選單
            modifier_combo = ttk.Combobox(row_frame, values=["無", "CTRL +", "SHIFT +", "ALT +"], width=8,
                                          state="readonly")
            modifier_combo.current(0)
            modifier_combo.pack(side="left", padx=2)

            # 3. 智慧按鍵輸入框
            key_entry = tk.Entry(row_frame, width=10, justify="center", bg="#f0f0f0", fg="blue",
                                 font=("Arial", 9, "bold"))
            key_entry.insert(0, str(i % 10))
            key_entry.pack(side="left", padx=2)
            key_entry.bind("<Button-1>", lambda event, e=key_entry: self.start_recording(e))

            # 4. CD時間輸入框
            tk.Label(row_frame, text="秒:").pack(side="left")
            cd_entry = tk.Entry(row_frame, width=5)
            cd_entry.insert(0, "1.0")
            cd_entry.pack(side="left", padx=2)

            self.skills_data.append({
                "enable": enable_var,
                "modifier_combo": modifier_combo,
                "key_entry": key_entry,
                "cd_entry": cd_entry
            })

        # ------------------ 底部狀態顯示 ------------------
        self.status_label = tk.Label(root, text="目前狀態：已停止", fg="red", font=("Arial", 14, "bold"))
        self.status_label.pack(pady=10)

        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # 【新增功能邏輯】：全部取消勾選
    def clear_all_skills(self):
        for skill in self.skills_data:
            skill["enable"].set(False)

    # 【新增功能邏輯】：全部選取勾選
    def select_all_skills(self):
        for skill in self.skills_data:
            skill["enable"].set(True)

    def start_recording(self, entry):
        if self.recording_entry:
            self.recording_entry.configure(bg="#f0f0f0")

        self.recording_entry = entry
        entry.delete(0, tk.END)
        entry.insert(0, "請按鍵...")
        entry.configure(bg="#ffcccc")
        self.root.focus_set()

    def on_press(self, key):
        try:
            if self.recording_entry is not None:
                key_name = ""
                if isinstance(key, keyboard.Key):
                    if key.name in ["ctrl", "ctrl_r", "shift", "shift_r", "alt", "alt_l", "alt_r"]:
                        return
                    key_name = key.name
                elif isinstance(key, keyboard.KeyCode):
                    if key.vk is not None and 96 <= key.vk <= 105:
                        key_name = f"num_{key.vk - 96}"
                    elif key.vk == 107:
                        key_name = "num_add"
                    elif key.vk == 109:
                        key_name = "num_subtract"
                    else:
                        key_name = key.char if key.char else f"vk_{key.vk}"

                if key_name:
                    entry = self.recording_entry
                    self.recording_entry = None

                    def force_overwrite():
                        time.sleep(0.01)
                        entry.delete(0, tk.END)
                        entry.insert(0, key_name.upper())
                        entry.configure(bg="#f0f0f0")

                    threading.Thread(target=force_overwrite, daemon=True).start()
                return

            if key == keyboard.Key.f10:
                self.start_helper()
            elif key == keyboard.Key.f11:
                self.stop_helper()
        except Exception:
            pass

    def start_helper(self):
        if not self.running:
            if self.recording_entry:
                self.recording_entry.configure(bg="#f0f0f0")
                self.recording_entry = None

            self.running = True
            self.status_label.config(text="目前狀態：腳本運行中...", fg="green")

            if self.click_enable.get():
                threading.Thread(target=self.click_loop, daemon=True).start()

            for skill in self.skills_data:
                if skill["enable"].get():
                    mod_value = skill["modifier_combo"].get()
                    key_value = skill["key_entry"].get()
                    cd_value = skill["cd_entry"].get()
                    threading.Thread(target=self.skill_loop, args=(mod_value, key_value, cd_value), daemon=True).start()

    def stop_helper(self):
        if self.running:
            self.running = False
            self.status_label.config(text="目前狀態：已停止", fg="red")

    def click_loop(self):
        try:
            delay = float(self.click_delay_entry.get())
        except ValueError:
            delay = 0.1
        while self.running:
            if self.left_var.get(): self.mouse_controller.click(mouse.Button.left, 1)
            if self.right_var.get(): self.mouse_controller.click(mouse.Button.right, 1)
            time.sleep(delay)

    def skill_loop(self, mod_str, key_str, cd_str):
        try:
            cd = float(cd_str)
            if cd < 0.01: cd = 0.01
        except ValueError:
            cd = 1.0

        key_str = key_str.strip().lower()

        special_keys = {
            "f1": keyboard.Key.f1, "f2": keyboard.Key.f2, "f3": keyboard.Key.f3, "f4": keyboard.Key.f4,
            "f5": keyboard.Key.f5, "f6": keyboard.Key.f6, "f7": keyboard.Key.f7, "f8": keyboard.Key.f8,
            "f9": keyboard.Key.f9, "f10": keyboard.Key.f10, "f11": keyboard.Key.f11, "f12": keyboard.Key.f12,
            "home": keyboard.Key.home, "end": keyboard.Key.end,
            "page_up": keyboard.Key.page_up, "page_down": keyboard.Key.page_down,
            "up": keyboard.Key.up, "down": keyboard.Key.down, "left": keyboard.Key.left, "right": keyboard.Key.right,
            "space": keyboard.Key.space, "enter": keyboard.Key.enter, "tab": keyboard.Key.tab, "esc": keyboard.Key.esc,
            "num_0": keyboard.KeyCode.from_vk(96), "num_1": keyboard.KeyCode.from_vk(97),
            "num_2": keyboard.KeyCode.from_vk(98), "num_3": keyboard.KeyCode.from_vk(99),
            "num_4": keyboard.KeyCode.from_vk(100), "num_5": keyboard.KeyCode.from_vk(101),
            "num_6": keyboard.KeyCode.from_vk(102), "num_7": keyboard.KeyCode.from_vk(103),
            "num_8": keyboard.KeyCode.from_vk(104), "num_9": keyboard.KeyCode.from_vk(105),
            "num_add": keyboard.KeyCode.from_vk(107), "num_subtract": keyboard.KeyCode.from_vk(109)
        }

        target_key = special_keys.get(key_str, key_str)

        mod_keys = {
            "CTRL +": keyboard.Key.ctrl,
            "SHIFT +": keyboard.Key.shift,
            "ALT +": keyboard.Key.alt
        }
        active_mod = mod_keys.get(mod_str, None)

        while self.running:
            try:
                if active_mod:
                    with self.keyboard_controller.pressed(active_mod):
                        self.keyboard_controller.press(target_key)
                        self.keyboard_controller.release(target_key)
                else:
                    self.keyboard_controller.press(target_key)
                    self.keyboard_controller.release(target_key)
            except Exception:
                pass
            time.sleep(cd)

    def on_close(self):
        try:
            self.running = False
            self.listener.stop()
        except Exception:
            pass
        self.root.destroy()
        sys.exit()


if __name__ == "__main__":
    root = tk.Tk()
    app = GameHelperApp(root)
    root.mainloop()
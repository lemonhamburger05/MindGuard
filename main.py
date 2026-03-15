import rumps
import subprocess
import json
import os
from datetime import date
import AppKit

# 动态获取当前 main.py 所在的绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
DATA_FILE = os.path.join(BASE_DIR, "data.json")


class MindGuardApp(rumps.App):
    def __init__(self):
        super(MindGuardApp, self).__init__("🧠 启动中...")

        self.load_config()
        self.load_today_data()

        # --- UI 菜单初始化 ---
        self.status_item = rumps.MenuItem("状态: 检查中...")
        self.stats_item = rumps.MenuItem("今日概览: 加载中...")
        self.unlock_btn = rumps.MenuItem("✅ 完成任务并解锁", callback=self.try_unlock)

        # 组装符合《用户手册》的菜单结构
        self.menu = [
            self.status_item,
            self.stats_item,
            None,
            # 规则设置 (Rules) - 二级菜单
            ["⚙️ 规则设置 (Rules)", [
                rumps.MenuItem("➕ 添加限制应用", callback=self.add_blacklist_app),
                rumps.MenuItem("⏱️ 设定每日配额", callback=self.change_quota),
                rumps.MenuItem("📋 查看当前黑名单", callback=self.view_blacklist)
            ]],
            # 统计 (Statistics)
            rumps.MenuItem("📊 查看专注报告", callback=self.show_statistics),
            None,
            self.unlock_btn,
            None,
            "退出"
        ]

        self.is_locked = False
        self.save_counter = 0

        # ================= 1. 规则设置 (Rules) 模块 =================

    def add_blacklist_app(self, _):
        # 使用原生 AppleScript 弹窗
        script = '''
        tell application "System Events"
            activate
            set dialog_result to display dialog "请输入想限制的应用名称 (例如: TikTok, 微信):" default answer "" buttons {"取消", "添加"} default button "添加"
            return text returned of dialog_result
        end tell
        '''
        try:
            new_app = subprocess.check_output(['osascript', '-e', script]).decode('utf-8').strip()
            if new_app:
                if new_app.lower() not in [app.lower() for app in self.config["blacklist"]]:
                    self.config["blacklist"].append(new_app)
                    self.save_config()
                    rumps.notification("✅ 添加成功", "", f"已将【{new_app}】加入限制名单")
                else:
                    rumps.notification("⚠️ 提示", "", "该应用已在名单中")
        except subprocess.CalledProcessError:
            pass # 用户点击了取消

    def change_quota(self, _):
        current_min = self.config["max_entertainment_seconds"] // 60
        script = f'''
        tell application "System Events"
            activate
            set dialog_result to display dialog "当前配额: {current_min}分钟。\\n请输入新配额 (数字):" default answer "" buttons {"取消", "保存"} default button "保存"
            return text returned of dialog_result
        end tell
        '''
        try:
            new_min_str = subprocess.check_output(['osascript', '-e', script]).decode('utf-8').strip()
            if new_min_str.isdigit():
                self.config["max_entertainment_seconds"] = int(new_min_str) * 60
                self.save_config()
                rumps.notification("✅ 设置成功", "", f"每日配额已更新为 {new_min_str} 分钟")
        except subprocess.CalledProcessError:
            pass

    def view_blacklist(self, _):
        """辅助功能：查看当前被限制的软件列表"""
        AppKit.NSApp.activateIgnoringOtherApps_(True) # 强制获取焦点
        apps_str = "\n".join([f"- {app}" for app in self.config["blacklist"]])
        rumps.alert("📋 当前限制名单", apps_str)

    # ================= 2. 统计 (Statistics) 模块 =================

    def show_statistics(self, _):
        """对应手册第四步：查看你的专注报告"""
        AppKit.NSApp.activateIgnoringOtherApps_(True)  # 强制获取焦点

        f_sec = self.today_data.get("focus_seconds", 0)
        e_sec = self.today_data.get("entertainment_seconds", 0)
        total_sec = f_sec + e_sec

        # 计算专注率
        ratio = 0 if total_sec == 0 else int((f_sec / total_sec) * 100)

        # 将进度条长度缩短为 12，防止在原生弹窗中换行
        bar_length = 12
        focus_bars = int((ratio / 100) * bar_length)
        visual_bar = "█" * focus_bars + "░" * (bar_length - focus_bars)

        report_text = f"📅 日期：{self.today_str}\n\n"
        report_text += f"🟢 专注时长：{f_sec // 60} 分 {f_sec % 60} 秒\n"
        report_text += f"🔴 娱乐时长：{e_sec // 60} 分 {e_sec % 60} 秒\n\n"
        report_text += f"🏆 今日专注率：{ratio}%\n"
        report_text += f"[{visual_bar}]"

        rumps.alert("📊 你的专注报告", report_text)

    # ================= 数据持久化模块 =================

    def load_config(self):
        default_config = {
            "blacklist": ["抖音", "Douyin", "TikTok", "YouTube", "Bilibili", "爱奇艺", "IINA"],
            "max_entertainment_seconds": 15,  # 测试用，你可以通过UI改大
            "required_task": "阅读一篇论文或敲50行代码"
        }
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except Exception:
                self.config = default_config
        else:
            self.config = default_config
            self.save_config()

    def save_config(self):
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception:
            pass

    def load_today_data(self):
        self.today_str = date.today().isoformat()
        self.all_data = {}
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    self.all_data = json.load(f)
            except Exception:
                pass

        if self.today_str not in self.all_data:
            self.all_data[self.today_str] = {"focus_seconds": 0, "entertainment_seconds": 0}
        self.today_data = self.all_data[self.today_str]

    def save_data(self):
        try:
            self.all_data[self.today_str] = self.today_data
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.all_data, f, indent=4, ensure_ascii=False)
        except Exception:
            pass

    # ================= 核心监控逻辑 =================

    @rumps.timer(1)
    def monitor_loop(self, _):
        current_date = date.today().isoformat()
        if current_date != self.today_str:
            self.load_today_data()

        app_name, window_title = self.get_active_window_info()

        is_entertaining = False
        combined_info = f"{app_name} {window_title}".lower()
        for keyword in self.config["blacklist"]:
            if keyword.lower() in combined_info:
                is_entertaining = True
                break

        if is_entertaining:
            self.handle_entertainment(app_name)
        else:
            self.handle_learning()

        f_min = self.today_data["focus_seconds"] // 60
        e_min = self.today_data["entertainment_seconds"] // 60
        self.stats_item.title = f"今日概览: 🟢专注 {f_min}分 | 🔴娱乐 {e_min}分"

        self.save_counter += 1
        if self.save_counter >= 3:
            self.save_data()
            self.save_counter = 0

    def handle_entertainment(self, app_name):
        max_time = self.config["max_entertainment_seconds"]
        current_usage = self.today_data["entertainment_seconds"]

        if self.is_locked or current_usage >= max_time:
            if not self.is_locked:
                self.lock_system()
            self.title = "🔒 已锁定"
            self.status_item.title = "状态: ⛔️ 禁止访问"
            self.hide_app(app_name)
        else:
            self.today_data["entertainment_seconds"] += 1
            remain = max_time - self.today_data["entertainment_seconds"]
            self.title = f"👀 摸鱼中 (余 {remain}s)"
            self.status_item.title = f"状态: 正在看 {app_name}"

    def handle_learning(self):
        if not self.is_locked:
            self.today_data["focus_seconds"] += 1
            self.title = "🧠 专注中"
            self.status_item.title = "状态: 🟢 学习/工作中"

    def lock_system(self):
        self.is_locked = True
        try:
            rumps.notification("配额耗尽！", "今日娱乐时间已达上限", f"请完成任务：{self.config['required_task']}")
        except RuntimeError:
            pass
        self.save_data()

    def hide_app(self, app_name):
        script = f'tell application "System Events" to set visible of process "{app_name}" to false'
        try:
            subprocess.run(['osascript', '-e', script], check=False)
        except:
            pass

    def try_unlock(self, _):
        if not self.is_locked:
            AppKit.NSApp.activateIgnoringOtherApps_(True)
            rumps.alert("提示", "当前未锁定，无需解锁。")
            return

        AppKit.NSApp.activateIgnoringOtherApps_(True)  # 强制获取焦点
        window = rumps.Window(
            message=f"需完成任务：【{self.config['required_task']}】\n（解锁将额外赠送30%的时间）",
            title="任务检查",
            ok="完成",
            cancel="取消"
        )
        response = window.run()
        if response.clicked and len(response.text) > 0:
            self.is_locked = False
            bonus_time = int(self.config["max_entertainment_seconds"] * 0.3)
            self.today_data["entertainment_seconds"] = max(0, self.today_data["entertainment_seconds"] - bonus_time)
            self.save_data()
            self.title = "🧠 已解锁"
            try:
                rumps.notification("解锁成功", "继续加油", f"已为你恢复 {bonus_time} 秒额度。")
            except RuntimeError:
                pass
        elif response.clicked:
            rumps.alert("拒绝", "请输入具体的完成情况！")

    def get_active_window_info(self):
        try:
            script_app = 'tell application "System Events" to get name of first application process whose frontmost is true'
            res_app = subprocess.check_output(['osascript', '-e', script_app], stderr=subprocess.STDOUT).decode(
                'utf-8').strip()
            return res_app, ""
        except Exception:
            return "Unknown", ""


if __name__ == "__main__":
    MindGuardApp().run()
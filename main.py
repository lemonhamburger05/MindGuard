import rumps
import subprocess
import time


class MindGuardApp(rumps.App):
    def __init__(self):
        # 初始化，默认标题用 Emoji
        super(MindGuardApp, self).__init__("🧠 准备中...")

        self.status_item = rumps.MenuItem("当前状态: 检查中...")
        self.timer_item = rumps.MenuItem("娱乐时长: 0秒")
        self.unlock_btn = rumps.MenuItem("✅ 完成任务并解锁", callback=self.try_unlock)

        self.menu = [self.status_item, self.timer_item, None, self.unlock_btn, None, "退出"]

        # --- 配置区 ---
        # 既包含中文名也包含英文进程名
        self.blacklist = ["抖音", "Douyin", "TikTok", "YouTube", "Bilibili", "爱奇艺", "IINA"]
        self.MAX_ENTERTAINMENT_SECONDS = 300

        # --- 状态区 ---
        self.current_usage = 0
        self.is_locked = False
        self.required_task = "背诵5个单词"

    @rumps.timer(1)
    def monitor_loop(self, _):
        # 1. 获取信息
        app_name, window_title = self.get_active_window_info()

        # 调试打印：看看到底抓到了什么
        print(f"检测中 -> App: [{app_name}] | Title: [{window_title}]")

        # 2. 判断逻辑
        is_entertaining = False

        # 检查1: App 名字本身是否在黑名单 (针对抖音桌面版)
        for keyword in self.blacklist:
            if keyword.lower() in app_name.lower():
                is_entertaining = True
                break

        # 检查2: 如果App名字没中，检查窗口标题 (针对浏览器看视频)
        if not is_entertaining:
            combined_info = f"{window_title}"
            for keyword in self.blacklist:
                if keyword.lower() in combined_info.lower():
                    is_entertaining = True
                    break

        # 3. 执行动作
        if is_entertaining:
            self.handle_entertainment(app_name)
        else:
            self.handle_learning()

    def handle_entertainment(self, app_name):
        if self.is_locked:
            # 锁定状态：修改文字标题，不改icon避免报错
            self.title = "🔒 已锁定"
            self.status_item.title = "状态: ⛔️ 禁止访问"

            # 强制隐藏该应用
            print(f"尝试隐藏: {app_name}")
            self.hide_app(app_name)

        else:
            self.current_usage += 1
            self.title = f"👀 摸鱼 {self.current_usage}s"
            self.status_item.title = f"状态: 正在看 {app_name}"
            self.timer_item.title = f"已用: {self.current_usage}/{self.MAX_ENTERTAINMENT_SECONDS}秒"

            if self.current_usage >= self.MAX_ENTERTAINMENT_SECONDS:
                self.lock_system()

    def handle_learning(self):
        if not self.is_locked:
            # 只有没锁定时才恢复状态
            self.title = "🧠 学习中"
            self.status_item.title = "状态: 🟢 专注"
            # 可选：学习时慢慢恢复娱乐时间
            # if self.current_usage > 0: self.current_usage -= 1

    def lock_system(self):
        self.is_locked = True
        # 发送通知
        rumps.notification("时间到！", "休息时间结束", f"请完成任务：{self.required_task}")
        # 确保解锁按钮是激活状态
        self.unlock_btn.state = 0

    def hide_app(self, app_name):
        # AppleScript 强制隐藏
        script = f'tell application "System Events" to set visible of process "{app_name}" to false'
        try:
            subprocess.run(['osascript', '-e', script], check=False)
        except Exception as e:
            print(f"隐藏失败: {e}")

    def try_unlock(self, _):
        if not self.is_locked:
            rumps.alert("提示", "当前未锁定，无需解锁。")
            return

        window = rumps.Window(
            message=f"需完成任务：【{self.required_task}】",
            title="任务检查",
            ok="完成",
            cancel="取消"
        )
        response = window.run()

        if response.clicked:
            if len(response.text) > 0:
                self.is_locked = False
                self.current_usage = 0
                self.title = "🧠 已解锁"
                rumps.notification("解锁成功", "继续加油", "")
            else:
                rumps.alert("拒绝", "请输入具体的完成情况！")

    def get_active_window_info(self):
        try:
            # 获取 App 名字 (核心步骤)
            script_app = 'tell application "System Events" to get name of first application process whose frontmost is true'
            # 使用 subprocess.check_output 并捕获错误
            res_app = subprocess.check_output(['osascript', '-e', script_app], stderr=subprocess.STDOUT).decode(
                'utf-8').strip()

            # 获取标题 (辅助)
            title = ""
            # 如果是浏览器，尝试获取 Tab 标题
            if res_app in ["Google Chrome", "Microsoft Edge", "Safari"]:
                # 这里省略具体的浏览器脚本以简化排错，先保证能抓到 App 名字
                pass

            return res_app, title

        except subprocess.CalledProcessError as e:
            # 这里是最关键的调试信息！
            error_msg = e.output.decode('utf-8').strip() if e.output else "无详细错误"
            print(f"⚠️ 获取窗口信息失败: {error_msg}")
            return "Unknown", ""
        except Exception as e:
            print(f"⚠️ 未知错误: {e}")
            return "Unknown", ""


if __name__ == "__main__":
    MindGuardApp().run()
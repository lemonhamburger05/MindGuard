# 🛡️ MindGuard 

![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey.svg)
![Language](https://img.shields.io/badge/Language-Swift%20%7C%20Objective--C-orange.svg)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

MindGuard 是一款专为 macOS 打造的效率与屏幕时间管理应用。在这个充满信息诱惑的时代，MindGuard 旨在帮助用户精准监控并限制在泛娱乐应用（如 TikTok、社交媒体等）上消耗的时间，从而夺回注意力控制权，保持深度专注。

## ✨ 核心特性 (Features)

- **⏱️ 精准的时间追踪**：在后台静默运行，精准记录各个目标应用的前台运行时间。
- **🛑 自定义限制规则**：支持为特定的娱乐应用（如 TikTok、特定浏览器标签页）设置每日时间配额。
- **🛡️ 强力干预机制**：当应用使用时间达到设定的阈值时，自动触发提醒或限制访问，打破“无意识滑动”的习惯。
- **📊 数据可视化报表**：直观展示每日/每周的屏幕使用数据，帮助你了解自己的数字习惯。
- **⚡️ 原生且轻量**：基于 Swift 和 Objective-C 开发，深度融合 macOS 原生体验，极低系统资源占用。

---

## 🚀 安装指南 (Installation)

### 选项一：直接下载运行 (推荐)
1. 访问本仓库的 [Releases](https://github.com/lemonhamburger05/MindGuard/releases) 页面。
2. 下载最新版本的 `MindGuard.dmg` 或 `MindGuard.app.zip`。
3. 解压并将其拖入 macOS 的 `应用程序 (Applications)` 文件夹中。
4. 首次打开时，如果遇到系统安全提示，请前往“系统偏好设置 -> 隐私与安全性”中允许运行。

### 选项二：通过源码编译
1. 克隆本仓库到本地：
   ```bash
   git clone [https://github.com/lemonhamburger05/MindGuard.git](https://github.com/lemonhamburger05/MindGuard.git)
2. 使用 Xcode 打开 MindGuard.xcodeproj（或 .xcworkspace）。
3. 选择你的 Mac 作为运行目标 (Target)。
4. 点击 Cmd + R 编译并运行。

### 📖 详细用户手册 (User Manual)
欢迎使用 MindGuard！为了让应用完美发挥作用，请在首次使用时按照以下步骤进行配置：

## 第一步：授予必要权限
MindGuard 需要获取您当前正在使用的应用状态才能进行计时。
   1. 启动 MindGuard 后，应用会提示需要辅助功能 (Accessibility) 或 屏幕录制 (Screen Recording) 权限。
   2. 点击提示跳转至“系统偏好设置 -> 隐私与安全性”。
   3. 找到对应的权限选项，解锁并勾选 MindGuard。(注：MindGuard 仅读取窗口标题与包名，绝不会收集或上传您的隐私数据。)

## 第二步：添加监控与限制应用
1. 点击系统状态栏（菜单栏）右上角的 MindGuard 🛡️ 图标，打开主面板。
2. 进入 “规则设置 (Rules)”。
3. 点击 "+" 号，从列表中选择你想要限制的应用程序（例如：TikTok, 微信, 某些视频播放器）。
   
## 第三步：设定每日配额
1. 在已添加的应用旁，设置你每天允许自己使用的最大时间（例如：30分钟）。
2. 你还可以设置工作日/休息日的不同规则。
3. 开启“严格模式”后，一旦超时，该应用将被强制隐藏或退出，在次日零点前无法再次长时间打开。

## 第四步：查看你的专注报告
1. 在主面板中点击 “统计 (Statistics)”。
2. 这里会显示你今日的专注时间与娱乐时间占比。
3. 通过回顾每周的数据图表，你可以清晰地看到自己注意力的改善轨迹。

### 🛠️ 技术栈 (Tech Stack)
# 核心逻辑: Swift
# 底层接口与兼容: Objective-C
# UI 框架: AppKit / SwiftUI
# 系统 API: 深度调用 NSWorkspace, NSRunningApplication 等 macOS 原生 API 进行状态监测。

### 🤝 参与贡献 (Contributing)
欢迎提交 Issue 报告 Bug 或提出新功能建议！如果你想为 MindGuard 贡献代码，请：
   1. Fork 本仓库
   2. 创建你的特性分支 (git checkout -b feature/AmazingFeature)
   3. 提交你的更改 (git commit -m 'Add some AmazingFeature')
   4. 推送到分支 (git push origin feature/AmazingFeature)
   5. 发起一个 Pull Request

### 📄 许可证 (License)
本项目采用 MIT License 开源许可证。

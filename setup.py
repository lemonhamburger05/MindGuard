from setuptools import setup

APP = ['main.py']  # 你的主程序文件名
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': '', # 如果你有 .icns 图标文件，可以填在这里，比如 'icon.icns'
    'plist': {
        'LSUIElement': True, # 关键：隐藏 Dock 图标，只在菜单栏显示
        'CFBundleName': 'MindGuard',
        'CFBundleDisplayName': 'MindGuard',
        'CFBundleIdentifier': "com.student.mindguard", # 唯一的 ID
        'CFBundleVersion': "0.1.0",
        'CFBundleShortVersionString': "0.1.0",
        'NSHumanReadableCopyright': "Copyright © 2026, Cognitive Science Student",
    },
    'packages': ['rumps'], # 确保把依赖库打包进去
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
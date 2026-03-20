[app]

# 应用名称
title = 数字积木

# 包名
package.name = numberblocks
package.domain = org.example

# 源代码目录
source.dir = .

# 源代码包含的文件类型
source.include_exts = py,png,jpg,kv,atlas,json

# 版本
version = 1.0

# 依赖
requirements = python3,kivy,cython

# 屏幕方向（竖屏）
orientation = portrait

# 全屏
fullscreen = 0

# Android API
android.api = 33
android.minapi = 21

# 权限
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# 功能
android.features = android.hardware.screen.portrait

# 图标 (512x512 PNG)
# icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
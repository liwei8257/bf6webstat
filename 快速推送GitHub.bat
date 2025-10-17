@echo off
chcp 65001 >nul
echo ========================================
echo   推送项目到GitHub
echo ========================================
echo.

REM 检查是否已初始化Git
if not exist ".git" (
    echo [1/4] 初始化Git仓库...
    git init
    echo.
)

echo [2/4] 添加所有文件...
git add .
echo.

echo [3/4] 提交更改...
set /p commit_msg="请输入提交信息（直接回车使用默认）: "
if "%commit_msg%"=="" set commit_msg=Update BF6 Stats System

git commit -m "%commit_msg%"
echo.

echo [4/4] 推送到GitHub...
echo.
echo ⚠️  如果这是第一次推送，请先在GitHub创建仓库：
echo    https://github.com/liwei8257/bf6webstat.git
echo.
set /p repo_url="请输入GitHub仓库URL（例如：https://github.com/username/bf6stat.git）: "

REM 检查是否已添加remote
git remote | findstr origin >nul
if errorlevel 1 (
    git remote add origin %repo_url%
) else (
    git remote set-url origin %repo_url%
)

git branch -M main
git push -u origin main

echo.
echo ========================================
if errorlevel 1 (
    echo ❌ 推送失败！
    echo.
    echo 可能的原因：
    echo 1. 仓库URL不正确
    echo 2. 需要GitHub认证
    echo 3. 仓库不存在
    echo.
    echo 建议：使用GitHub Desktop更简单
    echo 下载：https://desktop.github.com/
) else (
    echo ✅ 推送成功！
    echo.
    echo 🎉 项目已上传到GitHub
    echo 📍 仓库地址：%repo_url%
    echo.
    echo 下一步：在Render.com部署
    echo 访问：https://render.com
)
echo ========================================
echo.
pause


@echo off
chcp 65001 >nul
echo ========================================
echo   BF6 玩家数据统计系统
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [1/3] 检查依赖...
pip show Flask >nul 2>&1
if errorlevel 1 (
    echo [提示] 正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
) else (
    echo [OK] 依赖已安装
)

echo.
echo [2/3] 检查配置文件...
if not exist "players.json" (
    echo [警告] 未找到 players.json，请先配置玩家列表
    pause
    exit /b 1
)
echo [OK] 配置文件存在

echo.
echo [3/3] 启动Web应用...
echo.
echo ========================================
echo   服务启动成功！
echo   访问地址: http://localhost:5000
echo   按 Ctrl+C 停止服务
echo ========================================
echo.

python app.py


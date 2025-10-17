@echo off
chcp 65001 >nul
echo ========================================
echo   更新BF6玩家数据
echo ========================================
echo.

echo [1/3] 导出数据...
py export_data.py

if errorlevel 1 (
    echo.
    echo ❌ 数据导出失败！
    pause
    exit /b 1
)

echo.
echo [2/3] 提交到Git...
git add static/players_data.json
git commit -m "Update player data - %date% %time%"

echo.
echo [3/3] 推送到GitHub...
git push

if errorlevel 1 (
    echo.
    echo ⚠️  推送失败，请检查网络连接
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ 数据更新完成！
echo.
echo Render会自动部署新数据
echo 大约1-2分钟后生效
echo ========================================
echo.
pause


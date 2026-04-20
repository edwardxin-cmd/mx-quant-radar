@echo off
title MX-Deployer
color 0A
cd /d "F:\mx_radar_web"

echo --- Ready to deploy ---
:: 注意下面的那个点(.)，它代表将 html 和所有 json 数据全部打包！
git add .
git commit -m "Auto Update Dashboard and Data"
git push origin main

echo.
echo --- DONE ---
echo If error says main does not match, change main to master in script.
pause
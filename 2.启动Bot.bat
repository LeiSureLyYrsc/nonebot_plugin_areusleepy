@echo off
echo 正在启动 Bot...
pdm run nb run
echo Bot 已停止, 返回代码: %ERRORLEVEL%
pause
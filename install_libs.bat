@echo off
chcp 65001
title 安装脚本
echo 安装依赖中, 请等待...
pip install pdm
pdm install
echo 安装完成!
pause

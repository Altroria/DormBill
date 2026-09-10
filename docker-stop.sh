#!/bin/bash
#
# DormBill 停止脚本 (Linux/macOS)
# 使用方法: ./docker-stop.sh
#

echo "======================================"
echo "  DormBill Docker 停止脚本"
echo "======================================"
echo ""

echo "正在停止服务 ..."
docker-compose stop

echo ""
echo "======================================"
echo "  服务已停止"
echo "======================================"
echo ""
echo "如需再次启动，请运行: ./docker-start.sh"
echo ""

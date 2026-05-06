#!/bin/bash

set -e

echo "=========================================="
echo "  📚 Picture English 启动脚本"
echo "=========================================="
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装 Python3"
    exit 1
fi

# 1. 安装 Python 依赖
echo "📦 安装 Python 依赖..."
pip install -r requirements.txt

# 2. 检查 Node.js 是否安装，如果安装则构建前端
if command -v npm &> /dev/null; then
    echo ""
    echo "📦 安装 Node.js 依赖..."
    npm install
    
    echo ""
    echo "🔨 构建前端..."
    npm run build
else
    echo ""
    echo "⚠️  Node.js 未安装，跳过前端构建"
    echo "   如果 dist 目录不存在，请先安装 Node.js 并运行 npm run build"
fi

# 3. 启动服务器
echo ""
echo "🚀 启动服务器..."
echo "🌐 访问地址: http://localhost:8000/"
echo ""
python3 server.py

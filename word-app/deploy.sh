#!/bin/bash

#==========================================
#  📚 Picture English - 环境部署和启动脚本
#==========================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "=========================================="
echo "  📚 Picture English 部署脚本"
echo "=========================================="
echo ""

# 检查 Python
echo "🔍 检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 未安装${NC}"
    echo "   请先安装 Python3: https://www.python.org/downloads/"
    exit 1
fi
echo -e "${GREEN}✅ Python3 已安装: $(python3 --version)${NC}"

# 1. 安装 Python 依赖
echo ""
echo "📦 安装 Python 依赖..."
pip3 install flask flask-cors requests -q 2>/dev/null || pip install flask flask-cors requests -q
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Python 依赖安装成功${NC}"
else
    echo -e "${YELLOW}⚠️  Python 依赖安装完成（可能有警告）${NC}"
fi

# 2. 检查 Node.js（可选）
echo ""
echo "🔍 检查 Node.js 环境..."
if command -v npm &> /dev/null; then
    echo -e "${GREEN}✅ Node.js 已安装: $(node --version)${NC}"
    
    HAS_NODE=true
else
    echo -e "${YELLOW}⚠️  Node.js 未安装，跳过前端构建${NC}"
    HAS_NODE=false
fi

# 3. 前端构建（可选）
if [ "$HAS_NODE" = true ]; then
    echo ""
    echo "🔍 检查 dist 目录..."
    if [ ! -d "dist" ] || [ ! -f "dist/index.html" ]; then
        echo "📦 安装 Node.js 依赖..."
        npm install --silent
        
        echo "🔨 构建前端..."
        npm run build
        
        echo -e "${GREEN}✅ 前端构建成功${NC}"
    else
        echo -e "${GREEN}✅ dist 目录已存在，跳过构建${NC}"
    fi
else
    echo ""
    echo "⚠️  跳过前端构建"
    if [ ! -d "dist" ] || [ ! -f "dist/index.html" ]; then
        echo -e "${YELLOW}⚠️  警告: dist 目录不存在，应用可能无法正常运行${NC}"
        echo "   请安装 Node.js 并运行: npm install && npm run build"
    fi
fi

# 4. 清理旧进程
echo ""
echo "🧹 清理旧进程..."
if lsof -ti:8000 &> /dev/null; then
    echo "   停止端口 8000 上的旧进程..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    sleep 1
fi

# 5. 启动服务器
echo ""
echo "🚀 启动服务器..."
echo "🌐 访问地址: http://localhost:8000/"
echo "📝 按 Ctrl+C 停止服务器"
echo ""
echo "=========================================="

# 启动 Flask 服务器
python3 server.py

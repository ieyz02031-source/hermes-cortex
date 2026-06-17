#!/bin/bash
# Hermes Cortex 初始化脚本
# 在每次会话开始时运行，确保环境健康

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
VAULT_DIR="D:/ObsidianVault"

echo "🧠 Hermes Cortex 初始化..."
echo "================================"

# 1. 检查目录结构
echo "📁 检查目录结构..."
if [ ! -d "$VAULT_DIR" ]; then
    echo "❌ Obsidian Vault 不存在: $VAULT_DIR"
    exit 1
fi
echo "✅ Obsidian Vault 存在"

# 2. 检查关键文件
echo "📄 检查关键文件..."
for file in "$SKILL_DIR/SKILL.md" "$SKILL_DIR/feature_list.json" "$SKILL_DIR/progress.md"; do
    if [ ! -f "$file" ]; then
        echo "❌ 缺少文件: $file"
        exit 1
    fi
done
echo "✅ 关键文件存在"

# 3. 检查脚本
echo "🔧 检查脚本..."
for script in hot_cache.py semantic_index.py build_graph.py retrieve.py maintain.py evolve.py auto_optimize.py; do
    if [ ! -f "$SKILL_DIR/scripts/$script" ]; then
        echo "❌ 缺少脚本: $script"
        exit 1
    fi
done
echo "✅ 脚本完整"

# 4. 检查 Python 环境
echo "🐍 检查 Python 环境..."
if ! command -v python &> /dev/null; then
    echo "❌ Python 未安装"
    exit 1
fi
echo "✅ Python 存在: $(python --version)"

# 5. 检查数据库
echo "💾 检查数据库..."
DB_FILE="$VAULT_DIR/.hermes_brain.db"
if [ ! -f "$DB_FILE" ]; then
    echo "⚠️ 数据库不存在，将创建新的"
    python "$SKILL_DIR/scripts/semantic_index.py" index
else
    echo "✅ 数据库存在"
fi

# 6. 更新热缓存
echo "🔥 更新热缓存..."
python "$SKILL_DIR/scripts/hot_cache.py" > /dev/null 2>&1
echo "✅ 热缓存更新完成"

# 7. 检查孤立笔记
echo "🔍 检查孤立笔记..."
ISOLATED=$(python "$SKILL_DIR/scripts/maintain.py" isolated 2>/dev/null | grep -c "isolated" || echo "0")
if [ "$ISOLATED" -gt 20 ]; then
    echo "⚠️ 孤立笔记过多 ($ISOLATED)，建议清理"
else
    echo "✅ 孤立笔记正常 ($ISOLATED)"
fi

# 8. 显示状态
echo ""
echo "================================"
echo "✅ Hermes Cortex 初始化完成"
echo "================================"
echo ""
echo "📊 状态摘要："
python "$SKILL_DIR/scripts/maintain.py" stats 2>/dev/null | head -10
echo ""

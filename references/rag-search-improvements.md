# RAG搜索改进（借鉴he-wiki-rag）

## 来源
GitHub: https://github.com/liuhe37186/he-wiki-rag

## 核心改进

### 1. 章节树切块
- 工具：D:/Hermes/tools/chapter_tree.py
- 按Markdown标题层级切块，保留父子关系
- 每个节点包含：node_id, title, breadcrumb, parent_id, children_ids

### 2. 三阶段检索
- 工具：D:/Hermes/tools/three_stage_retrieval.py
- Stage 1: 向量检索（语义相似度）
- Stage 2: BM25检索（关键词匹配）
- Stage 3: RRF融合（加权倒数排名融合）

### 3. 自动查询扩展
- 工具：D:/Hermes/tools/query_expander.py
- 基于Embedding相似度自动发现同义词
- 例："切块" → "chunking", "分块", "切分"

### 4. 统一搜索接口
- 工具：D:/Hermes/tools/unified_search.py
- 融合章节树+三阶段检索+查询扩展

## 使用方法

```bash
# 构建索引
python D:/Hermes/tools/unified_search.py --build --vault D:/ObsidianVault

# 搜索
python D:/Hermes/tools/unified_search.py "RAG切块策略"

# 搜索（禁用扩展）
python D:/Hermes/tools/unified_search.py "RAG" --no-expand
```

## 与现有系统对比

| 对比 | 之前 | 现在 |
|------|------|------|
| 切块 | 按段落 | 章节树 |
| 检索 | FTS5 | 向量+BM25+RRF |
| 扩展 | 无 | 自动同义词 |

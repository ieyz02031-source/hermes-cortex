#!/usr/bin/env python3
"""
评估者评分表管理器
实现 AHE 可观测性驱动的评估者评分表机制
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 配置
SKILL_DIR = Path(__file__).parent.parent
EVALUATOR_RUBRICS_DIR = SKILL_DIR / "evaluator_rubrics"
PROGRESS_FILE = SKILL_DIR / "progress.md"

# 默认评分维度
DEFAULT_DIMENSIONS = {
    "code_correctness": {
        "name": "代码正确性",
        "description": "代码是否正确实现了功能",
        "levels": {
            "A": {"score": 4, "description": "所有测试通过"},
            "B": {"score": 3, "description": "主流程通过"},
            "C": {"score": 2, "description": "部分通过"},
            "D": {"score": 1, "description": "构建失败"}
        }
    },
    "architecture_compliance": {
        "name": "架构合规性",
        "description": "代码是否符合架构规范",
        "levels": {
            "A": {"score": 4, "description": "完全合规"},
            "B": {"score": 3, "description": "轻微偏差"},
            "C": {"score": 2, "description": "明显偏差"},
            "D": {"score": 1, "description": "严重违规"}
        }
    },
    "test_coverage": {
        "name": "测试覆盖",
        "description": "测试是否充分",
        "levels": {
            "A": {"score": 4, "description": "主流程+边界"},
            "B": {"score": 3, "description": "仅主流程"},
            "C": {"score": 2, "description": "仅骨架"},
            "D": {"score": 1, "description": "无测试"}
        }
    },
    "performance": {
        "name": "性能",
        "description": "代码性能是否达标",
        "levels": {
            "A": {"score": 4, "description": "超出预期"},
            "B": {"score": 3, "description": "符合预期"},
            "C": {"score": 2, "description": "略低于预期"},
            "D": {"score": 1, "description": "严重不足"}
        }
    },
    "security": {
        "name": "安全性",
        "description": "代码是否安全",
        "levels": {
            "A": {"score": 4, "description": "无安全漏洞"},
            "B": {"score": 3, "description": "低风险漏洞"},
            "C": {"score": 2, "description": "中等风险漏洞"},
            "D": {"score": 1, "description": "高风险漏洞"}
        }
    }
}

class EvaluatorRubric:
    """评估者评分类"""
    
    def __init__(self, rubric_id: str, title: str, dimensions: Dict):
        self.rubric_id = rubric_id
        self.title = title
        self.dimensions = dimensions
        self.created_at = datetime.now().isoformat()
        self.evaluations = []
    
    def to_dict(self) -> Dict:
        return {
            "rubric_id": self.rubric_id,
            "title": self.title,
            "dimensions": self.dimensions,
            "created_at": self.created_at,
            "evaluations": self.evaluations
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'EvaluatorRubric':
        rubric = cls(
            rubric_id=data["rubric_id"],
            title=data["title"],
            dimensions=data["dimensions"]
        )
        rubric.created_at = data["created_at"]
        rubric.evaluations = data.get("evaluations", [])
        return rubric

class EvaluatorRubricManager:
    """评估者评分表管理器"""
    
    def __init__(self):
        self.rubrics_dir = EVALUATOR_RUBRICS_DIR
        self.rubrics_dir.mkdir(exist_ok=True)
    
    def create_rubric(self, title: str, dimensions: Optional[Dict] = None) -> EvaluatorRubric:
        """创建新的评估者评分表"""
        rubric_id = f"rubric_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if dimensions is None:
            dimensions = DEFAULT_DIMENSIONS
        
        rubric = EvaluatorRubric(
            rubric_id=rubric_id,
            title=title,
            dimensions=dimensions
        )
        
        # 保存到文件
        rubric_file = self.rubrics_dir / f"{rubric_id}.json"
        with open(rubric_file, 'w', encoding='utf-8') as f:
            json.dump(rubric.to_dict(), f, indent=2, ensure_ascii=False)
        
        # 更新进度文件
        self._update_progress(rubric)
        
        return rubric
    
    def get_rubric(self, rubric_id: str) -> Optional[EvaluatorRubric]:
        """获取评估者评分表"""
        rubric_file = self.rubrics_dir / f"{rubric_id}.json"
        if not rubric_file.exists():
            return None
        
        with open(rubric_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return EvaluatorRubric.from_dict(data)
    
    def list_rubrics(self) -> List[EvaluatorRubric]:
        """列出所有评估者评分表"""
        rubrics = []
        for rubric_file in self.rubrics_dir.glob("*.json"):
            with open(rubric_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            rubric = EvaluatorRubric.from_dict(data)
            rubrics.append(rubric)
        
        return rubrics
    
    def evaluate(self, rubric_id: str, task_id: str, 
                scores: Dict[str, str], evidence: Dict[str, str]) -> bool:
        """执行评估"""
        rubric = self.get_rubric(rubric_id)
        if not rubric:
            return False
        
        # 验证评分
        for dimension, score in scores.items():
            if dimension not in rubric.dimensions:
                return False
            if score not in rubric.dimensions[dimension]["levels"]:
                return False
        
        # 计算总分
        total_score = 0
        for dimension, score in scores.items():
            total_score += rubric.dimensions[dimension]["levels"][score]["score"]
        
        average_score = total_score / len(scores)
        
        # 创建评估记录
        evaluation = {
            "task_id": task_id,
            "scores": scores,
            "evidence": evidence,
            "total_score": total_score,
            "average_score": average_score,
            "evaluated_at": datetime.now().isoformat()
        }
        
        rubric.evaluations.append(evaluation)
        
        # 保存到文件
        rubric_file = self.rubrics_dir / f"{rubric_id}.json"
        with open(rubric_file, 'w', encoding='utf-8') as f:
            json.dump(rubric.to_dict(), f, indent=2, ensure_ascii=False)
        
        return True
    
    def get_evaluation_summary(self, rubric_id: str) -> Dict:
        """获取评估摘要"""
        rubric = self.get_rubric(rubric_id)
        if not rubric:
            return {}
        
        if not rubric.evaluations:
            return {"total_evaluations": 0}
        
        # 计算平均分
        total_scores = []
        dimension_scores = {}
        
        for evaluation in rubric.evaluations:
            total_scores.append(evaluation["average_score"])
            
            for dimension, score in evaluation["scores"].items():
                if dimension not in dimension_scores:
                    dimension_scores[dimension] = []
                dimension_scores[dimension].append(
                    rubric.dimensions[dimension]["levels"][score]["score"]
                )
        
        summary = {
            "total_evaluations": len(rubric.evaluations),
            "average_score": sum(total_scores) / len(total_scores),
            "dimension_averages": {}
        }
        
        for dimension, scores in dimension_scores.items():
            summary["dimension_averages"][dimension] = {
                "name": rubric.dimensions[dimension]["name"],
                "average": sum(scores) / len(scores),
                "min": min(scores),
                "max": max(scores)
            }
        
        return summary
    
    def _update_progress(self, rubric: EvaluatorRubric):
        """更新进度文件"""
        if not PROGRESS_FILE.exists():
            return
        
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 添加评估者评分表记录
        rubric_record = f"""
## 评估者评分表: {rubric.title}
- **ID**: {rubric.rubric_id}
- **创建时间**: {rubric.created_at}
- **维度数**: {len(rubric.dimensions)}
"""
        
        # 追加到进度文件
        with open(PROGRESS_FILE, 'a', encoding='utf-8') as f:
            f.write(rubric_record)

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python evaluator_rubric.py <command> [args]")
        print("命令:")
        print("  create <title>")
        print("  list")
        print("  show <rubric_id>")
        print("  evaluate <rubric_id> <task_id> <scores> <evidence>")
        print("  summary <rubric_id>")
        return
    
    manager = EvaluatorRubricManager()
    command = sys.argv[1]
    
    if command == "create":
        if len(sys.argv) < 3:
            print("用法: python evaluator_rubric.py create <title>")
            return
        
        title = sys.argv[2]
        rubric = manager.create_rubric(title)
        print(f"✅ 创建评估者评分表: {rubric.rubric_id}")
        print(f"   标题: {rubric.title}")
        print(f"   维度数: {len(rubric.dimensions)}")
    
    elif command == "list":
        rubrics = manager.list_rubrics()
        
        print(f"📋 评估者评分表列表 ({len(rubrics)} 个):")
        for rubric in rubrics:
            print(f"   - {rubric.rubric_id}: {rubric.title}")
    
    elif command == "show":
        if len(sys.argv) < 3:
            print("用法: python evaluator_rubric.py show <rubric_id>")
            return
        
        rubric_id = sys.argv[2]
        rubric = manager.get_rubric(rubric_id)
        
        if not rubric:
            print(f"❌ 评分表不存在: {rubric_id}")
            return
        
        print(f"📄 评估者评分表详情:")
        print(f"   ID: {rubric.rubric_id}")
        print(f"   标题: {rubric.title}")
        print(f"   创建时间: {rubric.created_at}")
        print(f"   维度数: {len(rubric.dimensions)}")
        
        print(f"   维度详情:")
        for dim_id, dim in rubric.dimensions.items():
            print(f"     - {dim['name']}: {dim['description']}")
            for level, info in dim['levels'].items():
                print(f"       {level}: {info['description']} ({info['score']}分)")
    
    elif command == "evaluate":
        if len(sys.argv) < 6:
            print("用法: python evaluator_rubric.py evaluate <rubric_id> <task_id> <scores> <evidence>")
            print("示例: python evaluator_rubric.py evaluate rubric_20260615 task_1 'code_correctness:A,architecture_compliance:B' 'code_correctness:所有测试通过,architecture_compliance:符合规范'")
            return
        
        rubric_id = sys.argv[2]
        task_id = sys.argv[3]
        scores_str = sys.argv[4]
        evidence_str = sys.argv[5]
        
        # 解析评分
        scores = {}
        for item in scores_str.split(","):
            dimension, score = item.split(":")
            scores[dimension] = score
        
        # 解析证据
        evidence = {}
        for item in evidence_str.split(","):
            dimension, evid = item.split(":")
            evidence[dimension] = evid
        
        if manager.evaluate(rubric_id, task_id, scores, evidence):
            print(f"✅ 执行评估: {task_id}")
            print(f"   评分表: {rubric_id}")
            for dimension, score in scores.items():
                print(f"   {dimension}: {score}")
        else:
            print(f"❌ 评估失败")
    
    elif command == "summary":
        if len(sys.argv) < 3:
            print("用法: python evaluator_rubric.py summary <rubric_id>")
            return
        
        rubric_id = sys.argv[2]
        summary = manager.get_evaluation_summary(rubric_id)
        
        if not summary:
            print(f"❌ 评分表不存在或无评估记录")
            return
        
        print(f"📊 评估摘要:")
        print(f"   总评估数: {summary['total_evaluations']}")
        
        if summary['total_evaluations'] > 0:
            print(f"   平均分: {summary['average_score']:.2f}")
            print(f"   维度平均分:")
            for dimension, stats in summary['dimension_averages'].items():
                print(f"     - {stats['name']}: {stats['average']:.2f} (最小: {stats['min']}, 最大: {stats['max']})")
    
    else:
        print(f"❌ 未知命令: {command}")

if __name__ == "__main__":
    main()

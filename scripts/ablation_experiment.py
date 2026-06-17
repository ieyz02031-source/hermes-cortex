#!/usr/bin/env python3
"""
消融实验管理器
实现 AHE 可观测性驱动的消融实验机制
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import subprocess

# 配置
SKILL_DIR = Path(__file__).parent.parent
ABLATION_EXPERIMENTS_DIR = SKILL_DIR / "ablation_experiments"
PROGRESS_FILE = SKILL_DIR / "progress.md"

# Harness 组件
HARNESS_COMPONENTS = {
    "instructions": {
        "name": "指令",
        "description": "SKILL.md 指令集",
        "files": ["SKILL.md"]
    },
    "state": {
        "name": "状态",
        "description": "进度追踪和状态持久化",
        "files": ["progress.md", "feature_list.json"]
    },
    "verification": {
        "name": "验证",
        "description": "自动验证和质量检查",
        "files": ["scripts/verify_harness.py", "scripts/auto_optimize.py"]
    },
    "scope": {
        "name": "范围",
        "description": "功能边界控制",
        "files": ["feature_list.json"]
    },
    "lifecycle": {
        "name": "生命周期",
        "description": "会话初始化和清理",
        "files": ["init.sh", "scripts/hook_session_start.py", "scripts/hook_session_end.py"]
    },
    "sprint_contract": {
        "name": "Sprint 合同",
        "description": "任务前协商完成定义",
        "files": ["scripts/sprint_contract.py"]
    },
    "evaluator_rubric": {
        "name": "评估者评分表",
        "description": "量化质量评估",
        "files": ["scripts/evaluator_rubric.py"]
    },
    "observability": {
        "name": "可观测性",
        "description": "运行时信号收集",
        "files": ["scripts/observability.py"]
    }
}

class AblationExperiment:
    """消融实验类"""
    
    def __init__(self, experiment_id: str, title: str, 
                 baseline_components: List[str],
                 ablation_sequence: List[List[str]]):
        self.experiment_id = experiment_id
        self.title = title
        self.baseline_components = baseline_components
        self.ablation_sequence = ablation_sequence
        self.created_at = datetime.now().isoformat()
        self.results = []
        self.status = "created"  # created, running, completed, failed
    
    def to_dict(self) -> Dict:
        return {
            "experiment_id": self.experiment_id,
            "title": self.title,
            "baseline_components": self.baseline_components,
            "ablation_sequence": self.ablation_sequence,
            "created_at": self.created_at,
            "results": self.results,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AblationExperiment':
        experiment = cls(
            experiment_id=data["experiment_id"],
            title=data["title"],
            baseline_components=data["baseline_components"],
            ablation_sequence=data["ablation_sequence"]
        )
        experiment.created_at = data["created_at"]
        experiment.results = data.get("results", [])
        experiment.status = data.get("status", "created")
        return experiment

class AblationExperimentManager:
    """消融实验管理器"""
    
    def __init__(self):
        self.experiments_dir = ABLATION_EXPERIMENTS_DIR
        self.experiments_dir.mkdir(exist_ok=True)
    
    def create_experiment(self, title: str, 
                         baseline_components: Optional[List[str]] = None,
                         ablation_sequence: Optional[List[List[str]]] = None) -> AblationExperiment:
        """创建新的消融实验"""
        experiment_id = f"ablation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if baseline_components is None:
            baseline_components = list(HARNESS_COMPONENTS.keys())
        
        if ablation_sequence is None:
            # 默认消融序列：逐个移除组件
            ablation_sequence = []
            for component in baseline_components:
                ablation_sequence.append([component])
        
        experiment = AblationExperiment(
            experiment_id=experiment_id,
            title=title,
            baseline_components=baseline_components,
            ablation_sequence=ablation_sequence
        )
        
        # 保存到文件
        experiment_file = self.experiments_dir / f"{experiment_id}.json"
        with open(experiment_file, 'w', encoding='utf-8') as f:
            json.dump(experiment.to_dict(), f, indent=2, ensure_ascii=False)
        
        # 更新进度文件
        self._update_progress(experiment)
        
        return experiment
    
    def get_experiment(self, experiment_id: str) -> Optional[AblationExperiment]:
        """获取消融实验"""
        experiment_file = self.experiments_dir / f"{experiment_id}.json"
        if not experiment_file.exists():
            return None
        
        with open(experiment_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return AblationExperiment.from_dict(data)
    
    def list_experiments(self) -> List[AblationExperiment]:
        """列出所有消融实验"""
        experiments = []
        for experiment_file in self.experiments_dir.glob("*.json"):
            with open(experiment_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            experiment = AblationExperiment.from_dict(data)
            experiments.append(experiment)
        
        return experiments
    
    def run_experiment(self, experiment_id: str, 
                      test_script: str,
                      metrics: List[str]) -> bool:
        """运行消融实验"""
        experiment = self.get_experiment(experiment_id)
        if not experiment:
            return False
        
        experiment.status = "running"
        self._save_experiment(experiment)
        
        try:
            # 运行基线测试
            baseline_result = self._run_test(test_script, metrics, experiment.baseline_components)
            experiment.results.append({
                "configuration": "baseline",
                "components": experiment.baseline_components,
                "metrics": baseline_result,
                "timestamp": datetime.now().isoformat()
            })
            
            # 运行消融测试
            for ablation_step in experiment.ablation_sequence:
                # 计算当前组件（移除指定组件）
                current_components = [
                    c for c in experiment.baseline_components 
                    if c not in ablation_step
                ]
                
                # 运行测试
                result = self._run_test(test_script, metrics, current_components)
                
                experiment.results.append({
                    "configuration": f"ablation_{'_'.join(ablation_step)}",
                    "components": current_components,
                    "removed_components": ablation_step,
                    "metrics": result,
                    "timestamp": datetime.now().isoformat()
                })
            
            experiment.status = "completed"
            self._save_experiment(experiment)
            
            return True
        
        except Exception as e:
            experiment.status = "failed"
            experiment.results.append({
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            self._save_experiment(experiment)
            
            return False
    
    def _run_test(self, test_script: str, metrics: List[str], 
                 components: List[str]) -> Dict:
        """运行测试并收集指标"""
        # 这里应该实际运行测试脚本
        # 为了示例，返回模拟数据
        
        result = {}
        for metric in metrics:
            # 模拟指标收集
            # 实际实现中，这里应该运行测试脚本并解析输出
            result[metric] = {
                "value": 0.0,
                "unit": "score",
                "description": f"模拟 {metric} 指标"
            }
        
        return result
    
    def _save_experiment(self, experiment: AblationExperiment):
        """保存实验"""
        experiment_file = self.experiments_dir / f"{experiment.experiment_id}.json"
        with open(experiment_file, 'w', encoding='utf-8') as f:
            json.dump(experiment.to_dict(), f, indent=2, ensure_ascii=False)
    
    def analyze_results(self, experiment_id: str) -> Dict:
        """分析实验结果"""
        experiment = self.get_experiment(experiment_id)
        if not experiment or experiment.status != "completed":
            return {}
        
        if len(experiment.results) < 2:
            return {}
        
        baseline = experiment.results[0]
        analysis = {
            "experiment_id": experiment_id,
            "title": experiment.title,
            "baseline_metrics": baseline["metrics"],
            "component_impact": {}
        }
        
        # 分析每个组件的影响
        for result in experiment.results[1:]:
            if "removed_components" in result:
                for component in result["removed_components"]:
                    impact = {}
                    for metric in baseline["metrics"]:
                        baseline_value = baseline["metrics"][metric]["value"]
                        ablation_value = result["metrics"][metric]["value"]
                        
                        if baseline_value > 0:
                            change = (ablation_value - baseline_value) / baseline_value * 100
                        else:
                            change = 0
                        
                        impact[metric] = {
                            "baseline": baseline_value,
                            "ablation": ablation_value,
                            "change_percent": change,
                            "impact": "negative" if change < 0 else "positive" if change > 0 else "neutral"
                        }
                    
                    analysis["component_impact"][component] = {
                        "name": HARNESS_COMPONENTS.get(component, {}).get("name", component),
                        "impact": impact
                    }
        
        return analysis
    
    def generate_report(self, experiment_id: str) -> str:
        """生成实验报告"""
        analysis = self.analyze_results(experiment_id)
        if not analysis:
            return "无法生成报告：实验未完成或无结果"
        
        report = f"""
# 消融实验报告: {analysis['title']}

## 实验 ID
{analysis['experiment_id']}

## 基线指标
"""
        for metric, data in analysis['baseline_metrics'].items():
            report += f"- **{metric}**: {data['value']} {data['unit']}\n"
        
        report += "\n## 组件影响分析\n"
        
        for component, data in analysis['component_impact'].items():
            report += f"\n### {data['name']} ({component})\n"
            
            for metric, impact in data['impact'].items():
                direction = "↑" if impact['impact'] == 'positive' else "↓" if impact['impact'] == 'negative' else "→"
                report += f"- **{metric}**: {impact['baseline']} → {impact['ablation']} ({direction} {abs(impact['change_percent']):.1f}%)\n"
        
        report += "\n## 结论\n"
        
        # 找出影响最大的组件
        max_impact_component = None
        max_impact_value = 0
        
        for component, data in analysis['component_impact'].items():
            total_impact = sum(abs(imp['change_percent']) for imp in data['impact'].values())
            if total_impact > max_impact_value:
                max_impact_value = total_impact
                max_impact_component = component
        
        if max_impact_component:
            report += f"影响最大的组件: **{analysis['component_impact'][max_impact_component]['name']}**\n"
            report += f"总影响度: {max_impact_value:.1f}%\n"
        
        return report
    
    def _update_progress(self, experiment: AblationExperiment):
        """更新进度文件"""
        if not PROGRESS_FILE.exists():
            return
        
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 添加消融实验记录
        experiment_record = f"""
## 消融实验: {experiment.title}
- **ID**: {experiment.experiment_id}
- **创建时间**: {experiment.created_at}
- **状态**: {experiment.status}
- **基线组件数**: {len(experiment.baseline_components)}
- **消融步骤数**: {len(experiment.ablation_sequence)}
"""
        
        # 追加到进度文件
        with open(PROGRESS_FILE, 'a', encoding='utf-8') as f:
            f.write(experiment_record)

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python ablation_experiment.py <command> [args]")
        print("命令:")
        print("  create <title>")
        print("  list")
        print("  show <experiment_id>")
        print("  run <experiment_id> <test_script> <metrics>")
        print("  analyze <experiment_id>")
        print("  report <experiment_id>")
        return
    
    manager = AblationExperimentManager()
    command = sys.argv[1]
    
    if command == "create":
        if len(sys.argv) < 3:
            print("用法: python ablation_experiment.py create <title>")
            return
        
        title = sys.argv[2]
        experiment = manager.create_experiment(title)
        print(f"✅ 创建消融实验: {experiment.experiment_id}")
        print(f"   标题: {experiment.title}")
        print(f"   基线组件数: {len(experiment.baseline_components)}")
        print(f"   消融步骤数: {len(experiment.ablation_sequence)}")
    
    elif command == "list":
        experiments = manager.list_experiments()
        
        print(f"📋 消融实验列表 ({len(experiments)} 个):")
        for experiment in experiments:
            print(f"   - {experiment.experiment_id}: {experiment.title} [{experiment.status}]")
    
    elif command == "show":
        if len(sys.argv) < 3:
            print("用法: python ablation_experiment.py show <experiment_id>")
            return
        
        experiment_id = sys.argv[2]
        experiment = manager.get_experiment(experiment_id)
        
        if not experiment:
            print(f"❌ 实验不存在: {experiment_id}")
            return
        
        print(f"📄 消融实验详情:")
        print(f"   ID: {experiment.experiment_id}")
        print(f"   标题: {experiment.title}")
        print(f"   状态: {experiment.status}")
        print(f"   创建时间: {experiment.created_at}")
        print(f"   基线组件: {', '.join(experiment.baseline_components)}")
        print(f"   消融步骤: {len(experiment.ablation_sequence)}")
        
        if experiment.results:
            print(f"   结果数: {len(experiment.results)}")
    
    elif command == "run":
        if len(sys.argv) < 5:
            print("用法: python ablation_experiment.py run <experiment_id> <test_script> <metrics>")
            print("示例: python ablation_experiment.py run ablation_20260615 test.sh 'accuracy,speed,quality'")
            return
        
        experiment_id = sys.argv[2]
        test_script = sys.argv[3]
        metrics = sys.argv[4].split(",")
        
        if manager.run_experiment(experiment_id, test_script, metrics):
            print(f"✅ 运行消融实验: {experiment_id}")
        else:
            print(f"❌ 运行失败")
    
    elif command == "analyze":
        if len(sys.argv) < 3:
            print("用法: python ablation_experiment.py analyze <experiment_id>")
            return
        
        experiment_id = sys.argv[2]
        analysis = manager.analyze_results(experiment_id)
        
        if not analysis:
            print(f"❌ 无法分析：实验未完成或无结果")
            return
        
        print(f"📊 分析结果:")
        print(f"   实验: {analysis['title']}")
        print(f"   组件影响:")
        for component, data in analysis['component_impact'].items():
            print(f"     - {data['name']}: {len(data['impact'])} 个指标")
    
    elif command == "report":
        if len(sys.argv) < 3:
            print("用法: python ablation_experiment.py report <experiment_id>")
            return
        
        experiment_id = sys.argv[2]
        report = manager.generate_report(experiment_id)
        
        print(report)
    
    else:
        print(f"❌ 未知命令: {command}")

if __name__ == "__main__":
    main()

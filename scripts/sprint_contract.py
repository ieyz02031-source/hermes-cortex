#!/usr/bin/env python3
"""
Sprint 合同管理器
实现 AHE 可观测性驱动的 Sprint 合同机制
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 配置
SKILL_DIR = Path(__file__).parent.parent
SPRINT_CONTRACTS_DIR = SKILL_DIR / "sprint_contracts"
PROGRESS_FILE = SKILL_DIR / "progress.md"

class SprintContract:
    """Sprint 合同类"""
    
    def __init__(self, contract_id: str, title: str, scope: List[str], 
                 verification_standards: List[str], exclusions: List[str]):
        self.contract_id = contract_id
        self.title = title
        self.scope = scope
        self.verification_standards = verification_standards
        self.exclusions = exclusions
        self.created_at = datetime.now().isoformat()
        self.status = "draft"  # draft, active, completed, failed
        self.evaluation_results = []
    
    def to_dict(self) -> Dict:
        return {
            "contract_id": self.contract_id,
            "title": self.title,
            "scope": self.scope,
            "verification_standards": self.verification_standards,
            "exclusions": self.exclusions,
            "created_at": self.created_at,
            "status": self.status,
            "evaluation_results": self.evaluation_results
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SprintContract':
        contract = cls(
            contract_id=data["contract_id"],
            title=data["title"],
            scope=data["scope"],
            verification_standards=data["verification_standards"],
            exclusions=data["exclusions"]
        )
        contract.created_at = data["created_at"]
        contract.status = data["status"]
        contract.evaluation_results = data.get("evaluation_results", [])
        return contract

class SprintContractManager:
    """Sprint 合同管理器"""
    
    def __init__(self):
        self.contracts_dir = SPRINT_CONTRACTS_DIR
        self.contracts_dir.mkdir(exist_ok=True)
    
    def create_contract(self, title: str, scope: List[str], 
                       verification_standards: List[str], 
                       exclusions: List[str]) -> SprintContract:
        """创建新的 Sprint 合同"""
        contract_id = f"sprint_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        contract = SprintContract(
            contract_id=contract_id,
            title=title,
            scope=scope,
            verification_standards=verification_standards,
            exclusions=exclusions
        )
        
        # 保存到文件
        contract_file = self.contracts_dir / f"{contract_id}.json"
        with open(contract_file, 'w', encoding='utf-8') as f:
            json.dump(contract.to_dict(), f, indent=2, ensure_ascii=False)
        
        # 更新进度文件
        self._update_progress(contract)
        
        return contract
    
    def get_contract(self, contract_id: str) -> Optional[SprintContract]:
        """获取 Sprint 合同"""
        contract_file = self.contracts_dir / f"{contract_id}.json"
        if not contract_file.exists():
            return None
        
        with open(contract_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return SprintContract.from_dict(data)
    
    def list_contracts(self, status: Optional[str] = None) -> List[SprintContract]:
        """列出所有 Sprint 合同"""
        contracts = []
        for contract_file in self.contracts_dir.glob("*.json"):
            with open(contract_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            contract = SprintContract.from_dict(data)
            if status is None or contract.status == status:
                contracts.append(contract)
        
        return contracts
    
    def update_contract_status(self, contract_id: str, status: str) -> bool:
        """更新合同状态"""
        contract = self.get_contract(contract_id)
        if not contract:
            return False
        
        contract.status = status
        contract_file = self.contracts_dir / f"{contract_id}.json"
        with open(contract_file, 'w', encoding='utf-8') as f:
            json.dump(contract.to_dict(), f, indent=2, ensure_ascii=False)
        
        return True
    
    def add_evaluation_result(self, contract_id: str, dimension: str, 
                            score: str, evidence: str) -> bool:
        """添加评估结果"""
        contract = self.get_contract(contract_id)
        if not contract:
            return False
        
        evaluation = {
            "dimension": dimension,
            "score": score,
            "evidence": evidence,
            "evaluated_at": datetime.now().isoformat()
        }
        contract.evaluation_results.append(evaluation)
        
        contract_file = self.contracts_dir / f"{contract_id}.json"
        with open(contract_file, 'w', encoding='utf-8') as f:
            json.dump(contract.to_dict(), f, indent=2, ensure_ascii=False)
        
        return True
    
    def _update_progress(self, contract: SprintContract):
        """更新进度文件"""
        if not PROGRESS_FILE.exists():
            return
        
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 添加 Sprint 合同记录
        sprint_record = f"""
## Sprint 合同: {contract.title}
- **ID**: {contract.contract_id}
- **创建时间**: {contract.created_at}
- **状态**: {contract.status}
- **范围**: {', '.join(contract.scope)}
- **验证标准**: {', '.join(contract.verification_standards)}
"""
        
        # 追加到进度文件
        with open(PROGRESS_FILE, 'a', encoding='utf-8') as f:
            f.write(sprint_record)

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python sprint_contract.py <command> [args]")
        print("命令:")
        print("  create <title> <scope> <verification> <exclusions>")
        print("  list [status]")
        print("  show <contract_id>")
        print("  update <contract_id> <status>")
        print("  evaluate <contract_id> <dimension> <score> <evidence>")
        return
    
    manager = SprintContractManager()
    command = sys.argv[1]
    
    if command == "create":
        if len(sys.argv) < 6:
            print("用法: python sprint_contract.py create <title> <scope> <verification> <exclusions>")
            return
        
        title = sys.argv[2]
        scope = sys.argv[3].split(",")
        verification = sys.argv[4].split(",")
        exclusions = sys.argv[5].split(",")
        
        contract = manager.create_contract(title, scope, verification, exclusions)
        print(f"✅ 创建 Sprint 合同: {contract.contract_id}")
        print(f"   标题: {contract.title}")
        print(f"   范围: {', '.join(contract.scope)}")
    
    elif command == "list":
        status = sys.argv[2] if len(sys.argv) > 2 else None
        contracts = manager.list_contracts(status)
        
        print(f"📋 Sprint 合同列表 ({len(contracts)} 个):")
        for contract in contracts:
            print(f"   - {contract.contract_id}: {contract.title} [{contract.status}]")
    
    elif command == "show":
        if len(sys.argv) < 3:
            print("用法: python sprint_contract.py show <contract_id>")
            return
        
        contract_id = sys.argv[2]
        contract = manager.get_contract(contract_id)
        
        if not contract:
            print(f"❌ 合同不存在: {contract_id}")
            return
        
        print(f"📄 Sprint 合同详情:")
        print(f"   ID: {contract.contract_id}")
        print(f"   标题: {contract.title}")
        print(f"   状态: {contract.status}")
        print(f"   创建时间: {contract.created_at}")
        print(f"   范围: {', '.join(contract.scope)}")
        print(f"   验证标准: {', '.join(contract.verification_standards)}")
        print(f"   排除项: {', '.join(contract.exclusions)}")
        
        if contract.evaluation_results:
            print(f"   评估结果:")
            for eval in contract.evaluation_results:
                print(f"     - {eval['dimension']}: {eval['score']}")
                print(f"       证据: {eval['evidence']}")
    
    elif command == "update":
        if len(sys.argv) < 4:
            print("用法: python sprint_contract.py update <contract_id> <status>")
            return
        
        contract_id = sys.argv[2]
        status = sys.argv[3]
        
        if manager.update_contract_status(contract_id, status):
            print(f"✅ 更新合同状态: {contract_id} -> {status}")
        else:
            print(f"❌ 合同不存在: {contract_id}")
    
    elif command == "evaluate":
        if len(sys.argv) < 6:
            print("用法: python sprint_contract.py evaluate <contract_id> <dimension> <score> <evidence>")
            return
        
        contract_id = sys.argv[2]
        dimension = sys.argv[3]
        score = sys.argv[4]
        evidence = sys.argv[5]
        
        if manager.add_evaluation_result(contract_id, dimension, score, evidence):
            print(f"✅ 添加评估结果: {contract_id}")
            print(f"   维度: {dimension}")
            print(f"   评分: {score}")
            print(f"   证据: {evidence}")
        else:
            print(f"❌ 合同不存在: {contract_id}")
    
    else:
        print(f"❌ 未知命令: {command}")

if __name__ == "__main__":
    main()

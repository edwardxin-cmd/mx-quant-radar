import json
import os
import subprocess

# ==========================================
# ⚙️ 配置路径 (锁定美股/宏观全局文件)
# ==========================================
repo_path = r"F:\mx_radar_web"  # 你的 Web 仓库物理路径
history_file = os.path.join(repo_path, "history_1d.json")     # 👈 移除了 _china
consensus_file = os.path.join(repo_path, "consensus_1d.json") # 👈 移除了 _china

def fix_and_push():
    print("🔧 开始执行美股/宏观物理回滚手术...")
    
    # 1. 读取并修复历史文件
    if not os.path.exists(history_file):
        print(f"❌ 找不到文件: {history_file}")
        return
        
    with open(history_file, 'r', encoding='utf-8') as f:
        history_data = json.load(f)

    if len(history_data) == 0:
        print("⚠️ 历史记录已经是空的了。")
        return

    # 咔嚓！切掉最后一次误点的记录
    wrong_record = history_data.pop()
    print(f"🗑️ 已切除误点记录: 🕰️ {wrong_record.get('timestamp')}")

    # 写回 history
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history_data, f, indent=4, ensure_ascii=False)
    print("✅ history_1d.json 已成功复原。")

    # 2. 修复 consensus 文件 (用上一次的真实数据重铸快照)
    if len(history_data) > 0:
        last_valid_snapshot = history_data[-1]
        consensus_payload = {
            "timeframe": "1D",
            "update_time": last_valid_snapshot.get("timestamp"),
            "signals": last_valid_snapshot.get("signals", []),
            "disclaimer": "Internal research only. Not financial advice."
        }

        with open(consensus_file, 'w', encoding='utf-8') as f:
            json.dump(consensus_payload, f, indent=4, ensure_ascii=False)
        print(f"✅ consensus_1d.json 已重置回: 🕰️ {last_valid_snapshot.get('timestamp')}")
    else:
        print("⚠️ 历史库已清空，无法恢复 consensus。")

    # 3. 自动推送到 GitHub 强行覆盖
    print("\n🚀 正在拉起 Git 协议，将干净时空推送到全球节点...")
    try:
        os.chdir(repo_path)
        # 强制提交修改后的这两个文件
        subprocess.run(["git", "add", "history_1d.json", "consensus_1d.json"], check=True)
        subprocess.run(["git", "commit", "-m", "⚡ Revert: Undo accidental duplicate US/Macro snapshot"], check=True)
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        print("🏆 美股/宏观云端节点已全部修复同步！")
    except Exception as e:
        print(f"❌ Git 推送失败，请手动在文件夹下 push: {e}")

if __name__ == "__main__":
    fix_and_push()
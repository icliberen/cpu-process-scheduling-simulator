from typing import List, Dict

def init_per_process(processes: List[Dict]) -> Dict[str, Dict]:
    per_proc: Dict[str, Dict] = {}
    for p in processes:
        pid = p["pid"]
        per_proc[pid] = {
            "arrival": p["arrival"],
            "burst": p["burst"],
            "priority": p["priority"],
            "start_time": None,
            "completion_time": None,
        }
    return per_proc

def count_context_switches(timeline) -> int:
    if not timeline:
        return 0
    switches = 0
    prev = timeline[0]
    for t in range(1, len(timeline)):
        cur = timeline[t]
        if cur != prev:
            switches += 1
        prev = cur
    return switches

from typing import List, Dict, Optional, Any
import copy
from . import init_per_process, count_context_switches

def schedule_priority_np(processes: List[Dict[str, Any]]) -> Dict[str, Any]:
    original = copy.deepcopy(processes)
    n = len(original)
    per_proc = init_per_process(original)
    timeline: List[Optional[str]] = []
    log: List[str] = []
    time = 0
    completed = 0
    finished = set()

    while completed < n:
        ready = [p for p in original if p["arrival"] <= time and p["pid"] not in finished]
        if not ready:
            timeline.append(None)
            time += 1
            continue

        ready.sort(key=lambda p: (p["priority"], p["arrival"], p["index"]))
        p = ready[0]
        pid = p["pid"]
        burst = p["burst"]

        if per_proc[pid]["start_time"] is None:
            per_proc[pid]["start_time"] = time
            log.append(f"t={time}: {pid} starts running (Priority NP)")

        for _ in range(burst):
            timeline.append(pid)
            time += 1

        per_proc[pid]["completion_time"] = time
        finished.add(pid)
        completed += 1
        log.append(f"t={time}: {pid} completes (Priority NP)")

    ctx = count_context_switches(timeline)
    return {
        "name": "PRIO_NP",
        "timeline": timeline,
        "per_process": per_proc,
        "log": log,
        "context_switches": ctx,
    }

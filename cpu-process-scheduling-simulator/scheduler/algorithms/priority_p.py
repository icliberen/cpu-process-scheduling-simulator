from typing import List, Dict, Optional, Any
import copy
from . import init_per_process, count_context_switches

def schedule_priority_p(processes: List[Dict[str, Any]]) -> Dict[str, Any]:
    original = copy.deepcopy(processes)
    n = len(original)
    per_proc = init_per_process(original)
    timeline: List[Optional[str]] = []
    log: List[str] = []
    remaining = {p["pid"]: p["burst"] for p in original}
    time = 0
    completed = 0
    prev_pid: Optional[str] = None

    while completed < n:
        ready = [p for p in original if p["arrival"] <= time and remaining[p["pid"]] > 0]
        if not ready:
            timeline.append(None)
            time += 1
            prev_pid = None
            continue

        ready.sort(key=lambda p: (p["priority"], p["arrival"], p["index"]))
        cur = ready[0]
        pid = cur["pid"]

        if per_proc[pid]["start_time"] is None:
            per_proc[pid]["start_time"] = time
            log.append(f"t={time}: {pid} starts running (Priority P)")
        elif prev_pid is not None and prev_pid != pid:
            log.append(f"t={time}: {pid} preempts {prev_pid} (Priority P)")

        timeline.append(pid)
        time += 1
        remaining[pid] -= 1

        if remaining[pid] == 0:
            per_proc[pid]["completion_time"] = time
            completed += 1
            log.append(f"t={time}: {pid} completes (Priority P)")

        prev_pid = pid

    ctx = count_context_switches(timeline)
    return {
        "name": "PRIO_P",
        "timeline": timeline,
        "per_process": per_proc,
        "log": log,
        "context_switches": ctx,
    }

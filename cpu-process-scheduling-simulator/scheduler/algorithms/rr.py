from typing import List, Dict, Optional, Any
import copy
from collections import deque
from . import init_per_process, count_context_switches

def schedule_rr(processes: List[Dict[str, Any]], quantum: int) -> Dict[str, Any]:
    original = copy.deepcopy(processes)
    original.sort(key=lambda p: (p["arrival"], p["index"]))

    per_proc = init_per_process(original)
    timeline: List[Optional[str]] = []
    log: List[str] = []

    remaining = {p["pid"]: p["burst"] for p in original}
    time = 0
    completed = 0
    n = len(original)

    ready = deque()
    i = 0
    prev_pid: Optional[str] = None

    while completed < n:
        while i < n and original[i]["arrival"] <= time:
            ready.append(original[i])
            i += 1

        if not ready:
            timeline.append(None)
            time += 1
            continue

        p = ready.popleft()
        pid = p["pid"]

        if per_proc[pid]["start_time"] is None:
            per_proc[pid]["start_time"] = time
            log.append(f"t={time}: {pid} starts running (RR)")
        elif prev_pid is not None and prev_pid != pid:
            log.append(f"t={time}: {pid} resumes (RR)")

        run_for = min(quantum, remaining[pid])

        for _ in range(run_for):
            timeline.append(pid)
            time += 1
            remaining[pid] -= 1

            while i < n and original[i]["arrival"] <= time:
                ready.append(original[i])
                i += 1

            if remaining[pid] == 0:
                break

        if remaining[pid] == 0:
            per_proc[pid]["completion_time"] = time
            completed += 1
            log.append(f"t={time}: {pid} completes (RR)")
        else:
            ready.append(p)

        prev_pid = pid

    ctx = count_context_switches(timeline)
    return {
        "name": f"RR(q={quantum})",
        "timeline": timeline,
        "per_process": per_proc,
        "log": log,
        "context_switches": ctx,
    }

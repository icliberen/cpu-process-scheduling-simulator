from typing import List, Dict, Optional, Any
import copy
from . import init_per_process, count_context_switches

def schedule_fcfs(processes: List[Dict[str, Any]]) -> Dict[str, Any]:
    procs = copy.deepcopy(processes)
    procs.sort(key=lambda p: (p["arrival"], p["index"]))

    per_proc = init_per_process(procs)
    timeline: List[Optional[str]] = []
    log: List[str] = []
    time = 0

    for p in procs:
        pid = p["pid"]
        arrival = p["arrival"]
        burst = p["burst"]

        if time < arrival:
            for a in range(time, arrival):
                timeline.append(None)
            time = arrival
            log.append(f"t={time}: CPU idle until {pid} arrives")

        per_proc[pid]["start_time"] = time
        log.append(f"t={time}: {pid} starts running (FCFS)")

        for a in range(burst):
            timeline.append(pid)
            time += 1

        per_proc[pid]["completion_time"] = time
        log.append(f"t={time}: {pid} completes (FCFS)")

    ctx = count_context_switches(timeline)
    return {
        "name": "FCFS",
        "timeline": timeline,
        "per_process": per_proc,
        "log": log,
        "context_switches": ctx,
    }

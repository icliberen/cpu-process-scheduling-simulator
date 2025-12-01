from typing import Dict, List, Any, Tuple

def compute_per_process_stats(per_proc: Dict[str, Dict[str, int]]) -> Tuple[List[Dict[str, Any]], Dict[str, float]]:
    rows: List[Dict[str, Any]] = []
    total_turnaround = total_waiting = total_response = 0
    n = len(per_proc)
    for pid, info in sorted(per_proc.items(), key=lambda x: x[0]):
        arrival = info["arrival"]
        burst = info["burst"]
        completion = info["completion_time"]
        start = info["start_time"]

        turnaround = completion - arrival
        waiting = turnaround - burst
        response = start - arrival

        total_turnaround += turnaround
        total_waiting += waiting
        total_response += response

        rows.append({
            "pid": pid,
            "arrival": arrival,
            "burst": burst,
            "completion": completion,
            "turnaround": turnaround,
            "waiting": waiting,
            "response": response,
        })

    averages = {
        "avg_turnaround": total_turnaround / n if n else 0.0,
        "avg_waiting": total_waiting / n if n else 0.0,
        "avg_response": total_response / n if n else 0.0,
    }
    return rows, averages

def print_per_process_table(rows: List[Dict[str, Any]]) -> None:
    print("\nPer-process statistics:")
    print(f"{'PID':<5}{'Arr':>5}{'Burst':>7}{'Compl':>8}{'Turn':>8}{'Wait':>7}{'Resp':>7}")
    for r in rows:
        print(f"{r['pid']:<5}{r['arrival']:>5}{r['burst']:>7}{r['completion']:>8}"
              f"{r['turnaround']:>8}{r['waiting']:>7}{r['response']:>7}")

def print_overall_stats(averages: Dict[str, float], context_switches: int) -> None:
    print("\nOverall metrics:")
    print(f"Average Turnaround Time: {averages['avg_turnaround']:.2f}")
    print(f"Average Waiting Time   : {averages['avg_waiting']:.2f}")
    print(f"Average Response Time  : {averages['avg_response']:.2f}")
    print(f"Total Context Switches : {context_switches}")

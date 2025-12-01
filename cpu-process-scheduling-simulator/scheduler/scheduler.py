import argparse
from typing import Dict, Any, List
import os

HAS_MPL = False
try:
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    print("[INFO] matplotlib not found; graph generation will be skipped.")

from .utils.parser import parse_processes
from .utils import statistics as stats
from .utils import gantt

from .algorithms.fcfs import schedule_fcfs
from .algorithms.sjf import schedule_sjf
from .algorithms.srtf import schedule_srtf
from .algorithms.rr import schedule_rr
from .algorithms.priority_np import schedule_priority_np
from .algorithms.priority_p import schedule_priority_p

def run_and_report(algorithm_func, processes, **kwargs) -> Dict[str, Any]:
    result = algorithm_func(processes, **kwargs) if kwargs else algorithm_func(processes)

    name = result["name"]
    print("\n" + "=" * 60)
    print(f"Algorithm: {name}")
    print("=" * 60)

    os.makedirs("logs", exist_ok=True)
    txt_path = f"logs/{name}_log.txt"

    log_lines = []
    log_lines.append(f"Algorithm: {name}")
    log_lines.append("=" * 50)
    log_lines.append("\nEXECUTION LOG:")
    for entry in result["log"]:
        log_lines.append(entry)

    # Process statistics
    rows, averages = stats.compute_per_process_stats(result["per_process"])
    log_lines.append("\nPER-PROCESS STATISTICS:")
    for r in rows:
        log_lines.append(str(r))

    # Overall stats
    log_lines.append("\nOVERALL STATISTICS:")
    for k, v in averages.items():
        log_lines.append(f"{k}: {v:.2f}")
    log_lines.append(f"Context Switches: {result['context_switches']}")

    # Write .txt file
    with open(txt_path, "w", encoding="utf-8") as f:
        for line in log_lines:
            f.write(line + "\n")
            print(f"[SAVED] Execution log saved to {txt_path}")
            print("\nGantt chart:")
            gantt.print_gantt_chart(result["timeline"])

    print("\nExecution log:")
    for entry in result["log"]:
        print(entry)
    stats.print_per_process_table(rows)
    stats.print_overall_stats(averages, result["context_switches"])

    result["averages"] = averages
    return result


def run_all_algorithms(processes, quantum: int) -> List[Dict[str, Any]]:
    results = []
    results.append(run_and_report(schedule_fcfs, processes))
    results.append(run_and_report(schedule_sjf, processes))
    results.append(run_and_report(schedule_srtf, processes))
    results.append(run_and_report(schedule_rr, processes, quantum=quantum))
    results.append(run_and_report(schedule_priority_np, processes))
    results.append(run_and_report(schedule_priority_p, processes))
    return results

def plot_comparison(results: List[Dict[str, Any]], out_dir: str = "graphs") -> None:
    if not HAS_MPL:
        print("\n[INFO] Skipping graph generation (matplotlib not installed).")
        return

    os.makedirs(out_dir, exist_ok=True)
    alg_names = [r["name"] for r in results]
    avg_wait = [r["averages"]["avg_waiting"] for r in results]
    avg_turn = [r["averages"]["avg_turnaround"] for r in results]
    ctx = [r["context_switches"] for r in results]

    import matplotlib.pyplot as plt
    plt.figure()
    plt.bar(alg_names, avg_wait)
    plt.xlabel("Algorithm")
    plt.ylabel("Average Waiting Time")
    plt.title("Average Waiting Time vs Algorithm")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "waiting.png"))

    plt.figure()
    plt.bar(alg_names, avg_turn)
    plt.xlabel("Algorithm")
    plt.ylabel("Average Turnaround Time")
    plt.title("Average Turnaround Time vs Algorithm")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "turnaround.png"))

    plt.figure()
    plt.bar(alg_names, ctx)
    plt.xlabel("Algorithm")
    plt.ylabel("Context Switches")
    plt.title("Context Switches vs Algorithm")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "context_switches.png"))

    print(f"\nGraphs saved in directory: {out_dir}/")

def main():
    parser = argparse.ArgumentParser(description="CPU Process Scheduling Simulator")
    parser.add_argument("--input", required=True, help="Path to process description file")
    parser.add_argument("--algo", required=True,
                        help="FCFS, SJF, SRTF, RR, PRIO_NP, PRIO_P, or ALL")
    parser.add_argument("--quantum", type=int,
                        help="Time quantum for RR / ALL (required for RR and ALL)")
    args = parser.parse_args()

    processes = parse_processes(args.input)
    algo = args.algo.upper().replace(" ", "_")

    if algo in ("RR", "ALL") and args.quantum is None:
        raise SystemExit("Error: --quantum is required when --algo is RR or ALL.")

    if algo == "FCFS":
        run_and_report(schedule_fcfs, processes)
    elif algo == "SJF":
        run_and_report(schedule_sjf, processes)
    elif algo == "SRTF":
        run_and_report(schedule_srtf, processes)
    elif algo == "RR":
        run_and_report(schedule_rr, processes, quantum=args.quantum)
    elif algo in ("PRIO_NP", "PRIONP"):
        run_and_report(schedule_priority_np, processes)
    elif algo in ("PRIO_P", "PRIOP"):
        run_and_report(schedule_priority_p, processes)
    elif algo == "ALL":
        results = run_all_algorithms(processes, quantum=args.quantum)
        print("\n" + "#" * 60)
        print("Summary comparison:")
        print("#" * 60)
        print(f"{'Algorithm':<12}{'AvgTurn':>10}{'AvgWait':>10}{'AvgResp':>10}{'Ctx':>8}")
        for r in results:
            a = r["averages"]
            print(f"{r['name']:<12}{a['avg_turnaround']:>10.2f}{a['avg_waiting']:>10.2f}"
                  f"{a['avg_response']:>10.2f}{r['context_switches']:>8}")
        plot_comparison(results)
    else:
        raise SystemExit(f"Unknown algorithm: {args.algo}")

if __name__ == "__main__":
    main()

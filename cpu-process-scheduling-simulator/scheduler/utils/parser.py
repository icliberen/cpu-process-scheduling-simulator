from typing import List, Dict

def parse_processes(filename: str) -> List[Dict]:
    processes = []
    with open(filename, "r", encoding="utf-8") as f:
        idx = 0
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) != 4:
                raise ValueError(f"Invalid line in process file: {line}")
            pid, arrival, burst, priority = parts
            processes.append({
                "pid": pid,
                "arrival": int(arrival),
                "burst": int(burst),
                "priority": int(priority),
                "index": idx,
            })
            idx += 1
    return processes

from typing import List, Optional, Tuple

def compress_timeline(timeline: List[Optional[str]]) -> List[Tuple[int, int, Optional[str]]]:
    if not timeline:
        return []
    segments = []
    current_pid = timeline[0]
    start = 0
    for t in range(1, len(timeline)):
        if timeline[t] != current_pid:
            segments.append((start, t, current_pid))
            start = t
            current_pid = timeline[t]
    segments.append((start, len(timeline), current_pid))
    return segments

def print_gantt_chart(timeline: List[Optional[str]]) -> None:
    segments = compress_timeline(timeline)
    if not segments:
        print("No execution (empty timeline).")
        return

    max_time = segments[-1][1]
    print("Time:", end=" ")
    for t in range(max_time + 1):
        print(t, end=" ")
    print()

    bar = ""
    for (start, end, pid) in segments:
        length = end - start
        label = "IDLE" if pid is None else pid
        bar += "|" + "-" * length + label + "-" * length
    bar += "|"
    print(bar)

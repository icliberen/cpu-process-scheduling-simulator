# CPU-Process-Scheduling-Simulator
This project is a Python-based simulator. It allows users to run and compare various CPU Scheduling Algorithms, analyze their performance, and optionally generate visual graphs.

## Environment, Python Version and Dependencies

- **Python Version (tested):** Python 3.13.5  
  (The code should also work on Python 3.8+ with minor or no changes.)
- **Dependencies:**
  - Standard Library only:
    - `argparse`
    - `typing`
    - `copy`
    - `collections`
    - `os`
- **Optional:** `matplotlib` (only required for graph generation)
  - Used for:
    - Average Waiting Time vs Algorithm (bar chart)
    - Average Turnaround Time vs Algorithm (bar chart)
    - Context Switches vs Algorithm (bar chart)
    - If `matplotlib` is not installed, the simulator still runs and **skips graph generation**.

---

## Project Structure

scheduler/
  __init__.py
  scheduler.py
  processes.txt         # sample process input file
  algorithms/
    __init__.py
    fcfs.py
    sjf.py
    srtf.py
    rr.py
    priority_np.py
    priority_p.py
  utils/
    __init__.py
    parser.py
    statistics.py
    gantt.py

## How to Run the Simulator

Open a terminal in your project directory:

Running Individual Algorithms:
-   **FCFS**
    python -m scheduler.scheduler --input scheduler\processes.txt --algo FCFS
-   **SJF (non-preemptive)**   
    python -m scheduler.scheduler --input scheduler\processes.txt --algo SJF
-   **SRTF (preemptive SJF)**
    python -m scheduler.scheduler --input scheduler\processes.txt --algo SRTF
-   **Round Robin (requires quantum)**
    python -m scheduler.scheduler --input scheduler\processes.txt --algo RR --quantum 4
-   **Priority – Non-preemptive**
    python -m scheduler.scheduler --input scheduler\processes.txt --algo PRIO_NP
-   **Priority – Preemptive**
    python -m scheduler.scheduler --input scheduler\processes.txt --algo PRIO_P

Running All Algorithms Together:
python -m scheduler.scheduler --input scheduler\processes.txt --algo ALL --quantum 4

This command:
Runs all required algorithms:
-    FCFS
-    SJF
-    SRTF
-    RR (q=4)
-    Priority Non-preemptive
-    Priority Preemptive
-    Prints:
-    Gantt chart
-    Execution logs
-    Per-process stats
-    Overall stats
-    Prints a full comparison table
-    If matplotlib is installed:
-    Saves graphs to scheduler/graphs/

Brief Description of Each Algorithm Implementation

Each algorithm:
Tracks CPU execution at every time unit, handles arrival times correctly
Computes:
Turnaround Time
Waiting Time
Response Time
Tracks context switches

FCFS (First-Come First-Served)
The simplest scheduling algorithm. Processes run in order of arrival.
No preemption: once a process starts, it runs until completion.
CPU may stay idle until a process arrives.

SJF (Shortest Job First, Non-preemptive)
Chooses the ready process with the shortest burst time.
Non-preemptive: runs until completion.

SRTF (Shortest Remaining Time First, Preemptive SJF)
Preemptive form of SJF. At each time unit, process with the smallest remaining burst executes.
Preempts running process if a shorter job arrives.

Round Robin (RR)
Each process gets the CPU for a quantum q (e.g., 4).
After q units, unfinished processes return to the queue.

Priority Scheduling (Non-preemptive)
Selects the process with highest priority (lowest number).
Non-preemptive: once started, runs until finish.

Priority Scheduling (Preemptive)
At every time step, highest-priority job runs.
New higher-priority arrival preempts the running job.

Discussion & Observations
Best Overall Algorithm (General Workload)

SRTF typically performs the best regarding:
Average turnaround time
Average waiting time
Average response time

Reason:
It always prioritizes the process closest to finishing.
Preemptive Priority performs similarly if priority values correlate with burst times.

Observed Behaviors:

FCFS: suffers from convoy effect
SJF vs SRTF: preemption drastically improves performance
RR: performance heavily depends on quantum size
Priority: low-priority processes can starve


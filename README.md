# Cron Scheduler
## Brief Description
This project implements an in-process cron scheduler in Python. The scheduler allows clients to specify jobs with unique identifiers, execution intervals, and frequencies using cron-like expressions. The jobs are executed as specified and can be monitored and managed through logs.
## Reasoning Behind Technical Decisions
* **Python**: Chosen for its simplicity and rich standard library.
* **Multiprocessing**: Allows concurrent execution of tasks, ensuring the scheduler can handle multiple jobs efficiently.
* **JSON**: Used for persisting job schedules due to its simplicity and ease of use.
* **Subprocess**: Used to run external scripts, allowing flexibility in the types of jobs that can be scheduled.
## Trade-offs
* The current implementation runs as a foreground process. Running it as a background service or daemon would require additional setup.
* Using JSON for persistence is simple but not suitable for highly concurrent environments or large-scale use.
* The interval for single-run tasks expects a number representing minutes, which limits the granularity of scheduling options.

## Installing and Setting Up
1. Install the Package: Ensure you are in the cron_scheduler directory and run:
`pip install -e`
2. Ensure the create_cron Command is Available:
Add the Scripts directory (which will be given to you after the packages are installed) to your PATH environment variable if it's not already.
3. Verify by running:
`create_cron --help`

## Example Usage
### Adding a Job
`create_cron job_id --interval 30 "* * * * *" /idk/smth/script.py`

This command schedules a job with:
* A unique job identifier job1
* A single-run interval of 30 minutes (interval expects a number which will be treated as minutes)
* A frequency specified by the cron-like expression * * * * *
* A script located at /idk/smth/script.py

## Running the Scheduler
To run the scheduler, execute the following command:
`python -m cron_scheduler.scheduler`
This command runs the scheduler in the background.

## Log File
The log file is located at `cron_scheduler/scheduler.log`. This file contains information about task starts, completions, and errors.

## Possible Future Improvements
* **Robust Storage Solution**: Implementing a more robust storage solution (e.g., SQLite) for concurrency and scalability.
* **Background Service**: Enhancing the scheduler to run as a Windows service or a Linux daemon.
* **Web Interface**: Adding a web interface for easier job management.
* **Advanced Scheduling** Options: Supporting more granular and flexible scheduling options beyond minute intervals.
* **Enhanced Logging and Error Handling**: Adding more sophisticated logging and error handling mechanisms.


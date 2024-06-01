import datetime
import logging
import subprocess
import multiprocessing
import time
import json
import os

SCHEDULE_FILE = os.path.join(os.path.dirname(__file__), '../schedule.json')
LOG_FILE = os.path.join(os.path.dirname(__file__), '../scheduler.log')


logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')


def load_schedule():
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, 'r') as f:
            return json.load(f)
    return []


def should_run(expression):
    parts = expression.split()
    current_time = datetime.datetime.now()
    return (parts[0] == '*' or current_time.minute == int(parts[0])) and (
            parts[1] == '*' or current_time.hour == int(parts[1])) and (
            parts[2] == '*' or current_time.day == int(parts[2])) and (
            parts[3] == '*' or current_time.month == int(parts[3])) and (
            parts[4] == '*' or current_time.weekday() == int(parts[4]))


def run_script(file_path):
    if file_path.endswith('.py'):
        subprocess.run(['python', file_path])
    elif file_path.endswith('.sh'):
        subprocess.run(['bash', file_path])


timeout_list = []


def run_task(task):
    process = multiprocessing.Process(target=run_script, args=(task['script'], ))
    process.start()
    logging.info(f"Started task {task['id']} with PID {process.pid}")
    if task['interval']:
        timeout_list.append([process, time.time() + int(task['interval']) * 60])
    else:
        # giving every task 30 minutes timeout by default
        timeout_list.append([process, time.time() + 30 * 60])


def main():
    while True:
        schedule_list = load_schedule()
        for task in schedule_list:
            if should_run(task['frequency']):
                run_task(task)

        for [process, timeout] in timeout_list[:]:
            if not process.is_alive():
                logging.info(f"Task with PID {process.pid} completed.")
                timeout_list.remove([process, timeout])
                continue

            if timeout < time.time():
                logging.warning(f"Task with PID {process.pid} timed out.")
                process.terminate()
                process.join()
                timeout_list.remove([process, timeout])

        time.sleep(60)


if __name__ == "__main__":
    main()

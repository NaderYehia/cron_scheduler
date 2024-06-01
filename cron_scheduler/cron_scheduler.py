import argparse
import json
import os

SCHEDULE_FILE = os.path.join(os.path.dirname(__file__), '../schedule.json')


def load_schedule():
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, 'r') as f:
            return json.load(f)
    return []


def save_schedule(schedule_list):
    with open(SCHEDULE_FILE, 'w') as f:
        json.dump(schedule_list, f)


def add_task(task_id, interval, frequency, file_path):
    schedule_list = load_schedule()
    new_task = {
        "id": task_id,
        "interval": interval,
        "frequency": frequency,
        "script": file_path
    }
    schedule_list.append(new_task)
    save_schedule(schedule_list)


def cron_expression(value):
    parts = value.split()
    if len(parts) != 5:
        raise argparse.ArgumentTypeError("Cron expression must have five parts separated by spaces")
    for part in parts:
        if not part.isdigit() and part != '*':
            raise argparse.ArgumentTypeError("Cron expression parts must be digits or '*'")

    return value


def main():
    parser = argparse.ArgumentParser(description='Add a task to the custom cron scheduler')
    parser.add_argument('id', type=str, help='Unique job identifier')
    parser.add_argument('--interval', type=str, help='Single run interval (e.g., 30m)')
    parser.add_argument('frequency', type=cron_expression, help='Cron-like expression (e.g., * * * * *)')
    parser.add_argument('file_path', type=str, help='File path')
    args = parser.parse_args()

    schedule_list = load_schedule()
    for task in schedule_list:
        if task['id'] == args.id:
            parser.error('Task with id "{}" already exists'.format(args.id))

    add_task(args.id, args.interval, args.frequency, args.file_path)


if __name__ == '__main__':
    main()

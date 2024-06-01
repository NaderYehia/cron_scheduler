import subprocess

# a job that will run every minute
subprocess.run(['create_cron', 'test_job', '--interval', '1', '* * * * *', 'test_script.py'])

# a job that will run every 15 minutes
subprocess.run(['create_cron', 'another_test_job', '--interval', '1', '15 * * * *', 'test_script.py'])


subprocess.run(['python', '../cron_scheduler/scheduler.py'])

with open('../scheduler.log', 'r') as log_file:
    logs = log_file.read()
    print(logs)

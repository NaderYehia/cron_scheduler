from setuptools import setup, find_packages

setup(
    name='Cron Scheduler',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'create_cron=cron_scheduler.cron_scheduler:main'
        ]
    }
)
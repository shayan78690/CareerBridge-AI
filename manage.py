#!/usr/bin/env python




#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import time
from django.db import connections
from django.db.utils import OperationalError


def wait_for_db():
    """Wait for database to be available"""
    print("Waiting for database...")
    time.sleep(5)  # Wait for PostgreSQL to start
    
    db_conn = None
    max_retries = 10
    retry_count = 0
    
    while not db_conn and retry_count < max_retries:
        try:
            db_conn = connections['default']
            db_conn.cursor()
            print("Database is available!")
            return True
        except OperationalError:
            print(f"Database unavailable, waiting 2 seconds... (Attempt {retry_count + 1}/{max_retries})")
            retry_count += 1
            time.sleep(2)
    
    print("Could not connect to database after maximum retries")
    return False


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_portal.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Wait for database before running any commands
    if len(sys.argv) > 1 and sys.argv[1] != 'wait_for_db':
        wait_for_db()
    
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()


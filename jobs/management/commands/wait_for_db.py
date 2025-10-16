
from django.core.management.base import BaseCommand
import time
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = None
        max_retries = 10
        retry_count = 0
        
        while not db_conn and retry_count < max_retries:
            try:
                db_conn = connections['default']
                db_conn.cursor()
                self.stdout.write(self.style.SUCCESS('Database available!'))
                return
            except OperationalError:
                self.stdout.write(f'Database unavailable, waiting 2 seconds... (Attempt {retry_count + 1}/{max_retries})')
                retry_count += 1
                time.sleep(2)
        
        self.stdout.write(self.style.ERROR('Could not connect to database after maximum retries'))

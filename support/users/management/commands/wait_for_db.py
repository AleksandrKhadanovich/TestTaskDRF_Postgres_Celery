import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management import BaseCommand


# command to wait untill postgres database is available
class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waititng 1 second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))

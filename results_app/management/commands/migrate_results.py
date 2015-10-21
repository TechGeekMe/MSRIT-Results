from django.core.management.base import BaseCommand, CommandError
from results_app.models import Student, Result, Subject, SubjectList, Student2, Result2, Subject2
from . import result_fetcher, add_result

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('branch', nargs=1, type=str)
        parser.add_argument('year', nargs=1, type=str)

    def handle(self, *args, **options):
        self.pull(options['branch'][0], options['year'][0])

    def pull(self, branch, year):
        self.update_db('1MS'+year+branch, 0, 300)
        
    def update_db(self, usn_base, first_usn, last_usn):
        bad_usns = 0
        first_usn = int(first_usn)
        last_usn = int(last_usn)
        for i in range(first_usn, last_usn):
            if bad_usns > 5:
                self.stdout.write("Over! Stopped at " + str(usn))
            usn = usn_base + str(i).zfill(3)
            try:
                add_result.add_usn(usn)
                bad_usns = 0
            except ValueError:
                bad_usns += 1

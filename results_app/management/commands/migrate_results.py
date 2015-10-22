from django.core.management.base import BaseCommand, CommandError
from results_app.models import Student, Result, Subject, SubjectList, Student2, Result2, Subject2
from . import result_fetcher, add_result

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--branch', nargs=1, type=str)
        parser.add_argument('year', nargs=1, type=str)
        parser.add_argument('--diploma', action='store_true')

    def handle(self, *args, **options):
        if options['branch']:
            if options['diploma']:
                self.update_db('1MS'+options['year'][0]+options['branch'][0], 400, 500)
            else:
                self.update_db('1MS'+options['year'][0]+options['branch'][0], 0, 300)
        elif options['diploma']:
            self.pull_dip(options['year'][0])
        else:
            self.pull(options['branch'][0], options['year'][0])
        
    def update_db(self, usn_base, first_usn, last_usn):
        bad_usns = 0
        first_usn = int(first_usn)
        last_usn = int(last_usn)
        for i in range(first_usn, last_usn):
            if bad_usns > 5:
                return self.stdout.write("Over! Stopped at " + str(usn))
            usn = usn_base + str(i).zfill(3)
            try:
                add_result.add_usn(usn)
                bad_usns = 0
            except ValueError:
                bad_usns += 1

    def pull(this, year):
        branches = ['CS', 'IS', 'IT', 'IM', 'EC', 'CV', 'ME', 'TE', 'CH', 'BT', 'EE', 'ML', 'EI', 'AT']
        for branch in branches:
            this.update_db(request, '1MS'+year+branch, 0, 300)

    def pull_dip(this, year):
        branches = ['CS', 'IS', 'IT', 'IM', 'EC', 'CV', 'ME', 'TE', 'CH', 'BT', 'EE', 'ML', 'EI', 'AT']
        for branch in branches:
            this.update_db(request, '1MS'+year+branch, 400, 500)

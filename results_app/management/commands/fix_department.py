from django.core.management.base import BaseCommand, CommandError
from results_app.models import Student, Result, Subject, SubjectList
from . import result_fetcher, fix_student

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--branch', nargs=1, type=str)
        parser.add_argument('year', nargs=1, type=str)
        parser.add_argument('--diploma', action='store_true')

    def handle(self, *args, **options):
        if options['branch']:
            if 'start' in options and 'end' in options:
                self.fix_dept('1MS'+options['year'][0]+options['branch'][0], options['start'][0], options['end'][0])
            if options['branch'][0] == 'MCA' or options['branch'][0] == 'MBA':
                self.fix_dept_mca_or_mba('1MS'+options['year'][0]+options['branch'][0], 0, 100)
            elif options['diploma']:
                self.fix_dept('1MS'+options['year'][0]+options['branch'][0], 400, 500)
            else:
                self.fix_dept('1MS'+options['year'][0]+options['branch'][0], 0, 300)
        elif options['diploma']:
            self.fix_dip(options['year'][0])
        else:
            self.fix_all(options['year'][0])
        
    def fix_dept(self, usn_base, first_usn, last_usn):
        bad_usns = 0
        first_usn = int(first_usn)
        last_usn = int(last_usn)
        for i in range(first_usn, last_usn):
            if bad_usns > 5:
                return self.stdout.write("Over! Stopped at " + str(usn))
            usn = usn_base + str(i).zfill(3)
            try:
                fix_student.fix_usn(usn)
                bad_usns = 0
            except ValueError:
                bad_usns += 1

    def fix_dept_mca_or_mba(self, usn_base, first_usn, last_usn):
        bad_usns = 0
        first_usn = int(first_usn)
        last_usn = int(last_usn)
        for i in range(first_usn, last_usn):
            if bad_usns > 5:
                return self.stdout.write("Over! Stopped at " + str(usn))
            usn = usn_base + str(i).zfill(2)
            try:
                fix_student.fix_usn(usn)
                bad_usns = 0
            except ValueError:
                bad_usns += 1

    def fix_all(self, year):
        branches = ['CS', 'IS', 'IT', 'IM', 'EC', 'CV', 'ME', 'TE', 'CH', 'BT', 'EE', 'ML', 'EI', 'AT']
        for branch in branches:
            self.fix_dept('1MS'+year+branch, 0, 300)

    def fix_dip(self, year):
        branches = ['CS', 'IS', 'IT', 'IM', 'EC', 'CV', 'ME', 'TE', 'CH', 'BT', 'EE', 'ML', 'EI', 'AT']
        for branch in branches:
            self.fix_dept('1MS'+year+branch, 400, 500)

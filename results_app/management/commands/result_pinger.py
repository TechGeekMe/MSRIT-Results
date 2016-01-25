from os import system
from time import sleep
import result_fetcher
while (result_fetcher.fetch_result('1MS13CS001') == None):
    print 'Not yet out'
    sleep(5)
print 'Results out'
system("python /var/www/html/MSRIT-Results/manage.py fetch_results 13")

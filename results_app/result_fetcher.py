import requests
from bs4 import BeautifulSoup
import re

class FetchedSubject:
    def __init__(self):
        self.course_code = None
        self.subject_name = None
        self.credits_registered = None
        self.credits_earned = None
        self.grade = None
        self.grade_point = None
    def __unicode__(self):
        return self.course_code + self.subject_name + str(self.credits_registered)\
               + str(self.credits_earned) + self.grade               
    def __str__(self):        
        return unicode(self).encode('utf-8')
        

class FetchedResult():
    def __init__(self):
        self.usn = None
        self.name = None
        self.department = None
        self.branch_code = None
        self.credits_registered = None
        self.credits_earned = None
        self.sgpa = None
        self.cgpa = None
        self.semester = None
        self.subjects = list()

    def __unicode__(self):
        return self.usn + self.name + self.department + str(self.credits_registered)\
               + str(self.credits_earned) + str(self.sgpa) + str(self.cgpa) + str(self.semester)
               
    def __str__(self):        
        return unicode(self).encode('utf-8')
        


def fetch_result(usn):
    
    #Get html page
    
    payload = {'usn': usn, 'option': 'com_examresult', 'task': 'getResult'}
    r = requests.post("http://exam.msrit.edu/index.php", data=payload)
    data = r.text
    
    # Feed html to BeautifulSoup

    soup = BeautifulSoup(data)
    sub_tables = soup.find_all("table")
    fr = FetchedResult()
    
    #Check if usn exists

    row = sub_tables[0]
    row_data = row.find_all('td')
    error_message = row_data[7].get_text()
    if error_message.startswith('Oops') or error_message.startswith('Your'):
        return None

    # Extracting name and usn
    
    row = sub_tables[3]
    row_data = row.find_all('td')
    fr.name = row_data[2].get_text()
    fr.usn = row_data[3].get_text()
    fr.usn = re.sub(r'^USN : ', '', fr.usn)
    fr.usn = fr.usn.upper()
    fr.branch_code = fr.usn[5:7]

    # Extracting department
    
    row = sub_tables[5]
    row_data = row.find_all('td')
    fr.department = row_data[3].get_text()
    fr.department = re.sub(u'^\u00a0*Department : ', '', fr.department)

    # Extracting credits required, sgpa and cgpa
    
    row = sub_tables[7]
    
    row_data = row.find_all("span")
    fr.credits_registered = int(row_data[1].get_text())
    fr.credits_earned = int(row_data[3].get_text())
    fr.sgpa = row_data[5].get_text()
    
    # Checking SGPA for TAL to convert to float
    if fr.sgpa == "TAL":
        fr.sgpa = "0"
    fr.sgpa = float(fr.sgpa)
    
    fr.cgpa = row_data[7].get_text()
    
    # Checking CGPA for TAL to convert to float
    if fr.cgpa == "TAL":
        fr.cgpa = "0"
    fr.cgpa = float(fr.cgpa)

    # Extracting result of each of subject

    subject_sem = {}
    first_iteration = True
    for row in sub_tables[10].find_all('tr'):
        if first_iteration:
            first_iteration = False
            continue
        cols = row.find_all('td')
        # Detect last row
        if cols[1].get_text() == u'\xa0':
            break;
        fs = FetchedSubject()
        fs.course_code = cols[1].get_text()
        sem = int(re.match(r'[A-Z]+\d', fs.course_code).group()[-1])
        subject_sem[sem] = subject_sem.get(sem, 0) + 1
        fs.subject_name = cols[2].get_text()
        fs.credits_registered = int(float(cols[3].get_text()))
        fs.credits_earned = int(cols[4].get_text())
        fs.grade = cols[5].get_text()
        if fs.grade == 'S':
            fs.grade_point = 10
        elif fs.grade == 'A':
            fs.grade_point = 9
        elif fs.grade == 'B':
            fs.grade_point = 8
        elif fs.grade == 'C':
            fs.grade_point = 7
        elif fs.grade == 'D':
            fs.grade_point = 5
        elif fs.grade == 'E':
            fs.grade_point = 4
        else:
            fs.grade_point = 0
        fr.subjects.append(fs)

    fr.semester = max(subject_sem, key=subject_sem.get)
    
    return fr 

from selenium.webdriver.edge.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_submission():
    # Can get student id from url:
    # https://canvas.hull.ac.uk/courses/65765/gradebook/speed_grader?assignment_id=211938&student_id=183296
    url=driver.current_url
    eqpos = url.rfind('=')
    student_id=url[eqpos+1:]
    print(f'Student id is {student_id}')

    # <span class="ui-selectmenu-item-header"> DAMI AKINTOMIDE </span>

    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'ui-selectmenu-item-header'))
    WebDriverWait(driver, timeout).until(element_present)
    sname=driver.find_element(by=By.CLASS_NAME,value="ui-selectmenu-item-header")
    student_name=sname.text
    print(student_name)
    
    # The stuff of interest is inside an iframe, which must be selected
    # <iframe id="speedgrader_iframe" src="/courses/65765/assignments/211938/submissions/182356?preview=true" frameborder="0" allowfullscreen="true"></iframe>

    try:
        # <div id="this_student_does_not_have_a_submission">
        element_present = EC.visibility_of_element_located((By.ID, 'this_student_does_not_have_a_submission'))
        WebDriverWait(driver, 4).until(element_present)
        print('No submission')
        return student_id,student_name,'No submission',None,None
    except TimeoutException:
        print('Submission present')

    try:
        element_present = EC.presence_of_element_located((By.ID, 'speedgrader_iframe'))
        WebDriverWait(driver, timeout).until(element_present)
        print('Found iframe')
    except TimeoutException:
        print("Timed out waiting for iframe to load")
        return student_id,student_name,'Timeout fail',None,None


    iframe=driver.find_element(by=By.ID, value="speedgrader_iframe")
    driver.switch_to.frame(iframe)
    question1 = driver.find_element(by=By.ID, value="question_466010")
    answer1item=question1.find_element(by=By.CLASS_NAME, value="quiz_response_text")
    answer1=answer1item.text

    question2 = driver.find_element(by=By.ID, value="question_466011")
    answer2item=question2.find_element(by=By.CLASS_NAME, value="quiz_response_text")
    answer2=answer2item.text.replace('\n','\n\n')

    question3 = driver.find_element(by=By.ID, value="question_466406")
    answer3item=question2.find_element(by=By.CLASS_NAME, value="quiz_response_text")
    answer3=answer3item.text.replace('\n','\n\n')

    #input('Press enter to continue: ')
    driver.switch_to.default_content()
    return student_id,student_name,answer1,answer2,answer3

def next():
    try:
        element_present = EC.element_to_be_clickable((By.ID, 'next-student-button'))
        WebDriverWait(driver, timeout).until(element_present)
        print('Found next button')
    except TimeoutException:
        print("Timed out waiting for page to load")
        return

    navbutton = driver.find_element(by=By.ID, value="next-student-button")
    navbutton.click()


# name1,name2,canvas_id,student_id
import csv

sids = {}
with open('student_lookup.csv', newline='') as studentfile:
    reader = csv.DictReader(studentfile)
    for row in reader:
        sids[row['canvas_id']] = row['student_id']

timeout = 10

service = Service(executable_path="/drivers/edge")
driver = webdriver.Edge(service=service)
driver.maximize_window()

driver.get("https://canvas.hull.ac.uk/courses/65765/gradebook/speed_grader?assignment_id=211938&student_id=182356")
submissions={}

finished=False
testcount=0
while finished==False:
    (student_id,student_name,title,desc,comments) = get_submission()
    if student_id in submissions:
        finished=True
    else:
        submissions[student_id]={'name':student_name,'title':title,'desc':desc,'comments':comments}
        next()
    testcount=testcount+1
    if testcount==100:
        finished=True




with open('output.md','w',encoding='utf-8') as outfile:
    for key,value in submissions.items():
        if key in sids.keys():
            sid = sids[key]
        else:
            sid = key
        outfile.write(f'# {sid} {value["name"]}\n\n')
        outfile.write(f'## {value["title"]}\n\n')
        outfile.write(f'{value["desc"]}\n\n')
        outfile.write(f'{value["comments"]}\n\n')
        outfile.write('\n---\n\n')
    

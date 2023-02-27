from selenium.webdriver.edge.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


timeout = 10

service = Service(executable_path="/drivers/edge")
driver = webdriver.Edge(service=service)
driver.maximize_window()

driver.get("https://canvas.hull.ac.uk/courses/65765/gradebook/speed_grader?assignment_id=211938&student_id=182356")

#input('Press enter to continue: ')

# The stuff of interest is inside an iframe, which must be selected
# <iframe id="speedgrader_iframe" src="/courses/65765/assignments/211938/submissions/182356?preview=true" frameborder="0" allowfullscreen="true"></iframe>

try:
    element_present = EC.presence_of_element_located((By.ID, 'speedgrader_iframe'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")


iframe=driver.find_element(by=By.ID, value="speedgrader_iframe")
driver.switch_to.frame(iframe)
question1 = driver.find_element(by=By.ID, value="question_466010")
answer1=question1.find_element(by=By.CLASS_NAME, value="quiz_response_text")
print(answer1.text)

question2 = driver.find_element(by=By.ID, value="question_466011")
answer2=question2.find_element(by=By.CLASS_NAME, value="quiz_response_text")
print(answer2.text)

#input('Press enter to continue: ')


driver.switch_to.default_content()

try:
    element_present = EC.presence_of_element_located((By.ID, 'next-student-button'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")

navbutton = driver.find_element(by=By.ID, value="next-student-button")
print(navbutton.id)
print(driver.current_url)

# Note that when the window opens, it may not be big enough to show the button.
# Selenium can't click a non-visible button.  So the window must be resized first.
button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'next-student-button')))
button.click()

print(driver.current_url)

button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'next-student-button')))
button.click()

button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'next-student-button')))
print(driver.current_url)


input('Press enter to continue: ')

#
# <button id="next-student-button" class="Button Button--icon-action gradebookMoveToNext next" type="button" aria-label="Next">
#            <i class="icon-arrow-right next" aria-hidden="true"></i>
#          </button>
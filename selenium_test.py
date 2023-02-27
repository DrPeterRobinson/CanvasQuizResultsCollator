from selenium.webdriver.edge.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

service = Service(executable_path="/drivers/edge")
driver = webdriver.Edge(service=service)

driver.get("https://canvas.hull.ac.uk/courses/65765/gradebook/speed_grader?assignment_id=211938&student_id=182356")

input('Press enter to continue: ')

question1 = driver.find_element(by=By.ID, value="question_466010_question_text")
answer1=question1.find_element(by=By.CLASS, value="user_content quiz_response_text")
print(answer1.text)

input('Press enter to continue: ')

question2 = driver.find_element(by=By.ID, value="question_466011_question_text")
answer2=question2.find_element(by=By.CLASS, value="user_content quiz_response_text")
print(answer2.text)

input('Press enter to continue: ')

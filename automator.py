from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoAlertPresentException
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from urllib.parse import quote
from sys import platform

options = Options()
if platform == "win32":
	options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

f = open("message.txt", "r")
message = f.read()
f.close()

print('This is your message\n\n')
print(message)
message = quote(message)

numbers = []
f = open("numbers.txt", "r")
for line in f.read().splitlines():
	if line != "":
		numbers.append(line)
f.close()
total_number=len(numbers)
print('\nFound ' + str(total_number) + ' numbers in the file')
print()
delay = 30

driver = webdriver.Chrome(ChromeDriverManager().install())
print('Waiting for login...')
driver.get('https://web.whatsapp.com')
input("Press ENTER once the chats are visible.")
for idx, number in enumerate(numbers):
	number = number.strip()
	# if the line is blank, skip the line
	if number == "":
		continue
	# if number starts with 0, remove the 0 and put +91 (as country code is required by whatsapp)
	if number[0] == "0":
		new = '+91' + number[1:]
		print(f"Changing {number} to: ", end = " ") 
		number = new
		print(number)
	# if there is no country code, add it
	if number[0] != '+':
		number = '+91' + number
	print('{}/{} => Sending message to {}.'.format((idx+1), total_number, number))
	try:
		url = 'https://web.whatsapp.com/send?phone=' + number + '&text=' + message
		sent = False
		for i in range(3):
			if not sent:
				driver.get(url)
				try:
					click_btn = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CLASS_NAME , '_4sWnG')))
				except Exception as e:
					print(f"Something went wrong..\n Failed to send message to: {number}, retry ({i+1}/3)")
					print("Make sure your phone and computer are connected to the internet.")
					print("If there is an alert, please dismiss it.")
					input("Press enter to continue")
				else:
					sleep(1)
					click_btn.click()
					sent=True
					sleep(3)
					print('Message sent to: ' + number)
	except Exception as e:
		print('Failed to send message to ' + number + str(e))

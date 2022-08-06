from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# Enter an integer as the number of locations per state
while True:
    print('Enter the number of locations per state:')
    try:
        n = int(input())
        break
    except ValueError:
        print("please enter an integer!")

# Enter the output csv file name
print('Enter the name of the output file (.csv):')
output = input() + ".csv"

# Ooptions for the Chrome Driver
options = Options()
options.add_argument('--lang=en-US')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option('useAutomationExtension', False)

# Make browser open
browser = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
          'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
          'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
          'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
          'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
          'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
          'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

# Total rows
ntotal = n * len(states)

# Count the number of locations
count = 1

# Open a csv file
with open(output, 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    # Titles of the table
    writer.writerow(["#", "Name", "Stars", "Reviews", "Type",
                    "Address", "State", "Phone"])

    # print the status
    print("----------Start!----------")
    status = ["% Done", "Current State"]
    print('{:<14s}{}'.format(*status))

    for s in states:
        # Obtain the Google Map URL
        url = "https://www.google.com/maps/search/2nd+hand+toy+stores+in+" + s

        # Open the Google Map URL
        browser.get(url)

        # Locate the window to scroll
        scr = browser.find_element(
            By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]')

        for i0 in range(n):
            # an index for the elements' xpath (3 for the 1st location, 5 for the 2nd ...)
            i = i0 * 2 + 3

            # scroll down if the next element is not visible
            try:
                browser.find_element(
                    By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]\
                        /div[1]/div[{}]/div/div[2]/div[2]/div[1]/div/div/div/div[1]'.format(i))    # next element
            except NoSuchElementException:
                # stop scrolling if reach the end
                try:
                    browser.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]\
                        /div/div[1]/div/div/div[2]/div[1]/div[243]/div/p/span')                 # "You've reached the end of the list." element
                    break         # move to the next state

                # scroll down
                except NoSuchElementException:
                    browser.execute_script(
                        "arguments[0].scrollTop = arguments[0].scrollHeight", scr)
                    # wait until the enxt element appears
                    WebDriverWait(browser, 20).until(
                        EC.presence_of_element_located((
                            By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]\
                                       /div[1]/div[{}]/div/div[2]/div[2]/div[1]/div/div/div/div[1]'.format(i))))    # next element

            # Obtain the title of the location
            title = browser.find_element(
                By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]\
                /div[1]/div[{}]/div/div[2]/div[2]/div[1]/div/div/div/div[1]'.format(i)).text

            # Obtain the ratings of the location
            try:
                stars = browser.find_element(
                    By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]\
                        /div[1]/div[{}]/div/div[2]/div[2]/div[1]/div/div/div/div[3]/div/span[2]/span[2]/span[1]'.format(i))
                stars = stars.text
            except NoSuchElementException:
                stars = "null"

            # Obtain the review numbers of the location
            try:
                reviews = browser.find_element(
                    By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]\
                        /div[1]/div[{}]/div/div[2]/div[2]/div[1]/div/div/div/div[3]/div/span[2]/span[2]/span[2]'.format(i))
                reviews = reviews.text[1:][:-1]
            except NoSuchElementException:
                reviews = "null"

            # Obtain the type of the location
            type = browser.find_element(
                By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]\
                    /div[1]/div[{}]/div/div[2]/div[2]/div[1]/div/div/div/div[4]/div[1]/span[1]/jsl'.format(i)).text

            # Obtain the address of the location
            try:
                location = browser.find_element(
                    By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/\
                        div[2]/div[1]/div[{}]/div/div[2]/div[2]/div[1]/div/div/div/div[4]/div[1]/span[2]/jsl/span[2]'.format(i))
                location = location.text
            except NoSuchElementException:
                location = "null"

            # Obtain the phone number of the location
            try:
                phonenum = browser.find_element(
                    By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/\
                        div[2]/div[1]/div[{}]/div/div[2]/div[2]/div[1]/div/div/div/div[4]/div[2]/span[2]/jsl/span[2]'.format(i))
                phonenum = phonenum.text
            except NoSuchElementException:
                phonenum = "null"

            # You can uncommen this to print out the locations we get
            # print(count, ',', title, ',', stars, ',', reviews, ',',
            #       type, ',', location, ',', s, ',', phonenum)

            # show the status (for each 10%)
            if (count/ntotal*10 - int(count/ntotal*10) == 0):
                status = [count/ntotal*100, "%", s]
                print('{}{:<10s}{}'.format(*status))

            # write the location information to the csv file
            writer.writerow([count, title, stars, reviews,
                            type, location, s, phonenum])

            count = count + 1

print("Total rows: ", count-1)
browser.close()

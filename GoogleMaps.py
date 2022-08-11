from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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

states_full = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
               'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
               'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
               'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
               'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
               'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
               'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN',
          'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS',
          'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA',
          'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

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
    # status = ["Locations", "Current State"]
    # print('{:<15s}{}'.format(*status))

    for s in states:
        # Obtain the Google Map URL
        url = "https://www.google.com/maps/search/toy+store+in+" + s

        # Open the Google Map URL
        browser.get(url)

        # Locate the window to scroll
        scr = browser.find_element(
            By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]')

        for i0 in range(n):
            # an index for the elements' xpath (3 for the 1st location, 5 for the 2nd ...)
            i = i0 * 2 + 3

            # scroll down until the next element is visible or the end is reached
            try:
                browser.find_element(
                    By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]\
                        /div[1]/div[{}]/div/div[2]/div[2]/div[1]/div/div/div/div[1]'.format(i))    # next element
            except NoSuchElementException:
                # stop scrolling if reach the end
                try:
                    # "You've reached the end of the list." element
                    browser.find_element(By.CLASS_NAME, 'PbZDve')
                    print("You've reached the end of the list.")
                    break         # move to the next state
                # scroll down
                except NoSuchElementException:
                    browser.execute_script(
                        "arguments[0].scrollTop = arguments[0].scrollHeight", scr)
                    try:
                        # wait until the next element appears
                        WebDriverWait(browser, 20).until(
                            EC.presence_of_element_located((
                                By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]\
                                        /div[1]/div[{}]/div/div[2]/div[2]/div[1]/div/div/div/div[1]'.format(i))))    # next element
                    except TimeoutException:
                        try:
                            # "You've reached the end of the list." element
                            browser.find_element(By.CLASS_NAME, 'PbZDve')
                            print("You've reached the end of the list.")
                        except:
                            raise TimeoutException
                        break

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
            # if (count/n - int(count/n) == 0):
            #     status = [count, s]
            #     print('{:<10i}{}'.format(*status))

            # write the location information to the csv file
            writer.writerow([count, title, stars, reviews,
                            type, location, s, phonenum])

            count = count + 1

        print(count-1, "locations read, ", s, "completed")

print("Total rows: ", count-1)
browser.close()

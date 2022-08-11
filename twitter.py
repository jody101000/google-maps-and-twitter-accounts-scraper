from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import csv
import time

# Enter an integer as the number of accounts
while True:
    print('Enter the number of accounts you want to get:')
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


# Count the number of accounts
count = 1

# Open a csv file
with open(output, 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    # Titles of the table
    writer.writerow(["#", "Name", "ID", "Bio", "Link"])

    # print the status
    print("----------Start!----------")
    # status = ["Locations", "Current State"]
    # print('{:<15s}{}'.format(*status))

    # Obtain the Google Map URL
    url = "https://twitter.com/search?q=parents&src=typed_query&f=user"

    # Open the Google Map URL
    browser.get(url)
    time.sleep(3)

    i0 = 1
    i = 1
    while i0 < n:
        # hover = ActionChains(browser)
        # m = browser.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/\
        #     div/div/div/div/div/div[2]/div/section/div/div/div[{}]/div/div/div/div/\
        #         div[1]/div/div/div[2]/div/div[2]/div/a/div[4]/div'.format(i))
        # hover.move_to_element(m).perform()
        # scroll down until the next element is visible or the end is reached
        try:
            browser.find_element(
                By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/\
                        div/div/div/div/div/div[2]/div/section/div/div/div[{}]/div/div/div/\
                        div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]'.format(i))    # next element
        except NoSuchElementException:
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            i = 19

        # Obtain the name of the account
        try:
            name = browser.find_element(
                By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/\
                    div/div/div/div/div/div[2]/div/section/div/div/div[{}]/div/div/div/\
                        div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]'.format(i)).text
        except NoSuchElementException:
            break

        try:
            id = browser.find_element(
                By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/\
                    div/div/div/div/div/div[2]/div/section/div/div/div[{}]/div/div/div/\
                        div/div[2]/div[1]/div[1]/div/div[2]'.format(i))
            id = id.text
            link = " https://twitter.com/" + id[1:]
        except NoSuchElementException:
            id = "null"
            link = " https://twitter.com/" + name[1:]

        try:
            bio = browser.find_element(
                By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/\
                div/div/div/div/div/div[2]/div/section/div/div/div[{}]/div/div/div/\
                    div/div[2]/div[2]'.format(i))
            bio = "'" + bio.text + "'"
        except NoSuchElementException:
            bio = "null"

        # hover = ActionChains(browser)
        # m = browser.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/\
        #     div/div/div/div/div/div[2]/div/section/div/div/div[{}]/div/div/div/div/\
        #         div[1]/div/div/div[2]/div/div[2]/div/a/div[4]/div'.format(i))
        # hover.move_to_element(m).perform().find_element(
        #     By.CLASS_NAME, 'css-1dbjc4n r-nsbfu8').text
        # time.sleep(5)
        # followers = browser.find_element(
        #     By.CLASS_NAME, 'css-1dbjc4n r-nsbfu8').text

        # You can uncommen this to print out the locations we get
        # print(count, ',', name, ',', id, ',', bio, ',', link)

        # show the status (for each 10%)
        # if (count/n - int(count/n) == 0):
        #     status = [count, s]
        #     print('{:<10i}{}'.format(*status))

        # write the location information to the csv file
        writer.writerow([count, name, id, bio, link])
        i = i + 1
        i0 = i0 + 1
        count = count + 1

    if (count/50 - int(count/50) == 0):
        print(count, "account read")

print("Total rows: ", count-1)
# browser.close()

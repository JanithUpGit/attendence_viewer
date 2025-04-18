from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.devtools.v133.runtime import StackTrace
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import webbrowser
import os



# Replace with your real credentials

# USERNAME = "tg1798"
# PASSWORD = "Jan02#@mis"

course_codes =[]
# Dictionary to store attendance data
attendance_data = {}

# Chrome options for headless (no window)
chrome_options = Options()
chrome_options.add_argument("--headless")  # 🧠 Hides the window
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--log-level=3")  # Optional: silences logs

# Start Chrome WebDriver in headless mode
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Example: open a site
driver.get("https://paravi.ruh.ac.lk/tecmis/index.php")

print("✅ Chrome headless browser opened TECMIS successfully")

while True:
    USERNAME = input("Enter username: ")
    PASSWORD = input("Enter password: ")

    # Step 2: Log in
    driver.find_element(By.NAME, "uname").send_keys(USERNAME)
    driver.find_element(By.NAME, "upwd").send_keys(PASSWORD + Keys.RETURN)

    # Step 3: Wait until dashboard loads
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Course')]")))
        print("✅ Logged in successfully")
        break
    except:
        print("❌ Login failed")

#find courses code and name
url = f"https://paravi.ruh.ac.lk/tecmis/index.php?view=admin&admin=22"
driver.get(url)

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/table/tbody/tr[3]/td/table[2]"))
    )
    table = driver.find_element(By.XPATH, "/html/body/div/table/tbody/tr[3]/td/table[2]")
    rows = table.find_elements(By.TAG_NAME, "tr")

    for row in rows[1:]:  # Skip header
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 2:
            course_code = cells[0].text.strip()
            course_name = cells[1].text.strip()
            course_codes.append((course_code, course_name))

    print("✅ Course codes loaded:", course_codes)

except Exception as e:
    print(f"\n⚠️ Could not load data for courses: {e}")
    course_codes = []



#find medical
medicals = []
url = f"https://paravi.ruh.ac.lk/tecmis/index.php?view=admin&admin=87"
driver.get(url)

try:
    link = driver.find_element(By.XPATH, '/html/body/div/table/tbody/tr[3]/td/div[1]/ul/li[3]/a')
    link.click()


    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/table/tbody/tr[3]/td/div[4]/table"))
    )
    table = driver.find_element(By.XPATH, "/html/body/div/table/tbody/tr[3]/td/div[4]/table")
    rows = table.find_elements(By.TAG_NAME, "tr")

    for row in rows[1:]:  # Skip header
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 2:
            medical_start_date = cells[2].text.strip()
            medical_end_date = cells[3].text.strip()
            medicals.append((medical_start_date, medical_end_date))

    if len(medicals) != 0:
        print("medicals found:", medicals)

except Exception as e:
    if isinstance(e, StackTrace):
        print(f"\n No medical data found")
    else:
        print(f"\n⚠️ Could not load data for medicals: {e}")
    medicals = []



for course_name in course_codes:

    course = course_name[0]

    url = f"https://paravi.ruh.ac.lk/tecmis/index.php?view=admin&admin=22&task=viewAtt&course={course}"
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/table/tbody/tr[3]/td/table[2]"))
        )
        table = driver.find_element(By.XPATH, "/html/body/div/table/tbody/tr[3]/td/table[2]")

        rows = table.text.strip().split("\n")
        headers = rows[0].split()  # Optional: use headers if needed
        data = [row.split() for row in rows[1:]]

        attendance_data[course] = data

        print(f"\n📚 Attendance for {course}:")
        for row in data:
            print(row)
    except Exception as e:
        print(f"\n⚠️ Could not load data for {course}: {e}")
        attendance_data[course] = []



if len(attendance_data) != 0 :

    with open("../username.json", "w", encoding="utf-8") as f:
        json.dump(USERNAME.upper(), f, ensure_ascii=False, indent=4)
    print("\n💾 username to username.json")



    with open("../courses.json", "w", encoding="utf-8") as f:
        json.dump(course_codes, f, ensure_ascii=False, indent=4)
    print("\n💾 Courses data saved to courses.json")


    with open("../attendance_data.json", "w", encoding="utf-8") as f:
        json.dump(attendance_data, f, ensure_ascii=False, indent=4)

    print("\n💾 Attendance data saved to attendance_data.json")


    with open("../medicals.json", "w", encoding="utf-8") as f:
        json.dump(medicals, f, ensure_ascii=False, indent=4)
    print("\n💾 Courses data saved to courses.json")


driver.quit()

# Path to your HTML file
html_file = os.path.abspath("../index.html")

# Open in default browser
webbrowser.open(f"file://{html_file}")


import requests
import json
import traceback
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
from email.message import EmailMessage
import ssl
import smtplib

webhook_url = 'https://hooks.zapier.com/hooks/catch/1928691/3f050s9/'
sign_in_url = 'https://sis5.gamecreekvideo.com'
my_calendar_url = 'https://sis5.gamecreekvideo.com/calendar-whiteboard.php?staff_id=5021'


def add_event_to_calendar(job):

    data = {'summary': job.text[:5],
            'description': job.text,
            'location': 'location-value',
            'start_date_time': job.parent.parent.parent.get('date'),
            'end_date_time': job.parent.parent.parent.get('date'),
            }
    print(data)
    with open("events.txt", 'a') as f:
        f.write("\n")
        f.write(job.text)
        f.close()
    #r = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    pass


def runtime_loop():
    counter = 0

    while True:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                print("chromium launched")
                page = browser.new_page()
                page.goto(sign_in_url)
                print("URL1 access")
                page.fill('input#gcv-signin-email', 'nmahoney@gamecreekvideo.com')
                page.fill('input#gcv-signin-password', 'letsGOavs0517!!!!')
                page.click('button#gcv-login-signin-submit')
                print("Sign in success")
                page.goto(my_calendar_url)
                print("Calendar access")

                html = page.inner_html('#calendarBody')

                soup = BeautifulSoup(html, 'html.parser')

                jobs = soup.find_all('a', {'jobid': True})

                print("Listed jobs: ")
                x = 0
                for job in jobs:
                    x += 1
                    print("Job " + str(x) + ":" + job.text)
                page.close()
                pass

            with open("jobdata.txt", 'r') as f:
                print("Checking known jobs file")
                file = f.read()
                # print(file)
                f.close()
                pass

            i = 0
            for job in jobs:
                i += 1
                if file.__contains__(job.text):
                    print("Job " + str(i) + " found in known jobs.")
                    continue
                else:
                    with open("jobdata.txt", 'a') as f:
                        print("Job " + str(
                            i) + " not found. Adding to calendar and writing to known jobs.")
                        f.write("\n")
                        #f.write(job.text)
                        f.close()
                        pass
                    add_event_to_calendar(job)
        except:
            print("Exception caught...")
            traceback.print_exc()

        counter += 1
        print("This loop has run " + str(counter) + " times!")
        print("Process complete. Going to sleep now...")
        time.sleep(3600)


runtime_loop()

import traceback
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
import os

sign_in_url = 'https://sis5.gamecreekvideo.com'
my_calendar_url = 'https://sis5.gamecreekvideo.com/calendar-whiteboard.php?staff_id=5021'
webhook_url = 'https://hooks.zapier.com/hooks/catch/1928691/3f050s9/'


class EventCalendar:
    def __init__(self, file_path='events.txt'):
        self.file_path = file_path
        self.events = set()
        self.load_events()

    def load_events(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                self.events = set(file.read().splitlines())

    def save_events(self):
        with open(self.file_path, 'w') as file:
            file.write('\n'.join(self.events))

    def add_event(self, event):
        if event not in self.events:
            self.events.add(event)
            self.save_events()
            print(f"Event added: {event}")
            return True
        else:
            print(f"Event already exists: {event}")
            return False

local_calendar = EventCalendar()


def job_summary_slicer(job):
    string_after_colon = job.text.split(':')[1]
    string_before_at = string_after_colon.split('@')[0]
    summary = string_before_at[1:-1]
    return summary


def job_location_slicer(job):
    string_after_at = job.text.split('@')[1]
    city = string_after_at.split(',')[0][1:]
    state = string_after_at.split(',')[1][1:3]
    return city + ', ' + state


def get_job_number(job):
    return job.text[:5]
    pass


def get_job_date(job):
    return job.parent.parent.parent.get('date')

def post_webhook(event):
    pass


def update_calendar(job):
    unique_job_string = get_job_date(job) + "!" + get_job_number(job)
    print(unique_job_string)
    if local_calendar.add_event(unique_job_string):
        r = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})



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

        numberedjobs = soup.findAll('a', {'jobid': True})
        otherjobs = soup.findAll('span', {'class': 'staffStatusAbbrev'})

        for job in numberedjobs:
            update_calendar(job)
            print("job number: " + get_job_number(job))
            print("date: " + get_job_date(job))
            print(job_summary_slicer(job))
            print(job_location_slicer(job) + '\n')

        for job in otherjobs:
            update_calendar(job)
            print("unnumbered job: " + job.parent.text)
            print("date: " + job.parent.parent.parent.get('date') + '\n')


except:
    print("Exception caught...")
    traceback.print_exc()
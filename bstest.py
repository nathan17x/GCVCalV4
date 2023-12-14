import traceback
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

sign_in_url = 'https://sis5.gamecreekvideo.com'
my_calendar_url = 'https://sis5.gamecreekvideo.com/calendar-whiteboard.php?staff_id=5018'


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

        numberedjobs = soup.findAll( 'a', {'jobid': True})
        otherjobs = soup.findAll('span', {'class': 'staffStatusAbbrev'})

        for job in numberedjobs:
            print("job number: " + job.text[:5])
            print("date: " + job.parent.parent.parent.get('date'))
            print(job.text + '\n')

        for job in otherjobs:
            print("unnumbered job: " + job.parent.text)
            print("date: " + job.parent.parent.parent.get('date') + '\n')







except:
    print("Exception caught...")
    traceback.print_exc()
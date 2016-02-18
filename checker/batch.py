import sys
import os
sys.path.append('..' + os.sep)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sitechecker.settings")

import time
import schedule

from pingdumb.main_module import get_status, get_strftime
from pingdumb.smtp_module import send_email
from checker.loadconf import load_smtp_conf
from checker.models import Site


def check():
    sites = Site.objects.all()
    for site in sites:
        st = get_strftime()
        url = Site.url_type(site.url)
        status = get_status(url)
        if status == "IOError: can't connect":
            msg = site.form_msg_status(st +
                           "\n" + url +
                           " Http status is " + status,
                           site.user.nickname + "@gmail.com")
            send_status_mail(msg)
            continue

        if int(status) >= 400:
            msg = site.form_msg_status(st +
                           "\n" + url +
                           " Http status is " + status,
                           site.user.nickname + "@gmail.com")
            send_status_mail(msg)


def send_status_mail(msg):
    s = load_smtp_conf()
    send_email(s, msg)
    s.quit()

    
if __name__ == "__main__":
    s = load_smtp_conf()
    s.quit()

    schedule.every(5).minutes.do(check)

    while True:
        schedule.run_pending()
        time.sleep(1)

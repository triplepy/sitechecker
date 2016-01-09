import smtplib
import schedule

from .models import Site

from pingdumb.main_module import get_status, get_strftime
from pingdumb.smtp_module import form_msg, send_email


def check():
    sites = Site.odjects.all()
    for site in sites:
        status = get_status(site.url)
        st = get_strftime()
        if status >= 400:
            msg = form_msg(st +
                           "\n" + site.url +
                           " Http status is " + status,
                           site.user.nickanme + "@gmail.com")
            send_status_mail(msg)


def load_smtp_conf():
    s = smtplib.SMTP("smtp.gmail.com:587")
    s.starttls()
    username = ""
    password = ""
    s.login(username, password)
    return s


def send_status_mail(msg):
    s = load_smtp_conf()
    send_email(s, msg)
    s.quit()


s = load_smtp_conf()
s.quit()
while True:
    schedule.every(5).minutes.do(check)

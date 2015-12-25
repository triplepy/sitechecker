from models import Site
import schedule
from pingdumb.main_module import get_status, get_strftime


def check():
    sites = Site.odjects.all()
    for site in sites:
        status = get_status(site.url)
        st = get_strftime()
        if status >= 400:
            msg = form_msgs(st +
                            "\n" + site.url +
                            " Http status is " +
                            status, site.user.nickanme + "@gmail.com")
            send_status_mail(msg) # Todo it needs implement


while True:
    schedule.every(5).minutes.do(check)

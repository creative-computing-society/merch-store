from apscheduler.schedulers.background import BackgroundScheduler

from .job import send_mails

scheduler = BackgroundScheduler()

def start():
    scheduler.add_job(send_mails, 'interval', minutes=1, replace_existing=True, id='send_mails', name='send_mails')
    scheduler.start()

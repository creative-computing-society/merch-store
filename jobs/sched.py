from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from .job import send_mails

scheduler = BackgroundScheduler(jobstores={'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')})

def start():
    scheduler.add_job(send_mails, 'interval', minutes=15, replace_existing=True, id='send_mails', name='send_mails')
    scheduler.start()

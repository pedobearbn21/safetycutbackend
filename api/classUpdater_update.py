from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .views import updater 

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(updater, 'interval', minutes=1)
    scheduler.start()   
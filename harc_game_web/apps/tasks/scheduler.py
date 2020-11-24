from apscheduler.schedulers.background import BackgroundScheduler

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Schedule the crone to close the task approvals at 1 sec after midnight on Saturday
    scheduler.add_job('apps.tasks.models:close_task_approvals',
        'cron', day_of_week='sat', hour=0, minute=0, second=1)
    scheduler.start()
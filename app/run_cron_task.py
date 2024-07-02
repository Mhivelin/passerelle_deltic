from app.models import passerelles

def run_cron_task():

    passerelles.routine()


if __name__ == '__main__':
    run_cron_task()
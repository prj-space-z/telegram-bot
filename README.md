> celery -A services.sheduler worker -B --loglevel=debug
> 
> aio_celery worker services.sheduler:app_celery
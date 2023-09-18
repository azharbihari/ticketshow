from celery import Celery, Task


def celery_init_app(app):
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery = Celery(app.name, task_cls=FlaskTask,
                    broker_connection_retry_on_startup=True)
    celery.config_from_object(app.config["CELERY"])
    celery.Task = FlaskTask
    celery.set_default()
    return celery

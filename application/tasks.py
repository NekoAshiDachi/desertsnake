import json
import sys
import time

from flask import render_template
from rq import get_current_job

from application import create_app, db
from application.models import Task, User, Post
from application.send_email import send_email

"""
If wanting multiple workers (should have # of workers >= available
CPUS), run more instances of rq worker, all connected to same queue. Does not
preserve history of executed jobs.

to configure settings (URL, host, password):
desertsnake/redis_settings.py

bash console:
rq info -c redis_settings
rq worker tasks -c redis_settings

separately, in python console:
from rq import Queue, Connection
from redis import Redis
import os
from dotenv import load_dotenv

load_dotenv()
conn = Redis.from_url(os.environ.get('REDIS_URL'))
queue = Queue('tasks', connection=conn)

OR

with Connection(Redis(host, port, password):
    queue = Queue('tasks')

task name as function obj or import str; following args are for task function:
job = queue.enqueue('application.tasks.example', 23)
job.get_id() -> c651de7f-21a8-4068-afd5-8b982a6f6d32

job.is_finished
job.meta
job.refresh()  # updates contents from Redis
"""

# ------------------------------------------------------------------------------

# app is the only module rq worker requires and imports
app = create_app()

"""push makes app context "current" app instance; enables extensions such as
Flask-SQLAlchemy to use current_app.config"""
app.app_context().push()


def example(seconds):
    job = get_current_job()
    print('Starting task')
    for i in range(seconds):
        """job.meta is dict for custom data communicated to app;
        job.save_meta() writes data to Redis, where app can find it"""
        job.meta['progress'] = 100.0 * i / seconds
        job.save_meta()
        print(i)
        time.sleep(1)
    job.meta['progress'] = 100
    job.save_meta()
    print('Task completed')


def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        task.user.add_notification(
            'task_progress', {'task_id': job.get_id(), 'progress': progress})
        if progress >= 100:
            task.complete = True
        db.session.commit()


# runs in separate rq process rather than Flask, so needs own error handling
def export_posts(user_id):
    try:
        user = User.query.get(user_id)
        _set_task_progress(0)
        data = []
        post_n = 0
        total_posts = user.posts.count()
        for post in user.posts.order_by(Post.timestamp.asc()):
            data.append({
                'body': post.body,
                # 'Z' at end of timestamp indicates UTC timezone
                'timestamp': post.timestamp.isoformat() + 'Z'})
            # makes export task last longer, for seeing progress go up
            time.sleep(5)
            post_n += 1
            _set_task_progress(100 * post_n // total_posts)

        send_email('[Microblog] Your blog posts',
            sender=app.config['ADMINS'][0], recipients=[user.email],
            text_body=render_template('email/export_posts.txt', user=user),
            html_body=render_template('email/export_posts.html',
                                      user=user),
            attachments=[('posts.json', 'application/json',
                          json.dumps({'posts': data}, indent=4))],
            sync=True)
    except:
        _set_task_progress(100)
        """error and stack trace from sys.exc_info(); uses app Flask logger
        (e.g., admin error emails)"""
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())


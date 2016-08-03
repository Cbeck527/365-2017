"""
Fabric automation for building and deploying this S3-based website
"""
import os

from datetime import datetime, timedelta
from fabric import api

@api.task
def build():
    """
    Compile the stite from jekyll sources
    """
    api.local('jekyll build')


@api.task
def push_to_s3():
    """
    Push website to S3 and clear cloudfront cache (built-in to s3_website)
    """
    api.local('s3_website push')


@api.task
def deploy():
    """
    Build site and push to S3
    """
    api.execute(build)
    api.execute(push_to_s3)


@api.task
def new_roll(first=None, last=None, start_date=None):
    """
    When a new roll of film is developed, build the set of posts in the
    sequence starting at ``fist`` and going to ``last`` - incrementing
    the date by one from ``start_date``

    The template is written out as a markdown file in the src/_posts
    directory with the proper filename based on the date and number in
    the sequence; e.g. 2016-05-27-1.md
    """
    if not first and not last and not start_date:
        api.abort('Please specify start date, first, and last photo in the sequence')

    draft_filename = os.path.join(os.path.dirname(__file__), 'src/_drafts/template.md')
    posts_directory = os.path.join(os.path.dirname(__file__), 'src/_posts')

    with open(os.path.expanduser(draft_filename)) as inputfile:
        text = inputfile.read()
        date = datetime.strptime(start_date, '%Y-%m-%d')
        for num in xrange(int(first), int(last) + 1):
            with open(
                os.path.join(posts_directory,
                '{0}-{1}.md'.format(date.strftime('%Y-%m-%d'), num)),
                'w') as post:
                post.write(text.format(day_number=num, date=date.strftime('%Y-%m-%d')))
            date += timedelta(days=1)

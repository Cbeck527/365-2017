"""
Fabric automation for building and deploying this S3-based website
"""
import os
import yaml

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
def new_roll(seq_start=None, start_date=None, meta_file=None):
    """
    When a new roll of film is developed, build the set of posts in the
    sequence starting at ``fist`` through all of the files untracked by git;
    incrementing the date by one from ``start_date``

    An optional YAML file can exist with the title and locations for the
    images being imported. The YAML file's structure looks like:

    ```
    - title: Picture
      location: Location
    - title: Picture 2
      location: Location 2
    ```

    The template is written out as a markdown file in the src/_posts
    directory with the proper filename based on the date and number in
    the sequence; e.g. 2016-05-27-1.md
    """
    if not seq_start or not start_date:
        error_message = ("Please specify start date and the number of the first photo in the sequence\n"
                         "Usage:\n\n"
                         "    $ fab new_roll:seq_start=100,start_date=2016-01-01")
        api.abort(error_message)

    new_images = api.local('git ls-files --others --exclude-standard src/images/',
                           capture=True).split('\n')
    draft_filename = os.path.join(os.path.dirname(__file__), 'src/_drafts/template.md')
    posts_directory = os.path.join(os.path.dirname(__file__), 'src/_posts')
    if meta_file:
        with open(meta_file, 'r') as f:
            meta_info = yaml.load(f)
    else:
        meta_info = None

    with open(os.path.expanduser(draft_filename)) as inputfile:
        text = inputfile.read()
        try:
            date = datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError as e:
            api.abort("Unable to parse date, ensure it's formatted as YYYY-MM-DD.")

        for index, sequence_number in enumerate(new_images):
            photo_number = index + int(seq_start)
            with open(os.path.join(posts_directory, '{0}-{1}.md'.format(date.strftime('%Y-%m-%d'),
                                                                        photo_number)), 'w') as post:
                if meta_info:
                    post.write(text.format(day_number=photo_number,
                                           date=date.strftime('%Y-%m-%d'),
                                           title=meta_info[index]['title'],
                                           location=meta_info[index]['location']))
                else:
                    post.write(text.format(day_number=photo_number,
                                           date=date.strftime('%Y-%m-%d'),
                                           title='',
                                           location=''))
            date += timedelta(days=1)

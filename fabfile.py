"""
Fabric automation for building and deploying this S3-based website
"""
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

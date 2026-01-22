"""To make sure that app is always imported"""
from __future__ import absolute_import
from .celery import app as celery_app

__all__ = ('celery_app',)

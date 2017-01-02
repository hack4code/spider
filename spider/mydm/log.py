# -*- coding: utf-8 -*-


from celery.utils.log import get_task_logger
from scrapy.utils.project import get_project_settings


settings = get_project_settings()
logger = get_task_logger(settings['LOGGER_NAME'])

#!/usr/bin/env python
import os
import sys
'''
打开cmd 进入目标路径
项目名： mysite
输入 django-admin startproject mysite
创建 mysite文件夹
然后输入 python manage.py startapp learn
新建一个应用(app), 名称叫 learn
创建 learn文件夹
'''
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)

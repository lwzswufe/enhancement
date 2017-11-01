#!/usr/bin/env python
import os
import sys
'''
打开cmd
django-admin.py startproject new_models # 新建一个项目
cd new_models # 进入到该项目的文件夹
django-admin.py startapp people # 新建一个 people 应用（app)

同步一下数据库（我们使用默认的数据库 SQLite3，无需配置）
# Django 1.7 及以上的版本需要用以下命令
python manage.py makemigrations
python manage.py migrate
'''

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "query_set.settings")
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

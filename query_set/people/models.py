from django.db import models

'''
name 和 age 等字段中不能有 __（双下划线，因为在Django QuerySet API中有特殊含义
（用于关系，包含，不区分大小写，以什么开头或结尾，日期的大于小于，正则等）
也不能有Python中的关键字，name 是合法的，student_name 也合法，但是student__name
不合法，try, class, continue 也不合法，因为它是Python的关键字( import keyword;
 print(keyword.kwlist) 可以打出所有的关键字)
'''
# 我们新建了一个Person类，继承自models.Model, 一个人有姓名和年龄。
class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __unicode__(self):  # __str__ on Python 3
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __unicode__(self):  # __str__ on Python 3
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __unicode__(self):  # __str__ on Python 3
        return self.headline

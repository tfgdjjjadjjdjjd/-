from django.db import models

class Student(models.Model):
    name=models.CharField(verbose_name="学生姓名",max_length=32)
    age=models.CharField(verbose_name="学生年龄",max_length=32)
    student_type=models.ForeignKey(to="StudentType")

    def __str__(self):
        return self.name


class StudentType(models.Model):
    name=models.CharField(max_length=32,verbose_name="学生类型")

    def __str__(self):
        return self.name

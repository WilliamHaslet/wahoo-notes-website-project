from django.db import models

# Create your models here.

class Student(models.Model):
    computing_id = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    year = models.IntegerField()
    email = models.EmailField()

class Class(models.Model):
    name = models.CharField(max_length=30)
    professor = models.CharField(max_length=30)
    time = models.CharField(max_length=30)
    semester = models.CharField(max_length=30)

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Deepthought(models.Model):
    title_text = models.CharField(max_length=200)
    thought_text = models.CharField(max_length=200)
    def __str__(self):
        return self.thought_text
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    text = models.CharField(max_length=250)
    num_right = models.IntegerField(verbose_name='total answers')

    def __str__(self):
        return self.text
    
    def get_question(self, id):
        return Question.objects.get(id=id)

    def get_answers(self):
        return Answer.objects.filter(question=self)

    def get_right_answer(self):
        answer = Answer.objects.get(question=self, right=True)
        return answer.id

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ['-id']

    

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    right = models.BooleanField(verbose_name='right answer', default=False)

    def __str__(self):
        return self.text

class CategoryTest(models.Model):
    title = models.CharField(max_length=250, verbose_name='title')
    theory = models.CharField(max_length=1000, verbose_name='theory')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category of test'
        verbose_name_plural = 'Categories of test'
        ordering = ['-id']

class Tests(models.Model):
    category_test = models.ForeignKey(CategoryTest , verbose_name='category_test', on_delete=models.CASCADE)
    title = models.CharField(max_length=250, verbose_name='test')
    questions = models.ManyToManyField(Question)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'
        ordering = ['-id']

    def __repr__(self):
        return f'{self.id}'

class ResultTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Tests, on_delete=models.CASCADE)
    result = models.CharField(max_length=250, verbose_name='result')
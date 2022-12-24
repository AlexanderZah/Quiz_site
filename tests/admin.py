from django.contrib import admin

from .models import (
    Question, Answer, Tests, ResultTest, CategoryTest
)

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    
    def __str__(self):
        return Question.text
    

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Tests)
admin.site.register(ResultTest)
admin.site.register(CategoryTest)
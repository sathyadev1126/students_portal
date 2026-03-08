from django.contrib import admin
from .models import Topic, Question, Result, Company, CompanyTest

admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(Result)
admin.site.register(Company)
admin.site.register(CompanyTest)
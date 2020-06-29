from django.contrib import admin
from MyApp.models import Feedback, Question, MyProfile, Post, PostComment

admin.site.register(Feedback)
admin.site.register(Question)
admin.site.register(MyProfile)
admin.site.register(Post)
admin.site.register(PostComment)

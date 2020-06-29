from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from tinymce import models as tinymce


class Feedback(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=225)
    email = models.EmailField(max_length=225)
    message = models.TextField(max_length=225)
    date = models.DateField(auto_now_add=True)


class Question(models.Model):
    objects = models.Manager()
    question = models.TextField()
    option_one = models.CharField(max_length=30)
    option_two = models.CharField(max_length=30)
    option_three = models.CharField(max_length=30)
    option_one_count = models.IntegerField(default=0)
    option_two_count = models.IntegerField(default=0)
    option_three_count = models.IntegerField(default=0)
    status = models.BooleanField(default=False)

    def total(self):
        return self.option_one_count + self.option_two_count + self.option_three_count


class MyProfile(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=150, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics', blank=True, null=True)


@receiver(post_save, sender=User)
def update_my_profile(sender, instance, created, **kwargs):
    if created:
        MyProfile.objects.create(user=instance)
        instance.myprofile.save()


class Post(models.Model):
    objects = models.Manager()
    CATEGORY_CHOICES = (
        ("Django", "Django"),
        ("Python", "Python"),
        ("Java", "Java"),
        ("C++", "C++"),
        ("C", "C"),
        ("HTML", "HTML"),
        ("CSS", "CSS"),
        ("Bootstrap", "Bootstrap"),
        ("HTML/CSS/Bootstrap-Coding", "HTML/CSS/Bootstrap-Coding"),
        ("Database", "Database"),
    )
    name = models.ForeignKey(User, on_delete=models.PROTECT, related_name='name')
    title = models.CharField(max_length=100, blank=False, null=False)
    category = models.CharField(choices=CATEGORY_CHOICES, default='Django', max_length=100, blank=False, null=False)
    content = tinymce.HTMLField(blank=False, null=False)
    file = models.ImageField(upload_to='project_files', null=True, blank=True)
    slug = models.CharField(max_length=130)
    date_posted = models.DateTimeField(default=now)
    favourite = models.ManyToManyField(User, related_name='favourite', blank=True)

    def __str__(self):
        return self.title


class PostComment(models.Model):
    objects = models.Manager()
    sno = models.AutoField(primary_key=True)
    comment = models.TextField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reply = models.ForeignKey('PostComment', on_delete=models.CASCADE, null=True, related_name='replies')
    timestamp = models.DateTimeField(default=now)

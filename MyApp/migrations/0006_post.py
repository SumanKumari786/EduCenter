# Generated by Django 3.0.4 on 2020-06-25 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MyApp', '0005_myprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('Django', 'Django'), ('Python', 'Python'), ('Java', 'Java'), ('C++', 'C++'), ('C', 'C'), ('HTML', 'HTML'), ('CSS', 'CSS'), ('Bootstrap', 'Bootstrap'), ('HTML/CSS/Bootstrap-Coding', 'HTML/CSS/Bootstrap-Coding'), ('Database', 'Database')], default='Django', max_length=100)),
                ('content', tinymce.models.HTMLField()),
                ('file', models.ImageField(blank=True, null=True, upload_to='project_files')),
                ('slug', models.CharField(max_length=130)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('favourite', models.ManyToManyField(blank=True, related_name='favourite', to=settings.AUTH_USER_MODEL)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='name', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 5.1.1 on 2025-01-23 22:47

import datetime
import django.db.models.deletion
import django.utils.timezone
import volunteering.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Opportunity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('time', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('location', models.CharField(blank=True, max_length=300)),
                ('description', models.CharField(blank=True, max_length=1000)),
                ('applications_count', models.DecimalField(decimal_places=0, default=0, max_digits=4)),
                ('like_count', models.DecimalField(decimal_places=0, default=0, max_digits=4)),
                ('comment_count', models.DecimalField(decimal_places=0, default=0, max_digits=4)),
                ('profile_picture', models.ImageField(blank=True, upload_to=volunteering.models.upload_to)),
                ('cover_image', models.ImageField(blank=True, upload_to=volunteering.models.upload_to)),
                ('post_image', models.ImageField(blank=True, upload_to=volunteering.models.upload_to)),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opportunity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteering.opportunity')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=500)),
                ('answer_text', models.CharField(max_length=500)),
                ('answer_type', models.CharField(max_length=200)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteering.application')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=400)),
                ('last_name', models.CharField(blank=True, max_length=400)),
                ('name', models.CharField(blank=True, max_length=1000)),
                ('date_of_birth', models.DateField(default=datetime.date(2025, 1, 23))),
                ('gender', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('account_type', models.CharField(blank=True, max_length=200)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to=volunteering.models.upload_to)),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to=volunteering.models.upload_to)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserAddedParticipation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=200)),
                ('organiser', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=500)),
                ('start_date', models.DateField(default=datetime.date(2025, 1, 23))),
                ('end_date', models.DateField(default=datetime.date(2025, 1, 23))),
                ('description', models.CharField(max_length=1000)),
                ('diploma', models.FileField(blank=True, upload_to='diplomas/')),
                ('participation_picture', models.ImageField(blank=True, upload_to=volunteering.models.upload_to)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteering.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(blank=True, max_length=200)),
                ('function', models.CharField(blank=True, max_length=200)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('location', models.CharField(blank=True, max_length=300)),
                ('description', models.CharField(blank=True, max_length=1000)),
                ('opportunity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteering.opportunity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteering.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Callout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.CharField(blank=True, max_length=300)),
                ('callout_picture', models.ImageField(blank=True, upload_to=volunteering.models.upload_to)),
                ('sender', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='volunteering.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='UserToCallout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('callout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteering.callout')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteering.userprofile')),
            ],
        ),
    ]

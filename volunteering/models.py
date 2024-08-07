from django.db import models
from django.utils import timezone 

class Experience(models.Model):
    
    # identification
    name = models.CharField(max_length=200)
    time = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=300, blank=True)

    # customized details
    description = models.CharField(max_length=1000)

    def __str__(self):
        return f"Experience: {self.name}, at {self.time}: {self.description}"

class Notification(models.Model):
    
    title = models.CharField(max_length=200, blank=True)
    time = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f"Notification: {self.title}, at {self.time}: {self.description}"


class Volunteer(models.Model):
    
    #control
    username = models.CharField(max_length=64)

    # identification
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date_of_birth = models.DateField(default=timezone.localtime(timezone.now()).date())
    gender = models.CharField(max_length=100, blank=True)

    # customized details
    description = models.CharField(max_length=1000, blank=True)
    link_to_pfp = models.CharField(max_length=2000, blank=True)
    link_to_cover_image = models.CharField(max_length=2000, blank=True)

    # stats
    number_of_times_volunteered = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    hours_of_volunteering = models.FloatField(default=0)
    account_creation_date = models.DateField(default=timezone.localtime(timezone.now()).date())

    #relationships
    notifications = models.ManyToManyField(Notification, blank=True)
    experiences = models.ManyToManyField(Experience, blank=True)

    def __str__(self):
        return f"Volunteer: @{self.username} ({self.first_name} {self.last_name})"

class Organiser(models.Model):
     
    #control
    username = models.CharField(max_length=64)

    # identification
    name = models.CharField(max_length=200)

    # customized details
    description = models.CharField(max_length=1000, blank=True)
    link_to_pfp = models.CharField(max_length=2000, blank=True)
    link_to_cover_image = models.CharField(max_length=2000, blank=True)

    # stats
    events_organised = models.DecimalField(max_digits=4, decimal_places=2, blank=True)
    account_creation_date = models.DateField(default=timezone.localtime(timezone.now()).date())

    def __str__(self):
        return f"Organiser: @{self.username} ({self.name})"

class Event(models.Model):
    
    # identification
    name = models.CharField(max_length=200)
    time = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=300, blank=True)

    # customized details
    description = models.CharField(max_length=1000, blank=True)
    link_to_pfp = models.CharField(max_length=2000, blank=True)
    link_to_cover_image = models.CharField(max_length=2000, blank=True)

    # stats
    number_of_volunteers = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    edition = models.DecimalField(max_digits=4, decimal_places=0, default=1)

    # relationships
    volunteers = models.ManyToManyField(Volunteer, blank=True)
    organisers = models.ManyToManyField(Organiser, blank=True)

    def __str__(self):
        return f"Event: {self.name}, at {self.time} {self.location}"



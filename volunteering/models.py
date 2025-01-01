from django.db import models
from django.utils import timezone, tree 

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class User(models.Model):
    username = models.CharField(max_length=64)

    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=200, blank=True)

    date_of_birth = models.DateField(default=timezone.localtime(timezone.now()).date()) # necessary?
    gender = models.CharField(max_length=100, blank=True) # necessary?

    account_creation_date = models.DateField(default=timezone.localtime(timezone.now()).date())

    description = models.CharField(max_length=1000, blank=True)

    account_type = models.CharField(max_length=200, blank=True)
    profile_picture = models.ImageField(blank=True, upload_to=upload_to)
    cover_image = models.ImageField(blank=True, upload_to=upload_to)

    def __str__(self):
        return f"User: @{self.username} ({self.first_name} {self.last_name})"


class Opportunity(models.Model):
    name = models.CharField(max_length=200, blank=True)
    time = models.DateTimeField(default=timezone.now, blank=True)
    location = models.CharField(max_length=300, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    applications_count = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    like_count = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    comment_count = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    profile_picture = models.ImageField(blank=True, upload_to=upload_to)
    cover_image = models.ImageField(blank=True, upload_to=upload_to)
    post_image = models.ImageField(blank=True, upload_to=upload_to)

    def __str__(self):
        return f"Opportunity: {self.name}, at {self.time} {self.location}"


class Callout(models.Model):
    title = models.CharField(max_length=200, blank=True)
    time = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=300, blank=True)
    callout_picture = models.ImageField(blank=True, upload_to=upload_to)

    sender = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"Callout: {self.title}, at {self.time}: {self.description}"


class Application(models.Model):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)


class Question(models.Model):
    question_text = models.CharField(max_length=500)

    answer_text = models.CharField(max_length=500)
    answer_type = models.CharField(max_length=200)

    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    

class UserAddedParticipation(models.Model):
    role = models.CharField(max_length=200) 
    organiser = models.CharField(max_length=200) 

    location = models.CharField(max_length=500) 

    start_date = models.DateField(default=timezone.localtime(timezone.now()).date()) 
    end_date = models.DateField(default=timezone.localtime(timezone.now()).date()) 

    description = models.CharField(max_length=1000) 

    diploma = models.FileField(blank=True, upload_to="diplomas/")
    participation_picture = models.ImageField(blank=True, upload_to=upload_to)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# ------------------------------ HYBRID ------------------------------ 

class Participation(models.Model):
    role = models.CharField(max_length=200, blank=True)
    function = models.CharField(max_length=200, blank=True)
    time = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=300, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)

class UserToCallout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    callout = models.ForeignKey(Callout, on_delete=models.CASCADE) 

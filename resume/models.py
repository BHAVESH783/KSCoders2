from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver


# Create your models here.
class Resume(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Image")
    firstName = models.CharField(max_length=30, default='')
    lastName = models.CharField(max_length=30, default='')
    email = models.EmailField(null=True)
    profilePicture = models.FileField(upload_to="profiles", null=True)
    phoneNumber = models.IntegerField()
    male = "Male"
    female = "Female"
    others = "Others"
    gender_choices = (
        (male, male),
        (female, female),
        (others, others)
    )
    gender = models.CharField(max_length=10, choices=gender_choices)
    aboutMe = models.CharField(max_length=200)
    codingLanguage = models.CharField(max_length=200)
    hobbies = models.CharField(max_length=200)
    education = models.CharField(max_length=300)
    skills = models.CharField(max_length=300)
    exp = models.CharField(max_length=300, default='')

    def __str__(self):
        return self.firstName+str(self.id)

    def delete(self, using=None, keep_parents=False):
        # print("DOING")
        self.profilePicture.storage.delete(self.profilePicture.name)
        super().delete()


@receiver(pre_delete, sender=User)
def signal_function_name(sender, instance, using, **kwargs):
    alls = instance.Image.all()
    for i in alls:
        i.profilePicture.storage.delete(i.profilePicture.name)

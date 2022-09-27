from django.db import models
import os
from django.conf import settings
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver


# Create your models here.
class Pages(models.Model):
    name = models.CharField(max_length=20, unique=True)
    # file = models.FileField(upload_to="pages", null=True)

    def store(self, content):
        if not content == '':
            f = open(os.path.join(settings.MEDIA_ROOT, 'pages/'+self.name+'.txt'), 'w')
            f.write(content)
            f.close()

    def read(self):
        f = open(os.path.join(settings.MEDIA_ROOT, 'pages/' + self.name + '.txt'), 'r')
        content = f.read()
        return content

    def delete(self, using=None, keep_parents=False):
        f = os.path.join(settings.MEDIA_ROOT, 'pages/'+self.name+'.txt')
        if os.path.exists(f):
            os.remove(f)


@receiver(pre_delete, sender=Pages)
def signal_function_name(sender, instance, using, **kwargs):
    f = os.path.join(settings.MEDIA_ROOT, 'pages/'+instance.name+'.txt')
    if os.path.exists(f):
        os.remove(f)

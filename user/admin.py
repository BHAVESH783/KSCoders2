from django.contrib import admin
from .models import Address, Suffix, PhoneNumber, Verify, ContactUs

# Register your models here.
admin.site.register(Suffix)
admin.site.register(Address)
admin.site.register(PhoneNumber)
admin.site.register(Verify)
admin.site.register(ContactUs)

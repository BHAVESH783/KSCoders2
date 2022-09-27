from django.db import models
from django.contrib.auth.models import User
# from seller.models import Product


# Create your models here.
class Address(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Address")
    name = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200, default='')
    Pincode = models.IntegerField()
    City = models.CharField(max_length=30)
    State = models.CharField(max_length=30)
    Country = models.CharField(max_length=20, default='')
    prior = models.IntegerField(default=0)

    def __str__(self):
        return self.address


class Credits(models.Model):  # Payment Recieved
    person = models.ForeignKey(User, on_delete=models.PROTECT)
    amount = models.IntegerField()
    currency = models.CharField(max_length=20)
    date = models.DateField()


class Debits(models.Model):  # Amount Used
    person = models.ForeignKey(User, on_delete=models.PROTECT)
    amount = models.IntegerField()
    currency = models.CharField(max_length=20)
    date = models.DateField()


class PhoneNumber(models.Model):  # No Need
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="PhoneNumber")
    name = models.CharField(max_length=30, default='Personal')
    number = models.IntegerField()
    verified = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.number


class Suffix(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="suffix")
    customer = 'customer'
    seller = 'seller'
    admin = 'admin'
    user_type = (
        (customer, customer),
        (seller, seller),
        (admin, admin)
    )
    type = models.CharField(max_length=10, choices=user_type)
    content = models.IntegerField(default=10)

    def __str__(self):
        return self.person.username


class Verify(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verify")
    name = models.BooleanField()  # 0 for Email 1 for Phone Number
    OTP = models.CharField(max_length=64, default="0")
    times = models.DateTimeField()
    status = models.BooleanField(default=False)
    message = models.CharField(max_length=20, default="", null=True)
    loop = models.IntegerField(default=0)

    def __str__(self):
        return self.person.username + str(self.name)


# class Matrix(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Visits")
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="matrix")
#     visit = models.IntegerField()


class ContactUs(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    message = models.CharField(max_length=500)

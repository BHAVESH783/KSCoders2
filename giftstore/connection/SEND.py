import math
import random
from django.shortcuts import render
from .gmail.gmail import sendmail


def generateOTP():
    # Declare a digits variable
    # which stores all digits
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


def sendSMS(text, phone):
    print("SMS sent to ", phone)
    print("TYPE ", text)


def sendMail(text, emailId, template=0, r=''):
    if template == 0:
        response = render(r, "communication/otpMail.html", {"otp": text})
    elif template == 1:
        response = render(r, "communication/otpMail.html", {"otp": "click here to verify", "link": text})
    text = str(response.content.decode())
    sendmail(text, emailId, "checking Email")

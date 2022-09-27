from django.shortcuts import render, redirect
from giftstore.views import check_log
from .models import Resume
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User


# Create your views here.
def makenew(r):
    if check_log(r):
        return render(r, 'resume/form1.html')
    return redirect('home')


def savenew(r):
    if check_log(r):
        if r.method == "POST":
            file = r.FILES['dp']
            firstname = r.POST['firstName']
            lastname = r.POST['lastName']
            email = r.POST['email']
            phone = r.POST['phone']
            gender = ''
            try:
                male = r.POST['male']
                gender = Resume.male
            except MultiValueDictKeyError:
                try:
                    female = r.POST['female']
                    gender = Resume.female
                except MultiValueDictKeyError:
                    gender = Resume.others
                    # others = r.POST['others']

            aboutme = r.POST['aboutme']
            coding = r.POST['coding']
            hobbies = r.POST['hobbies']
            education = r.POST['education']
            skilld = r.POST['skills']
            exp = r.POST['exp']

            newR = Resume(person=r.user, firstName=firstname, lastName=lastname, email=email, profilePicture=file,
                          phoneNumber=phone, gender=gender, aboutMe=aboutme, codingLanguage=coding, education=education,
                          skills=skilld, hobbies=hobbies, exp=exp)
            newR.save()
        return redirect('home')


def index(r):
    if check_log(r):
        return render(r, 'resume/post.html', {'d': r.user.Image.all()})
    return redirect('home')


def show(r, username, resume):
    tempUser = User.objects.filter(username=username)
    if tempUser:
        mainU = tempUser[0]
        allrs = mainU.Image.filter(id=resume)
        if allrs:
            return render(r, "resume/template1.html", {'d': allrs[0]})
    return redirect('home')

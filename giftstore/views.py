import datetime
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import MinimumLengthValidator, UserAttributeSimilarityValidator, \
    CommonPasswordValidator, NumericPasswordValidator, ValidationError
import hashlib
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth import logout as lgout
from user.models import Address, PhoneNumber, Suffix, Verify, ContactUs
from django.utils.datastructures import MultiValueDictKeyError
# from seller.models import Product, Category, CatData
# from cart.models import Order, Group, clearbug
from .connection.SEND import *
from django.db.models import Count
from django.db.models import Q
from .my_captcha import FormWithCaptcha
from datetime import timezone
# from writer.models import Post
from django.db.models import Count
from django.db.models import Q


def get_hex(s):
    hexStr = hashlib.sha256(s.encode('utf-8')).hexdigest()
    return hexStr


def check_log(r):
    navt = True
    if str(r.user) == "AnonymousUser":
        navt = False
    else:
        obj = r.user.verify.get(name=False)
        if obj != "0" and not obj.status:
            return redirect('Email')
    return navt


def getURL(r, url, media=False, need="/cart/"):
    if media:
        need = "/cart/media/"
    http = 'http'
    if r.is_secure():
        http += 's'
    pro = r.META["HTTP_HOST"]
    return http + "://" + pro + need + str(url)


# def bestSeller(num):
#     allo = Order.objects.all().values('product').annotate(total=Count('product')).order_by('total')
#     allpro = []
#     for i in allo:
#         if num == 0:
#             break
#         else:
#             pro = Product.objects.get(id=i['product'])
#             clearbug(pro.Name)
#             if pro.instock > 0:
#                 allpro.append(pro)
#                 num -= 1
#     return allpro


# def latest(num):
#     allo = Product.objects.all().order_by('id').reverse()
#     inl = list(allo)
#     for p in allo:
#         clearbug(p.Name)
#         if p.instock < 1 and not p.ShowOUTproduct:
#             inl.remove(p)
#     if len(inl) < num:
#         return inl[:num]
#     else:
#         return inl


# def recently(r, num):
#     if check_log(r):
#         get = r.user.Visits.all().values('product').order_by('visit').reverse()
#     else:
#         get = Matrix.objects.all().values('product').order_by('visit').reverse()
#     allo = []
#     for v in get:
#         if num == 0:
#             break
#         allpro = Product.objects.get(id=v['product'])
#         clearbug(allpro.Name)
#         if not (allpro.instock == 0 and not allpro.ShowOUTproduct):
#             pro = allpro
#             allo.append(allpro)
#             num -= 1
#
#     if len(allo) < num:
#         return allo
#     else:
#         return allo[:num]


# def relatedPro(Pname, num):
#     allp = Product.objects.get(Name=Pname)
#     getp = allp.Categories.values('product').annotate(prior=Count('product')).order_by('prior')
#     pobj = []
#     for i in getp:
#         p = Product.objects.get(id=i['product'])
#         clearbug(p.Name)
#         if not (p.instock == 0 and not p.ShowOUTproduct):
#             pobj.append(p)
#     if len(pobj) < num:
#         return pobj
#     else:
#         return pobj[:num]
#     # if len(getp)<num:
#     #     ### Need to be added a search algo


def checkAdmin(r):
    getType = r.user.suffix.all()[0].type
    if getType == Suffix.seller or getType == Suffix.admin:
        return True
    else:
        return False


def index(r):
    datat = {}
    # allps = Post.objects.all().order_by('likes').reverse()
    # print(allps)
    # datat['posts'] = allps
    if check_log(r):
        datat['login'] = True
        datat['admin'] = checkAdmin(r)
        return render(r, "user/dashboard.html", datat)
    else:
        return render(r, "giftstore/index.html", datat)


def signup(r):
    # logged = check_log(r)
    # create logic for logged out user only
    if not check_log(r):
        validator_message = ['Your password length should be more than 8 charachters']
        return render(r, "giftstore/signupone.html", {"errors": validator_message})
    else:
        return redirect('home')


def SignupInit(r):  # User, PhoneNumber, Suffix
    if check_log(r):
        return redirect('home')
    if r.method == 'POST':
        try:
            Email = r.POST['Email']
            username = r.POST['username']
            Password = r.POST['password']
            RePassword = r.POST['repassword']
        except MultiValueDictKeyError:
            return render(r, "giftstore/signupone.html", {"erroro": "Please fill all the required fields"})
    alusers = User.objects.filter(email=Email)
    alusername = User.objects.filter(username=username)
    # phone = PhoneNumber.objects.filter(number=Phone)
    if len(alusers) == 1:
        return render(r, "giftstore/signupone.html", {"erroro": Email + " already registered try Sign in"})
    if len(alusername) == 1:
        return render(r, "giftstore/signupone.html", {"erroro": username + "already exits Please try again or Sign in"})
    if Password != RePassword:
        return render(r, "giftstore/signupone.html", {"re_password": "Please type correct password."})
    else:
        validator_message = []
        validators = [UserAttributeSimilarityValidator, MinimumLengthValidator, CommonPasswordValidator,
                      NumericPasswordValidator]
        hexpass = get_hex(Password + '10')
        new_user = User(email=Email, password=hexpass)
        for valid in validators:
            try:
                valid().validate(Password, new_user)
            except ValidationError as e:
                validator_message.append(list(e)[0])
        if len(validator_message) > 0:
            return render(r, "giftstore/signupone.html", {"errors": validator_message})
        else:
            newUser = User(username=username, email=Email, password=hexpass)
            newUser.save()
            # newP = PhoneNumber(person=newUser, number=int(Phone))
            # newP.save()
            newS = Suffix(person=newUser, type=Suffix.customer, content=10)
            newS.save()
            login(r, newUser)
            print("LOGGED in")
            em = Verify(person=newUser, name=False, OTP=0, times=datetime.datetime.now())
            em.save()
            # ph = Verify(person=newUser, name=False, OTP=0, times=datetime.datetime.now())
            # ph.save()
            return redirect("Email")


# ff
def signPhone(r):  # Not called
    if check_log(r) and not r.user.verify.get(name=True).status:
        obj = r.user.verify.get(name=True)
        otp = generateOTP()
        now = datetime.datetime.now()
        di = now - obj.times.replace(tzinfo=None)
        allow = 60 * 5  # need to add loop limits per user
        if obj.OTP == "0" or di.total_seconds() > allow:
            obj.loop += 1
            sendSMS(otp, r.user.username)
            obj.OTP = get_hex(otp)
            obj.message = ""
            obj.times = now
            obj.save()
        elif di.seconds < allow:
            print(obj.OTP)
        return render(r, "giftstore/verifyone.html", {"phone": str(r.user.username)[-3:], "error": obj.message})

    return redirect('home')


# ff
def recievePotp(r):  # The End
    if check_log(r) and r.method == "POST":
        obj = r.user.verify.get(name=True)
        now = datetime.datetime.now()
        di = now - obj.times.replace(tzinfo=None)
        allow = 60 * 5
        Otp = r.POST["otp"]
        if obj.OTP == get_hex(Otp) and di.total_seconds() < allow:
            obj.message = ""
            obj.status = True
            obj.OTP = "0"
            obj.save()
            return redirect("Email")
        elif di.total_seconds() > allow:
            obj.message = "Time Limit exceeded, New OTP has been sended"
            obj.save()
            return redirect("phone")
        else:
            obj.message = "Incorrect OTP"
            obj.save()
            return redirect("phone")
    return redirect("home")


def signEmail(r):
    if check_log(r) and not r.user.verify.get(name=False).status:
        obj = r.user.verify.get(name=False)
        otp = generateOTP()
        now = datetime.datetime.now()
        di = now - obj.times.replace(tzinfo=None)
        allow = 60 * 5  # 5 minutes
        if obj.OTP == "0" or di.total_seconds() > allow:
            obj.loop += 1
            sendMail(otp, r.user.email, 0, r)
            obj.OTP = get_hex(otp)
            obj.message = ""
            obj.times = now
            obj.save()
        elif di.seconds < allow:
            print(obj.OTP)
        # return redirect('home')
        return render(r, "giftstore/verifyemailone.html", {"email": r.user.email, "error": obj.message})
    return redirect('home')


def recieveEotp(r):
    if check_log(r) and r.method == "POST":
        obj = r.user.verify.get(name=False)
        now = datetime.datetime.now()
        di = now - obj.times.replace(tzinfo=None)
        allow = 60 * 5
        Otp = r.POST["otp"]
        if obj.OTP == get_hex(Otp) and di.total_seconds() < allow:
            obj.message = ""
            obj.status = True
            obj.OTP = "0"
            obj.save()
            print("Correct")
            return redirect("home")
        elif di.total_seconds() > allow:
            obj.message = "Time Limit exceeded, New OTP has been sended"
            obj.save()
            return redirect("Email")
        else:
            obj.message = "Incorrect OTP"
            obj.save()
            return redirect("Email")
    return redirect("home")


def otpresend(r):
    if check_log(r):
        obj = r.user.verify.get(name=False)
        if obj.status:
            return redirect('home')
        now = datetime.datetime.now()
        di = now - obj.times.replace(tzinfo=None)
        allow = 30 * obj.loop
        if di.total_seconds() > allow:
            obj.loop += 1
            otp = generateOTP()
            sendMail(otp, r.user.email, 0, r)  # 0 refers OTP
            obj.OTP = get_hex(otp)
            obj.message = "New OTP has been sended"
            obj.times = now
            obj.save()
            return redirect("Email")
        else:
            obj.message = "Please wait for " + str(obj.loop / 2) + " minutes"
            obj.save()
            return redirect("Email")
    return redirect("address")


# ff
# def save_signup(r):
#     if check_log(r):
#         return redirect('home')
#     if r.method == "POST":
#         FirstName = r.POST['first_name']
#         LastName = r.POST['last_name']
#         Email = r.POST['email_id']
#         address = r.POST['address']
#         Pincode = r.POST['pincode']
#         City = r.POST['city']
#         State = r.POST['state']
#         Phone = r.POST['phone_number']
#         Username = r.POST['username']
#         Password = r.POST['password']
#         RePassword = r.POST['re_password']
#     else:
#         return redirect('home')
#
#     validator_message = []
#     if Password == RePassword:
#         validators = [UserAttributeSimilarityValidator, MinimumLengthValidator, CommonPasswordValidator,
#                       NumericPasswordValidator]
#         hexpass = get_hex(Password + '10')
#         new_user = User(username=Username, email=Email, password=hexpass, first_name=FirstName, last_name=LastName)
#         for valid in validators:
#             try:
#                 valid().validate(Password, new_user)
#             except ValidationError as e:
#                 validator_message.append(list(e)[0])
#         if len(validator_message) > 0:
#             return render(r, "giftstore/signup.html", {"error": validator_message})
#         else:
#             get_user = User.objects.filter(username=Username)
#             if len(get_user) == 0 and Username != 'AnonymousUser':
#                 user_address = Address(person=new_user, name='address1', address=address, Pincode=Pincode, City=City,
#                                        State=State, prior=1)
#                 user_phone = PhoneNumber(person=new_user,
#                                          name='Phon1',
#                                          number=Phone)
#                 letPro = Suffix(person=new_user,
#                                 type=Suffix.customer)
#                 new_user.save()
#                 user_address.save()
#                 user_phone.save()
#                 letPro.save()
#                 login(r, new_user)
#             else:
#                 return render(r, "giftstore/signup.html", {"username": "Please use another Username, '"
#                                                                        + Username + "' Already taken"})
#     else:
#         return render(r, "giftstore/signup.html", {"re_password": "Please enter correct password"})
#
#     return redirect("phone")


def signin(r, message=''):
    if check_log(r):
        return redirect('home')

    return render(r, "giftstore/signin.html", {"error": message})


def inlog(r):
    if r.method == 'POST':
        Username = r.POST['username']
        Password = r.POST['password']
        c = False
        check_get = User.objects.filter(username=Username)
        if len(check_get) == 0:
            check_get = User.objects.filter(email=Username)
            c = True
        if not check_log(r) and len(check_get) == 1:
            if c:
                get_user = User.objects.get(email=Username)
            else:
                get_user = User.objects.get(username=Username)
            # getsuff = get_user.suffix.all()
            # if len(getsuff) == 0:
            #     return render(r, "giftstore/signin.html", {"error": "Incorrect Username or Password"})
            try:
                hexpass = get_hex(Password + str(get_user.suffix.all()[0].content))
            except IndexError:
                return render(r, "giftstore/signin.html", {"error": "Incorrect Username or Password"})
            if c:
                get_user = User.objects.filter(email=Username, password=hexpass)
            else:
                get_user = User.objects.filter(username=Username, password=hexpass)
            if len(get_user) < 1:
                return render(r, "giftstore/signin.html", {"error": "Incorrect Username or Password"})
            else:
                print('authenticated')
                login(r, get_user[0])
        else:
            return render(r, "giftstore/signin.html", {"error": "Incorrect Username or Password"})
    else:
        return redirect('home')
    return redirect('home')


def logout(r):
    lgout(r)
    return redirect('home')


def address(r, message={}):
    if check_log(r):
        return render(r, "giftstore/address.html", {'login': check_log(r), "admin": checkAdmin(r), "message": message})
    return redirect("home")


def displayaddress(r, addname, message=''):
    if check_log(r):
        gid = ''
        try:
            gid = r.GET['gid']
        except MultiValueDictKeyError:
            pass
        geta = r.user.Address.filter(name=addname)
        # print(addname)
        return render(r, "cart/ShowAddress.html",
                      {"every": Address.objects.all(), "prior": geta[0],
                       "error": message, 'gid': gid,
                       'r': r.user,
                       "login": check_log(r), "admin": checkAdmin(r), "purchase": False})


# def saveAddress(r, custom=False):
#     if check_log(r):
#         if r.method == "POST":
#             firstName = r.POST['first']
#             lastName = r.POST['last']
#             addName = r.POST['name']
#             pincode = r.POST['pincode']
#             addline = r.POST['address']
#             addline2 = r.POST['address2']
#             city = r.POST['city']
#             state = r.POST['state']
#             country = r.POST['country']
#             try:
#                 gid = r.POST['gid']
#             except MultiValueDictKeyError:
#                 gid = None
#             newadd = Address(person=r.user, name=addName, address=addline, address2=addline2, Pincode=pincode,
#                              City=city, State=state, Country=country, prior=True)
#
#             r.user.first_name = firstName
#             r.user.last_name = lastName
#             r.user.save()
#             geta = r.user.Address.filter(name=addName)
#             if len(r.user.Address.all()) == 20:
#                 if custom:
#                     return ['Failed', displayaddress(r, geta[0].name, "Maximum address limit exceeded.")]
#                 else:
#                     return displayaddress(r, geta[0].name, "Maximum address limit exceeded.")
#             # print(geta[0], '1' * 10)
#             if geta:
#                 gr = Group.objects.filter(address=geta[0])
#                 for g in gr:
#                     for p in g.products.all():
#                         if p.shipped and not p.delivered and \
#                                 newadd.address + newadd.address2 + str(newadd.Pincode) != geta[0].address + geta[
#                             0].address2 + str(geta[0].Pincode):
#                             # print(geta, 'i' * 20)
#                             if custom:
#                                 return ["Failed", displayaddress(r, geta[0].name,
#                                                                  "Can't update Address after the product shipped and "
#                                                                  "before delievered")]
#                             return displayaddress(r, geta[0].name,
#                                                   "Can't update Address after the product shipped and before "
#                                                   "delievered")
#                 newadd = geta[0]
#                 newadd.address = addline
#                 newadd.address2 = addline2
#                 newadd.Pincode = pincode
#                 newadd.City = city
#                 newadd.State = state
#                 newadd.Country = country
#                 newadd.prior = True
#             else:
#                 newadd = Address(person=r.user, name=addName, address=addline, address2=addline2, Pincode=pincode,
#                                  City=city, State=state, Country=country, prior=True)
#             if gid:
#                 getgp = Group.objects.get(id=gid)
#                 for p in getgp.products.all():
#                     if p.shipped and not p.delivered and newadd.address + newadd.address2 + str(newadd.Pincode) != geta[
#                         0].address + geta[0].address2 + str(geta[0].Pincode):
#                         if custom:
#                             return ["Failed", displayaddress(r, geta[0].name,
#                                                              "Can't update Address after the product shipped and "
#                                                              "before delievered")]
#                         return displayaddress(r, geta[0].name,
#                                               "Can't update Address after the product shipped and before delievered")
#                 getgp.address = newadd
#                 getgp.save()
#
#             alladdress = r.user.Address.all()
#             for a in alladdress:
#                 a.prior = False
#                 a.save()
#             newadd.prior = True
#             newadd.save()
#             if custom:
#                 return ["Success"]
#
#     return redirect("home")


# def search(r):
#     if r.method == "GET":
#         text = r.GET['sbar']
#         getC = CatData.objects.filter(Q(Name__icontains=text))
#         allp = []
#         if getC:
#             results = Category.objects.filter(type__in=getC).values("product")
#             for i in results:
#                 getp = Product.objects.get(id=i['product'])
#                 if not getp.ShowOUTproduct and getp.instock == 0:
#                     pass
#                 else:
#                     allp.append(getp)
#         for t in text.split():
#             results = Product.objects.filter(
#                 Q(Name__icontains=t) | Q(Description__icontains=t))
#             for i in results:
#                 getp = i
#                 clearbug(getp.Name)
#                 if not getp.ShowOUTproduct and getp.instock == 0:
#                     pass
#                 elif getp not in allp:
#                     allp.append(getp)
#
#     return render(r, 'giftstore/search.html', {"products": allp, "Image": list(allp), "url": getURL(r, ""),
#                                                "login": check_log(r), "text": text})


# def bestseller(r):
#     BestSellers = 30
#     productSell = bestSeller(BestSellers)
#     return render(r, 'giftstore/search.html', {"products": productSell, "Image": list(productSell) + [],
#                                                "url": getURL(r, "", ""), "login": check_log(r), "text": "Best Seller"})


# def newArrival(r):
#     latestNum = 30
#     productSell = latest(latestNum)
#     return render(r, 'giftstore/search.html', {"products": productSell, "Image": list(productSell) + [],
#                                                "url": getURL(r, ""), "login": check_log(r), "text": "New Arrivals"})


def contact(r, message=''):
    context = {
        "captcha": FormWithCaptcha,
        "message": message,
        "login": check_log(r),
    }
    if check_log(r):
        if checkAdmin(r):
            context['admin'] = True
    return render(r, 'giftstore/contactUS.html', context)


def contactresponse(r):
    get_recaptcha = r.POST.get("g-recaptcha-response")
    if get_recaptcha and r.method == "POST":
        Name = r.POST['firstname']
        Email = r.POST['email']
        message = r.POST['message']
        if check_log(r):
            if r.user.email != Email:
                mes = "You cannot enter another Email ID from your account"
                return contact(r, mes)
        else:
            getcs = User.objects.filter(email=Email)
            if getcs:
                mes = "(" + Email + ") Email ID is registred please login or use another email ID"
                return contact(r, mes)
        if len(ContactUs.objects.filter(email=Email)) < 5:
            newc = ContactUs(person=None, email=Email, name=Name, message=message)
            newc.save()
            mes = "Your contact form has been submitted successfully"
        else:
            mes = "Your contact us submission limit expired please wait for our response."
    else:
        mes = "Please check reCAPTCHA"
    return contact(r, mes)


def forgot(r, message=''):
    if not check_log(r):
        return render(r, 'giftstore/forgot.html', {'error': message})
    return redirect('home')


def verify(r):
    if not check_log(r) and r.method == "POST":
        email = r.POST['email']
        allUser = User.objects.filter(email=email)
        if allUser:
            now = datetime.datetime.now()
            getU = allUser[0]
            obj = getU.verify.get(name=False)
            otp = get_hex(generateOTP() + getU.email)
            obj.OTP = get_hex(otp)
            obj.times = now
            obj.save()
            alink = getURL(r, '/makenew/', False, '')
            sendMail(alink + "?key=" + otp, getU.email, 1, r)  # 1 refers linked OTP
            return signin(r, "Verification Email sent please check your inbox.")
        else:
            return forgot(r, "Email ID not registered please Sign Up")
    return redirect('home')


def makenew(r):
    if not check_log(r):
        hashkey = r.GET['key']
        result = get_hex(hashkey)
        allvs = Verify.objects.filter(OTP=result)
        if len(allvs) == 1:
            vs = allvs[0]
            now = datetime.datetime.now()
            di = now - vs.times.replace(tzinfo=None)
            print(di.total_seconds())
            if di.total_seconds() < 60 * 60 * 24 * 2 and vs.OTP != "0" and vs.OTP == result:  # 2 Days
                return render(r, 'giftstore/makenew.html', {"email": vs.person.email, 'key': hashkey})
            else:
                return signin(r, "Time Limit expired please create new link")
        else:
            return redirect('home')


def makenewsubmit(r):
    if check_log(r):
        return redirect('home')
    if r.method == "POST":
        try:
            key = get_hex(r.POST['key'])
            Email = r.POST['email']
            Password = r.POST['newpassword']
            repeatPassword = r.POST['repeatpassword']
            if Password != repeatPassword:
                return render(r, "giftstore/makenew.html", {'email': Email, "key": key,
                                                            "error": "Please type correct password"})
        except MultiValueDictKeyError:
            return signin(r, "Something went wrong please try again.")
        getU = User.objects.filter(email=Email)
        allvs = Verify.objects.filter(OTP=key)
        print(getU, allvs)
        if len(allvs) == 1:
            vi = allvs[0]
            if len(getU) == 1 and Password == repeatPassword and vi.person == getU[0]:
                new_user = getU[0]
                validator_message = []
                validators = [UserAttributeSimilarityValidator, MinimumLengthValidator, CommonPasswordValidator,
                              NumericPasswordValidator]
                for valid in validators:
                    try:
                        valid().validate(Password, new_user)
                    except ValidationError as e:
                        validator_message.append(list(e)[0])
                if len(validator_message) > 0:
                    return render(r, "giftstore/makenew.html", {"errors": validator_message, "email": vi.person.email,
                                                                'key': key})
                else:
                    vi.OTP = '0'
                    vi.save()
                    hexpass = get_hex(Password + str(new_user.suffix.all()[0].content))
                    new_user.password = hexpass
                    new_user.save()
                    message = "Your password changes successfully"
                    return signin(r, message)
        return signin(r, "Something went wrong please try again")


def getPopst(r, name):
    p = Post.objects.filter(title=name)
    # dp = r.user.dp.all()
    img = ''
    # if dp:
    #     img = dp[0].url
    # else:
    pd = False
    if p:
        post = p[0]
        return render(r, "writer/post.html", {'p': post, 'img': img, 'has': pd, 'r': r.user})


def search(r):
    # if r.method == ['GET']:
    which = r.GET['sbar']
    allps = Post.objects.filter(Q(title__icontains=which) | Q(content__icontains=which))
    datat = {}
    datat['posts'] = allps
    if check_log(r):
        datat['login'] = True
        datat['admin'] = checkAdmin(r)
        return render(r, "user/dashboard.html", datat)
    else:
        return render(r, "giftstore/index.html", datat)

#     def search(r):
#         if r.method == "GET":
#             text = r.GET['sbar']
#             getC = CatData.objects.filter(Q(Name__icontains=text))
#             allp = []
#             if getC:
#                 results = Category.objects.filter(type__in=getC).values("product")
#                 for i in results:
#                     getp = Product.objects.get(id=i['product'])
#                     if not getp.ShowOUTproduct and getp.instock == 0:
#                         pass
#                     else:
#                         allp.append(getp)
#             for t in text.split():
#                 results = Product.objects.filter(
#                     Q(Name__icontains=t) | Q(Description__icontains=t))
#                 for i in results:
#                     getp = i
#                     clearbug(getp.Name)
#                     if not getp.ShowOUTproduct and getp.instock == 0:
#                         pass
#                     elif getp not in allp:
#                         allp.append(getp)
#
#         return render(r, 'giftstore/search.html', {"products": allp, "Image": list(allp), "url": getURL(r, ""),
#                                                    "login": check_log(r), "text": text})

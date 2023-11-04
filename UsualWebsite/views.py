from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.urls import reverse
from UsualWebsite.models import SportsProduct, userAuthenticate, userOrder 
from ecommerce.settings import BASE_DIR
import os
from django.contrib.sessions.models import Session
from PIL import Image
BASE_DIR=str(BASE_DIR)

def validate(username,password):
    try:
        authentication=userAuthenticate.objects.get(username=username,password=password)
    except:
        authentication=None
    t=False
    if authentication!=None:
        t=True
        
    return t

def checkLogin(login):
    if login == 'yes':
        return 1
    return 0
# Create your views here.
class session:
    username=""
    password=""
    product=[]
    login=False
    order=""
    location=""
    cost=0
    costlist=[]
    search_product=""
    loc=True
    reloa_state=True

    def homePage(request):
        prducts=SportsProduct.objects.all().values()
        names=[]
        cost=[]
        location=[]
        date=[]
        suppliername=[]
        lastdate=[]
        images=[]
        description=[]
        session.order=""
        if request.session['login'] is not None :
            session.login=True
            session.username = request.session['login']
            u=userAuthenticate.objects.get(username=session.username)
            lo = u.location
            session.location = lo
            session.loc = False
            request.session['location'] = lo
        else:
            session.login=False

        for i in prducts:
            names.append(i['name'])
            cost.append(i['cost'])
            location.append(i['location'])
            date.append(i['date'])
            lastdate.append(i['removedate'])
            suppliername.append(i['supplierName'])
            images.append(i['image'])
            description.append(i["description"])
        zipped=zip(names,cost,location,date,suppliername,lastdate,images,description)
        
        if "searchSubmit" in request.POST:
            session.reloa_state=False
            session.search_product+=request.POST['ToSearch']
            if session.search_product != "":
                return HttpResponseRedirect(reverse('searchPage'))
            return  HttpResponse("no item select")
        if "seller" in request.POST:
            return HttpResponseRedirect(reverse('seller'))
        if "login" in request.POST:
            username=request.POST['username']
            password=request.POST['password']
            v=validate(username,password)
            if v:
                session.username=username
                session.password=password
                session.login=True
                request.session['login'] = username
        if "logout" in request.POST:
            session.login=False
            request.session['login']=None
        if "register" in request.POST:
            return HttpResponseRedirect(reverse("Register"))
        if "user_loc" in request.POST:
            session.location=request.POST['location']
            session.loc=False
        prod=""
        details=[]
        for i in details:
            if i in request.POST:
                prod+=i
                break
        if set(names) & set(request.POST):
            session.order+=(list(set(names) & set(request.POST))[0])
            cos=SportsProduct.objects.filter(name=session.order).all().values()[0]['cost']
            session.cost+=SportsProduct.objects.filter(name=session.order).all().values()[0]['cost']
            session.costlist.append(int(SportsProduct.objects.filter(name=session.order).all().values()[0]['cost']))
            uo=userOrder.objects.filter(username=session.username).values()
            if session.username=="":
                return HttpResponse("not login, please login")
            if session.location=="":
                return HttpResponse("enter location please")
            if(len(uo)==0):
                userOrder(location=session.location, ordersActive=session.order, count=1, username=userAuthenticate.objects.get(username=session.username), cost=session.cost).save()
            else:
                orderz=""
                cnt=1
                for i in uo[0]["ordersActive"].split(","):
                    orderz+=str(i)+","
                    cnt+=1
                orderz+=session.order
                userOrder.objects.filter(username=userAuthenticate.objects.get(username=session.username)).update(count=cnt, ordersActive=orderz, location= session.location, cost= session.cost)
            session.order=""
        if prod in details:
            session.product=SportsProduct.objects.filter(name=prod)
            return HttpResponseRedirect(reverse("ProductPage"))
        return render(request,"HomePage.html",{"products":zipped,"login":session.login,"username":session.username,"loc":session.loc,"user_location":session.location})
    
    def searchPage(request):
        prducts=SportsProduct.objects.filter(name=session.search_product).all().values()
        names=[]
        cost=[]
        location=[]
        date=[]
        suppliername=[]
        lastdate=[]
        images=[]
        description=[]

        for i in prducts:
            names.append(i['name'])
            cost.append(i['cost'])
            location.append(i['location'])
            date.append(i['date'])
            lastdate.append(i['removedate'])
            suppliername.append(i['supplierName'])
            images.append(i['image'])
            description.append(i["description"])
        zipped=zip(names,cost,location,date,suppliername,lastdate,images,description)
        if 'productSubmit' in request.POST:
            return HttpResponseRedirect(reverse('showProduct'))
        if "searchSubmit" in request.POST:
            if not session.reloa_state:
                if session.search_product=="":
                    session.reloa_state=not session.reloa_state
                    return HttpResponse("entered empty")
            return HttpResponseRedirect(reverse('searchPage'))
        session.search_product=""
        if "login" in request.POST:
            username=request.POST['username']
            password=request.POST['password']
            v=validate(username,password)
            if v:
                session.username=username
                session.password=password
                session.login=True
        if "logout" in request.POST:
            session.login=False
        if "register" in request.POST:
            return HttpResponseRedirect(reverse("Register"))
        if "user_loc" in request.POST:
            session.location=request.POST['location']
            u=userAuthenticate.objects.get(username=session.username)
            u.location=session.location
            request.session['location'] = session.location
            session.loc=False
        if set(names) & set(request.POST):
            session.order+=list(set(names) & set(request.POST))[0]
            session.cost+=int(SportsProduct.objects.filter(name=session.order).all().values()[0]['cost'])
            session.costlist.append(int(SportsProduct.objects.filter(name=session.order).all().values()[0]['cost']))
            uo=userOrder.objects.filter(username=session.username).values()
            if session.username=="":
                return HttpResponse("not login, please login")
            if session.location=="":
                return HttpResponse("enter location please")
            if(len(uo)==0):
                userOrder(location=session.location, ordersActive=session.order, count=1, username=userAuthenticate.objects.get(username=session.username), cost=session.cost).save()
            else:
                orderz=""
                cnt=1
                for i in uo[0]["ordersActive"].split(","):
                    orderz+=str(i)+","
                    cnt+=1
                orderz+=session.order
                userOrder.objects.filter(username=userAuthenticate.objects.get(username=session.username)).update(count=cnt, ordersActive=orderz, location= session.location, cost= session.cost)
        if 'checkout' in request.POST:
            return HttpResponseRedirect(reverse('checkout'))
        return render(request,'search_Page.html',{"products":zipped,"username":session.username,"login":session.login,"loc":session.loc,"user_location":session.location})
    
    def checkout(request):
        if 'buy' in request.POST:
            return HttpResponse("yea")
        if "ToSearch" in request.POST:
            return HttpResponseRedirect(reverse('searchPage'))
        if "login" in request.POST:
            username=request.POST['username']
            password=request.POST['password']
            v=validate(username,password)
            if v:
                session.username=username
                session.password=password
                session.login=True
        if "searchSubmit" in request.POST:
            session.search_product+=request.POST['ToSearch']
            if session.search_product != "":
                return HttpResponseRedirect(reverse('searchPage'))
            return  HttpResponse("no item select")
        if "logout" in request.POST:
            session.login=False
        if "register" in request.POST:
            return HttpResponseRedirect(reverse("Register"))
        if "user_loc" in request.POST:
            session.location=request.POST['location']
            session.loc=False
        try:
            uo=userOrder.objects.only('ordersActive').get(username=session.username)
            totalc=userOrder.objects.filter(username=session.username)
        except:
            uo="nothing"
        if session.username=="":
                return HttpResponse("not login, please login")
        if session.location=="":
            return HttpResponse("enter location please")
        return render(request,"checkout.html",{"pro":[uo.ordersActive],"username":session.username,"login":session.login,"loc":session.loc,"user_location":session.location})
    
    def register(request):
        if "register" in request.POST:
            username=request.POST['username']
            password=request.POST['password']
            location=request.POST['location']
            phonenumber=request.POST['phonenumber']
            userAuthenticate(username=username,password=password,location=location,phonenumber=phonenumber).save()
            return HttpResponseRedirect(reverse('homePage'))
        return render(request,'register.html')
    
    def seller(request):
        if "register" in request.POST:
            name=request.POST['name']
            cost=request.POST['cost']
            location=request.POST['location']
            date=request.POST['date']
            removedate=request.POST['removedate']
            suppliername=request.POST['suppliername']
            description=request.POST['description']
            session.handle_uploaded_file(request.FILES['file'])
            SportsProduct(name=name,cost=cost,date=date,removedate=removedate,location=location,supplierName=suppliername,image=request.FILES['file'].name,description=description).save()
            return HttpResponseRedirect(reverse('homePage'))
        return render(request,'seller.html')


    

    def resize_image(original_image):
        image = Image.open(original_image).convert('RGB')
        new_size = (181,100)
        image.resize(new_size)
        os.remove(original_image)
        image.save(original_image)


    def handle_uploaded_file(f):
        with open(r"static\\" + f.name,'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        session.resize_image(BASE_DIR+"\\static\\"+f.name)
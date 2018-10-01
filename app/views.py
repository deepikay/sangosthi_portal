"""
Definition of views.
"""
from django.core.mail import send_mail


from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponseRedirect

from django.template import RequestContext
import datetime
from django.contrib.auth.decorators import login_required
import forms
from django.contrib.auth import authenticate, login ,logout
from django.shortcuts import render , redirect ,get_object_or_404
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from .models import *
from django.views.decorators.csrf import csrf_exempt

# RequestList
def RequestList(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    q=CustomUser.objects.filter(is_Valid=False)
    return render(request,'app/RequestList.html',{'list':q , })


def ReqSignUp(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/SignUpReq.html',
        {
            'title':'Home Page',
            'year':datetime.datetime.now().year,
        }
    )

@csrf_exempt
def signup_view2(request,template_name,type):
    if request.method=='POST':
        print("PPPPPPPPPPPPPPPPPPPPP")
        form=forms.SignUpForm(request.POST)
        if(form.is_valid()):
            q=form.save()
            q.SA=True
            q=form.save()
        else:
            print(form.errors)

        return HttpResponseRedirect("login")

    else:
        form=forms.SignUpForm()
        # ha = form.save(commit=False)
    context={
    'form':form,
    'kindofadmin' : 2,
    'type':type
    }

    return render(request,template_name,context)


def signup_view3(request,template_name,type):
    if request.method=='POST':
        print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        form=forms.SignUpForm(request.POST)
        if(form.is_valid()):
            q=form.save()
            q.UA=True
            q=form.save()
        else:
            print(form.errors)

        return HttpResponseRedirect("login")

    else:
        form=forms.SignUpForm()
        # ha = form.save(commit=False)
    context={
    'form':form,
        'kindofadmin' : 3,
            'type':type


    }

    return render(request,template_name,context)


@csrf_protect
def login_view(request,template_name,id=None):
    print(str(request.method))
    if request.method=='POST':
        print("SWALALALAL")
        form=forms.BootstrapAuthenticationForm(data=request.POST)
        print(form.is_valid())
        if(form.is_valid()):
            user=form.get_user()
            print(user.location)
            print("LOCATION!!!!!!!!!!!!!!!!!!!!!!")
            l=user.location
            print(l)
            print(str(l))
            login(request,user)
            #return render(request,"app/login.html",{'form':form})
            # if(!user.superuser & !user.superadmin & user.admin):
            #     return HttpResponseRedirect("/profiles/"+str(user.id),{'location':l})
            return HttpResponseRedirect("/profiles/"+str(user.id),{'location':l})

    else:
        form=forms.BootstrapAuthenticationForm()
    return render(request,template_name,{'form':form})

def def_view(request,template_name):
    if request.method=='POST':
        form=forms.NameForm(data=request.POST)
        return HttpResponseRedirect("login")

    else:
        form=forms.NameForm()
    return render(request,template_name,{'form':form})

        # Redirect to a success page.
from django.core.mail import send_mail
def sendmail(request,id):
    print("WOW")
    instance=get_object_or_404(CustomUser,id=id)
    assert isinstance(request, HttpRequest)
    message='Reply back with username and password'
    from_email='anushka.bhandari45@gmail.com'
    tolist=[instance.email]
    send_mail('Login Credentials',message,from_email,tolist,fail_silently=False)
    print("MAIL SENT")
    instance.mail_sent=True
    instance.save()
    return render(request,'app/Request.html',{'userprof':instance, })



def deleteuser(request,id):
    print("DELETED")
    instance=get_object_or_404(CustomUser,id=id)
    instance.delete()
    print(instance.id)
    q=CustomUser.objects.filter(is_Valid=False)
    l='Delhi'
    # url(r'^RequestList', app.views.RequestList, name='RequestList'),
    return HttpResponseRedirect("/RequestList",{'list':q})




def request(request,id):
    print("!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(id)
    main_id=request.user.id
    assert isinstance(request, HttpRequest)
    instance=get_object_or_404(CustomUser,id=id)
    print(instance.email)

    return render(request,'app/Request.html',{'userprof':instance, })

def dashboard(request,id=None):
    main_id=request.user.id
    assert isinstance(request, HttpRequest)
    instance=get_object_or_404(CustomUser,id=main_id)
    print(instance.id)
    q=CustomUser.objects.all()
    kindofadmin=0
    typeofadmin='user'
    if(instance.MA):
        kindofadmin=1
        typeofadmin='Main Admin'
    if(instance.SA):
        kindofadmin=2
        typeofadmin='Super Admin'
    if(instance.UA):
        kindofadmin=3
        typeofadmin='User Admin'
    if (int(id)-int(main_id)==0):
        return render(request,'app/dashboard.html',{'kindofadmin':kindofadmin,'list':q, 'typeofadmin':typeofadmin})
    else:
        return render(request,"app/index.html")
from app.models import Asha
from django.template import loader
from django.http import HttpResponse
def ashalist(request,id=None):
    """Renders the home page."""
    template=loader.get_template('app/AshaList.html')
    q=[]
    p=Asha.objects.all()
    k=[]
    for i in p:
        if i.location==request.user.location:
            q.append(i)
        else:
            k.append(i)
    context={
    'f':"profiles/"+ str(request.user.id)+"/",

    'Items': q,
    'Disable': k
    }
    return HttpResponse(template.render(context,request))


def cohortlist(request):
    """Renders the home page."""
    template=loader.get_template('app/CohortList.html')
    q=[]
    p=Cohort.objects.all()
    k=[]
    for i in p:
        if i.status==True:
            q.append(i)
        else:
            k.append(i)
    context={

    'Items': q,
    'Disable': k
    }
    return HttpResponse(template.render(context,request))

year_dropdown = []
for y in range(1980, (datetime.datetime.now().year + 10)):
	year_dropdown.append((y,y))

CHOICES=[]
import datetime
today = str(datetime.date.today())
ans=today.split("-")
datedate=ans[1]+"/"+ans[2]+"/"+ans[0]

CHOICES.append(('Basic Phone','Basic Phone'))
CHOICES.append(('Smart Phone','Smart Phone'))

@csrf_exempt
def ashaAdd(request):
    template_name='app/AshaAdd.html'
    print(str(request.method))
    if request.method=='POST':
        print("NO")
        form=forms.NameForm(request.POST,request.FILES)
        if(form.is_valid()):
            form.save()
        else:
            print(form.errors)

        return HttpResponseRedirect("login")

    else:
        form=forms.NameForm()
        form.fields['author'].empty_label=request.user
        form.fields['author'].widget.attrs['placeholder']=request.user
        #form.fields['LastUpdatedBy'].widget.attrs['placeholder']=datedate

        form.fields['PhoneType'].widget.choices=CHOICES
        form.fields['YearOfJoining'].widget.choices=year_dropdown
        form.fields['location'].widget.attrs['placeholder'] = request.user.location
    for i in year_dropdown:
        print(i)
    context={
    "year_dropdown":year_dropdown,
    'form':form
    }

    return render(request,template_name,context)

@csrf_exempt
def ContentCategoryAdd(request):
    template_name='app/AddContentCategories.html'
    if request.method=='POST':
        form=forms.ContentCategoryForm(request.POST,request.FILES)
        if(form.is_valid()):
            q=form.save()
        else:
            print(form.errors)

        return HttpResponseRedirect("login")

    else:
        form=forms.ContentCategoryForm()
    context={
    'form':form
    }

    return render(request,template_name,context)

def handle_uploaded_file(f):

    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
from django.conf import settings
import os
from django.core.files.storage import default_storage
@csrf_exempt
def AudioFileAdd(request):
    template_name='app/AddAudioFiles.html'
    if request.method=='POST':
        form=forms.AudioFileForm(request.POST,request.FILES)
        if(form.is_valid()):
    #return default_storage.path(path)
            q=form.save()
        else:
            print(form.errors)

        return HttpResponseRedirect("login")

    else:
        form=forms.AudioFileForm()
    context={
    'form':form
    }

    return render(request,template_name,context)






@csrf_exempt
def ContentAdd(request):
    template_name='app/AddContent.html'
    if request.method=='POST':
        form=forms.ContentForm(request.POST,request.FILES)
        if(form.is_valid()):
    #return default_storage.path(path)
            q=form.save()
        else:
            print(form.errors)

        return HttpResponseRedirect("login")

    else:
        form=forms.ContentForm()
    context={
    'form':form
    }

    return render(request,template_name,context)









@csrf_exempt
def CohortAdd(request):
    template_name='app/CohortAdd.html'
    if request.method=='POST':
        form=forms.CohortForm(request.POST)
        if(form.is_valid()):
            q=form.save()
            flag=True
            for i in q.listeners.all():
                if(i.location!=request.user.location):
                    flag=False
            q.status=flag
            q.save()
        else:
            print(form.errors)

        return HttpResponseRedirect("login")

    else:
        form=forms.CohortForm()
    context={
    'form':form
    }

    return render(request,template_name,context)

@csrf_exempt
def ExpertAdd(request):
    template_name='app/ExpertAdd.html'
    if request.method=='POST':
        form=forms.ExpertForm(request.POST)
        if(form.is_valid()):

            q=form.save()
        else:
            print(form.errors)

        return HttpResponseRedirect("login")

    else:
        form=forms.ExpertForm()
    context={
    'form':form
    }

    return render(request,template_name,context)



def handle_uploaded_file(f):
    with open(f, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
import pandas as pd

def statistics(request):
    df = pd.read_csv('/home/anushka/Desktop/attendance.csv')
    saved_column = df.Phone
    x=saved_column.tolist()
    y=df.avg.tolist()
    df1 = pd.read_csv('/home/anushka/Desktop/BTP/MAIN/Sangoshthi/Sangoshthi/Sangoshthi_Project/app/speak_count_total.csv')
    saved_column1 = df1.Phone
    x1=saved_column1.tolist()
    y1=df1.avg.tolist()

    return render(request, 'app/statistics.html',{'x':x,'y':y,'x1':x1,'y1':y1})

def load_cities(request):
    category_id = request.GET.get('category')
    contents = Content.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'app/content_dropdown_list_options.html', {'contents': contents})
def load_questions(request):
    source = request.GET.get('NoOfQuestions')
    return render(request, 'app/load_questions.html',{'source':source})

@csrf_exempt
def ShowAdd(request):
    template_name='app/AddShow.html'
    if request.method=='POST':
        form=forms.ShowForm(request.POST,request.FILES)
        if(form.is_valid()):
            q=form.save()
        else:
            print(form.errors)

        return HttpResponseRedirect("login")

    else:
        form=forms.ShowForm()
    context={
    'form':form
    }

    return render(request,template_name,context)







@csrf_exempt
def TextMessageAdd(request):
    template_name='app/AddTextMessage.html'
    if request.method=='POST':
        form=forms.TextMessageForm(request.POST,request.FILES)
        if(form.is_valid()):
            q=form.save()
        else:
            print(form.errors)

        return HttpResponseRedirect("login")

    else:
        form=forms.TextMessageForm()
    context={
    'form':form
    }

    return render(request,template_name,context)






@csrf_exempt
def SendAudioTrailerAdd(request):
    template_name='app/AddSendAudioTrailer.html'
    if request.method=='POST':
        form=forms.SendAudioTrailerForm(request.POST,request.FILES)
        if(form.is_valid()):
            q=form.save()
        else:
            print(form.errors)

        return HttpResponseRedirect("login")

    else:
        form=forms.SendAudioTrailerForm()
    context={
    'form':form
    }

    return render(request,template_name,context)






@csrf_exempt
def ShowFeedbackAdd(request):
    template_name='app/AddShowFeedBack.html'
    if request.method=='POST':
        form=forms.ShowFeedbackForm(request.POST,request.FILES)
        if(form.is_valid()):
            q=form.save()
        else:
            print(form.errors)

        return HttpResponseRedirect("login")

    else:
        form=forms.ShowFeedbackForm()
    context={
    'form':form
    }

    return render(request,template_name,context)








@csrf_exempt
def ShowRecordingAdd(request):
    template_name='app/AddShowRecording.html'
    if request.method=='POST':
        form=forms.ShowRecordingForm(request.POST,request.FILES)
        if(form.is_valid()):
            q=form.save()
        else:
            print(form.errors)

        return HttpResponseRedirect("login")

    else:
        form=forms.ShowRecordingForm()
    context={
    'form':form
    }

    return render(request,template_name,context)

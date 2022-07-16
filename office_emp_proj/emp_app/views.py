from django.conf import settings
from django.conf.urls import url
from django.contrib import auth
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.views.generic import TemplateView
from .models import Employee, Role, Department, Feedback_Model, Employee_image,Registration
from _datetime import datetime
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Q
from .forms import Feedbackform, imageForm,registrationform
from django.contrib.auth import logout
from django.shortcuts import redirect
import logging
from django.db.models.aggregates import Avg,Max,Min,Count,Sum

# Create your views here.
logging.basicConfig(filename="emp_log.log",filemode='w', format='%(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)


@login_required()
def index(request):
    logging.info('Deepali logged in')
    return render(request, 'index.html')


@login_required()
def all_emp(request):
    emps = Employee.objects.all()
    context = {'emps': emps}
    return render(request, 'all_emp.html', context)

@login_required()
def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dept = request.POST['dept']
        print(dept)
        dept_object = Department.objects.get(name=dept)
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        role = request.POST['role']
        print(role)
        role_object=Role.objects.get(name=role)
        phone = int(request.POST['phone'])

        new_emp = Employee(first_name=first_name, last_name=last_name, dept=dept_object, salary=salary, bonus=bonus,
                           role=role_object, phone=phone, hiring_date=datetime.now())
        new_emp.save()
        emp_image = request.FILES.get('img')
        emp_image_object = Employee_image(emp=new_emp, img=emp_image)
        emp_image_object.save()

        return all_emp(request)

    elif request.method == 'GET':
        form = imageForm()
        department_names = Department.objects.all().values_list('name', flat=True)
        role_names=Role.objects.all().values_list('name',flat=True)

        context={
            'department_names': department_names,
            'role_names':role_names,
            'form':form
        }
        #print(department_names)
        return render(request, 'add_emp.html',context)
    else:
        return HttpResponse("Exception occurred! Employee not added")


def delete_emp(request, emp_id=0):
    if emp_id:
        try:

            employee_to_be_deleted = Employee.objects.get(id=emp_id)
            employee_to_be_deleted.delete()
            return all_emp(request)
        except:
            return HttpResponse("Enter valid Employee ID")
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'delete_emp.html', context)

@login_required()
def filter_emp(request):
    if request.method == 'POST':

        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()
        #unique_first_names = emps.values_list('first_name',flat=True).distinct()
        #print("Distinct first names:" + str(unique_first_names.count()))
        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))

        if dept:
            emps = emps.filter(dept_name=dept)
        if role:
            emps = emps.filter(role_name=role)

        context = {
            'emps': emps
        }
        return render(request, 'all_emp.html', context)
    elif request.method == 'GET':
        if request.GET.get('salary', None) is not None:
            salary = request.GET.get('salary')
            emps = Employee.objects.all()
            emps = emps.filter(salary=salary)
            context = {
                'emps': emps
            }
            return render(request, 'all_emp.html', context)
        else:
            return render(request, 'filter_emp.html')
    else:
        return HttpResponse("Exception occurred!")


def update_emp(request, emp_id=0):
    if request.method == 'GET':
        print("Got Get request")
        if emp_id:
            try:
                employee_to_be_updated = Employee.objects.get(id=emp_id)
                department_names = Department.objects.all().values_list('name', flat=True)
                role_names=Role.objects.all().values_list('name',flat=True)
                employee_image_obj = Employee_image.objects.get(emp=employee_to_be_updated)

                context = {
                    'employee_to_be_updated': employee_to_be_updated,
                    'department_names': department_names,
                    'role_names':role_names,
                    'employee_image_obj' : employee_image_obj
                }
                return render(request, 'update_emp.html', context)
            except:
                pass
    elif request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dept = request.POST['dept']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        role = request.POST['role']
        phone = int(request.POST['phone']);
        print("Post request values are %s %s %s %s %s" %(emp_id, first_name, last_name, dept, salary));
        dept_object = Department.objects.get(name=dept)
        role_object=Role.objects.get(name=role)
        employee_to_be_updated = Employee.objects.get(id=emp_id)
        employee_to_be_updated.first_name = first_name
        employee_to_be_updated.last_name = last_name
        employee_to_be_updated.dept=dept_object
        employee_to_be_updated.salary = salary
        employee_to_be_updated.bonus = bonus
        employee_to_be_updated.role=role_object
        employee_to_be_updated.phone = phone
        employee_to_be_updated.save(update_fields=["first_name", "last_name", "dept", "salary", "bonus", "role","phone"])
        return HttpResponseRedirect(redirect_to='/all_emp')


        ## Method 2
        # Employee.objects.filter(id=emp_id).update(first_name=first_name, last_name=last_name,
        #                                           dept=dept_object, salary=salary, bonus=bonus, phone=phone)
        # return all_emp(request)


def feedback(request):

    if request.method=='POST':
        form=Feedbackform(request.POST)
        print(form)
        if form.is_valid():
            print("Form is valid")
            form.save()

            return HttpResponse('<h3> Thanks for visits </h3>')
            return redirect('/all_emp')
        else:
            print("Hey-yyy the form is invalid")
            return HttpResponse('<h3> Invalid Form retry </h3>')

    else:
        # f=Feedbackform.objects.all.values()
        # print(f)
        feedbackform = Feedbackform()
        md={'form':feedbackform}
        return render(request,'feedback.html',context=md)


def logout_view(request):
    logout(request)
    return redirect('emps/login')


def employee_image_view(request):
    if request.method == 'POST':
        form = imageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = imageForm()
    return render(request, 'img_upload.html', {'form': form})


def success(request):
    return HttpResponseRedirect(redirect_to='gallery/')

def gallery(request,emp_id=0):
    if request.method == 'GET':
       if emp_id:
            employee_to_be_updated = Employee.objects.get(id=emp_id)
            department_names = Department.objects.all().values_list('name', flat=True)
            role_names = Role.objects.all().values_list('name', flat=True)
            employee_image_obj = Employee_image.objects.get(emp=employee_to_be_updated)
            context = {
                'employee_to_be_updated': employee_to_be_updated,
                'department_names': department_names,
                'role_names': role_names,
                'employee_image_obj': employee_image_obj
            }
            return render(request, 'gallery.html', context)
       else:
           return HttpResponse("failed")


def register(request):
    if request.method=='POST':
        form=registrationform(request.POST)
        if form.is_valid():
            print("Form is valid")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('Email')
            password  = form.cleaned_data.get('password')
            renter_password = form.cleaned_data.get('renter_password')
            print(first_name, last_name, email, username,password,renter_password)
            if password==renter_password:
                if Registration.objects.filter(username=username).exists():
                    print("Username Taken")
                elif Registration.objects.filter(Email=email).exists():
                    print("Email Taken")
                else:
                    user = User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
                    #form.save()
                    user.save();
                    print("user created")
                    return HttpResponseRedirect(redirect_to='/emps/login')
    else:
        form=registrationform()
        md = {'form': registrationform}
        return render(request,'register.html',context=md)


def statistics(request):
    avg=  Employee.objects.all().aggregate(Avg('salary'))
    min = Employee.objects.all().aggregate(Min('salary'))
    max = Employee.objects.all().aggregate(Max('salary'))
    sum = Employee.objects.all().aggregate(Sum('salary'))
    count = Employee.objects.all().aggregate(Count('salary'))

    md={'avg':avg,'min':min,'max':max,'sum':sum,'count':count}
    return render(request,'statistics.html', context=md)

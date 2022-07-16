from django.db import models

# Create your models here.


class Department(models.Model):
    name=models.CharField(max_length=50,null=False)
    location=models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Role(models.Model):
    name=models.CharField(max_length=50,null=False)

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name=models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dept = models.ForeignKey(Department,on_delete=models.CASCADE)
    salary=models.IntegerField(default=0)
    bonus=models.IntegerField(default=0)
    role=models.ForeignKey(Role,on_delete=models.CASCADE)
    phone=models.IntegerField()
    hiring_date=models.DateField()

    def __str__(self):
        return "%s %s %s %s %s %s" %(self.first_name,self.last_name,self.dept, self.salary, self.role, self.phone)


class Feedback_Model(models.Model):
    name = models.CharField(max_length=25, primary_key=True)
    Address = models.CharField(max_length=22)
    email = models.EmailField()
    feedback = models.TextField()

    def __str__(self):
        return "%s %d %s %s" %(self.name,self.Address,self.email,self.feedback)


class Employee_image(models.Model):

    emp=models.ForeignKey(Employee, on_delete=models.CASCADE,null=True, default=None)
    img = models.ImageField(upload_to='images/')

    def __str__(self):
        return " %s" % (self.img)


class Registration(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username=models.CharField(max_length=20)
    Email=models.EmailField()
    password=models.CharField(max_length=20)
    renter_password=models.CharField(max_length=20)


    def __str__(self):
        return "%s %s %s %s %s %s" % (self.first_name, self.last_name,self.username,self.Email,self.password,self.renter_password)


from django.db import models
from django.contrib.auth.models import User


 #Create your models here.
class Transaction(models.Model):
    TRANSACTION_TYPE=[
        ('Income','Income'),
        ('Expense','Expense')
       ]
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=255)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    transaction_type=models.CharField(max_length=10,choices=TRANSACTION_TYPE)
    date=models.DateField()
    category=models.CharField(max_length=255)

    def __str__(self):
        return self.title
    
#Create your models here.
class Goal(models.Model):
   
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    target_amount=models.DecimalField(max_digits=10,decimal_places=2)
    current_amount=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    deadline=models.DateField()
    def __str__(self):
        return self.name

from django.shortcuts import render,redirect
from django.views import View
from finance.forms import RegisterForm,TransactionForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from finance.models import Transaction



# Create your views here.
class RegisterView(View):
    def get(self,request,*args,**kwargs):
        form=RegisterForm()
        return render(request,'finance/register.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('dashboard')

class DashboardView(LoginRequiredMixin,View):
     def get(self,request,*args,**kwargs):
        return render(request,'finance/dashboard.html')

class TransactionCreateView(View):
     def get(self,request,*args,**kwargs):
        form=TransactionForm()
        return render(request,'finance/transaction_form.html',{'form':form})
     def post(self,request,*args,**kwargs):
        form=TransactionForm(request.POST)
        if form.is_valid():
            transaction=form.save(commit=False)
            transaction.user=request.user
            transaction.save()
            return redirect('dashboard')
        return render(request,'finance/transaction_form.html',{'form':form})
     
class TransactionListView(LoginRequiredMixin,View):
   def get(self,request,*args,**kwargs):
        transaction=Transaction.objects.all() 
     
        return render(request,'finance/transaction_form.html',{'transaction':Transaction})
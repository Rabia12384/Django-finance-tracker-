from django.shortcuts import render,redirect
from django.views import View
from finance import models
from finance.forms import RegisterForm,TransactionForm,GoalForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from finance.models import Transaction,Goal
from django.db import models



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
        transactions=Transaction.objects.filter(user=request.user)
        goals=Goal.objects.filter(user=request.user)
        #calculating total income and expense
        total_income=transactions.filter(user=request.user,transaction_type="Income").aggregate(models.Sum('amount'))['amount__sum']or 0
        total_expense=transactions.filter(user=request.user,transaction_type='Expense').aggregate(models.Sum('amount'))['amount__sum'] or 0
        net_savings=total_income-total_expense
        remaining_savings = max(net_savings, 0)

        goal_progress=[]
        for goal in goals:
            if remaining_savings >= goal.target_amount:
                goal_progress.append({'goal': goal, 'progress': 100})
                remaining_savings -= goal.target_amount
            elif remaining_savings > 0:
                progress = (remaining_savings / goal.target_amount) * 100
                goal_progress.append({'goal': goal, 'progress': progress})
                remaining_savings = 0
            else:
                goal_progress.append({'goal': goal, 'progress': 0})
        context={
            'transactions':transactions,
            'goals': goals,
            'total_income':total_income,
            'total_expense':total_expense,
            'net_savings':net_savings,
            'goal_progress':goal_progress
              }
        return render(request,'finance/dashboard.html',context)

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
        transactions=Transaction.objects.all() 
        return render(request,'finance/transaction_list.html',{'transactions':transactions})
   
class GoalCreateView(LoginRequiredMixin,View):
     def get(self,request,*args,**kwargs):
        form=GoalForm()
        return render(request,'finance/goal_form.html',{'form':form})
     def post(self,request,*args,**kwargs):
        form=GoalForm(request.POST)
        if form.is_valid():
            goal=form.save(commit=False)
            goal.user=request.user
            goal.save()
            return redirect('dashboard')
        return render(request,'finance/goal_form.html',{'form':form})
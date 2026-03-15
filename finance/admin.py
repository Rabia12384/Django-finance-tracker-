from django.contrib import admin
from finance.models import  Transaction, Goal

# Register your models here.
@admin.register( Transaction)
class  TransactionAdmin(admin.ModelAdmin):
    list_display=['title','amount','transaction_type','date','category']

@admin.register( Goal)
class  GoalAdmin(admin.ModelAdmin):
    list_display=['name','target_amount','current_amount','deadline']

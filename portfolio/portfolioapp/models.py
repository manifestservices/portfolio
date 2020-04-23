# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models import Sum
# Create your models here.

class Notes(models.Model):
    
    to_do = models.TextField(default='')
    assignee=models.ForeignKey(User, null=True, blank=True,on_delete=models.DO_NOTHING)
    deadline=models.DateTimeField(null=True)
    is_done=models.BooleanField(default=False)
    created_datetime=models.DateTimeField(null=True)
    created_by=models.CharField(max_length=100, default=None,null=True, blank=True)
    modified_datetime=models.DateTimeField(auto_now_add=True, blank=True)
    modified_by=models.CharField(max_length=100, default=None,null=True, blank=True)
    
    def __str__(self):
        return str(self.to_do)

class Stocks(models.Model):

    scrip=models.CharField(max_length=100, default=None,null=True, blank=True)
    quantity=models.PositiveSmallIntegerField(default=0)
    price=models.DecimalField(default=0,max_digits=5,decimal_places=2)
    total=models.DecimalField(default=0,max_digits=10,decimal_places=2)
    
class Ledger(models.Model):
    
    scrip=models.CharField(max_length=100, default=None,null=True, blank=True)
    action=models.CharField(max_length=100, default=None,null=True, blank=True,choices=[('BUY', 'BUY'),
                                                                                         ('SELL', 'SELL'), 
                                                                                         ])
    quantity=models.PositiveSmallIntegerField(default=0)
    price=models.PositiveIntegerField(default=0)
    
    
class NotesManager(object):
    
    def create_note(self,to_do,username):
        
        Notes.objects.create(to_do=to_do,created_by=username)
        
    def delete_note(self,note_id):
        Notes.objects.filter(id=note_id).delete()
        
    def fetch_all_notes(self):
        
        return Notes.objects.all()
    
    def update_note_details(self,note_id,to_do):
        
        Notes.objects.filter(id=note_id).update(to_do=to_do)


class StockManager():
    
    def get_all_stocks(self):
        
        return Stocks.objects.all()
    
    def get_scrip_data(self,scrip):
        
        return Stocks.objects.filter(scrip=scrip).last()
    
    def get_overall_total(self):
        
        return  Stocks.objects.aggregate(Sum('total')).get('total__sum')
    
    def update_stock(self,data):
        
        update_stock_obj=Stocks.objects.filter(scrip=data['scrip']).last()
        update_stock_obj.quantity=data['quantity']
        update_stock_obj.price=data['price']
        update_stock_obj.total=data['total']
        update_stock_obj.save()
    
    def add_new_stock(self,data):
        new_stock_obj=Stocks(scrip=data['scrip'],
                            quantity=data['quantity'],
                            price=data['price'],
                            total=data['total'],
                            )
        new_stock_obj.save()
        
        
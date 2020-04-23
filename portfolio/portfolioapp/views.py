# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import View
from django.shortcuts import render,redirect,HttpResponse,reverse
from django.http import HttpResponseRedirect
from portfolio.views import BaseView
from portfolioapp.portfolio_handler import PortfolioHandler
# Create your views here.
import logging,datetime
log=logging.getLogger(__name__)
from decimal import Decimal
    

class PortfolioHomeView(BaseView):

    def get(self, request,*args,**kwargs):
        """ 
            
        """
        self.context_dict['existing_stocks']=PortfolioHandler().fetch_all_stocks()
        self.context_dict['overall_total']=PortfolioHandler().fetch_overall_total()
        self.context_dict['overall_total']=PortfolioHandler().fetch_overall_total()
        return render(request,'portfolio_home.html',self.context_dict)


class PortfolioClientsView(BaseView):

    def get(self, request,*args,**kwargs):
        """ 
            
        """
        return render(request,'portfolio_home.html',self.context_dict)


class PortfolioAdjustStocksView(BaseView):

    def get(self, request,*args,**kwargs):
        """ 
            
        """
        self.context_dict['existing_stocks']=PortfolioHandler().fetch_all_stocks()
        self.context_dict['overall_total']=PortfolioHandler().fetch_overall_total()
        return render(request,'portfolio_adjust_stocks.html',self.context_dict)
    
    
    def post(self, request,*args,**kwargs):
        data={}
        data['scrip']=request.POST.get('scrip')
        data['quantity']=Decimal(request.POST.get('quantity'))
        data['price']=Decimal(request.POST.get('price'))
        PortfolioHandler().add_stock(data)
        return HttpResponseRedirect(reverse('portfolio_adjust_stocks'))

class NewInvestmentCalucationView(BaseView): 

    def get(self, request,*args,**kwargs):
        """ 
            
        """
        self.context_dict['new_investment_value']=Decimal(request.GET.get('value'))/100
        self.context_dict['existing_stocks']=PortfolioHandler().fetch_all_stocks()
        self.context_dict['overall_total']=PortfolioHandler().fetch_overall_total()
        return render(request,'portfolio_new_investment_split_table.html',self.context_dict)
class PortfolioNotesView(BaseView):

    def get(self, request,*args,**kwargs):
        """ 
            
        """
        self.context_dict['notes']=PortfolioHandler().get_all_notes()
        return render(request,'portfolio_notes.html',self.context_dict)

    def post(self, request,*args,**kwargs):
        action=request.GET.get('action')
        if action=='create':
            to_do=request.POST.get('to_do')
            username=request.POST.get('input_user')
            PortfolioHandler().create_note(to_do,username)
            return redirect(reverse('portfolio_notes'))
        if action =='delete':
            note_id=request.POST.get('note_id')
            PortfolioHandler().delete_note(note_id)
        if action =='update':
            note_id=request.POST.get('note_id')
            to_do=request.POST.get('to_do')
            PortfolioHandler().update_note(note_id, to_do)
            
        return HttpResponse('True')



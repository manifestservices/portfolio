from django.shortcuts import render,reverse
import logging,os
from portfolioapp.models import NotesManager,StockManager
log=logging.getLogger(__name__)

class PortfolioHandler(object):
    
    def __init__(self):
        pass
        
    def get_all_notes(self):
        
        return NotesManager().fetch_all_notes()
    
    def create_note(self,to_do,username):
        
        return NotesManager().create_note(to_do, username)
    
    def delete_note(self,note_id):
        
        return NotesManager().delete_note(note_id)
    
    def update_note(self,note_id,to_do):
        
        return NotesManager().update_note_details(note_id,to_do)
    
    def fetch_all_stocks(self):
        
        return StockManager().get_all_stocks()
    
    def fetch_overall_total(self):
        
        return StockManager().get_overall_total()
    
    def update_existing_stock(self,data):
        scrip_data_obj=StockManager().get_scrip_data(data['scrip'])
        current_quantity=scrip_data_obj.quantity
        new_quantity=current_quantity+data['quantity']
        current_total=scrip_data_obj.total
        addition= data['quantity']*data['price']
        new_total=current_total+addition
        new_price=new_total/new_quantity
        data['total']=new_total
        data['price']=new_price
        data['quantity']=new_quantity
        StockManager().update_stock(data)
        
    def add_stock(self,data):
        
        scrip_data_obj=StockManager().get_scrip_data(data['scrip'])
        if scrip_data_obj:
            self.update_existing_stock(data)
        else:
            data['total']=data['quantity']*data['price']
            StockManager().add_new_stock(data)
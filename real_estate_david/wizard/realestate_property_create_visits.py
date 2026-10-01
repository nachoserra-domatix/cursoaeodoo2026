from odoo import models, fields, api, _
from datetime import timedelta


class RealEstatePropertyCreateVisits(models.TransientModel):
   _name = 'realestate.property.create.visits'
   _description = 'Create visits from property using a wizard'
     
   start_date = fields.Date('start_date', required=True)
   
   end_date = fields.Date('end_date', required=True)
     
   
   def action_create_visits(self):
      vals_list = []
      current_date = self.start_date
      property = self.env['realestate.property'].browse(self.env.context.get('active_id'))
      
      while current_date <= self.end_date:
         vals_list.append({
            'property_id':property.id,
            'user_id':property.user_id.id,
            'date': current_date,
            'state':'scheduled',
         })
         current_date +=timedelta(days=1)
      visits = self.env['realestate.visit'].create(vals_list)
      
      return{
         'type':'ir.actions.act_window',
         'name':'Scheduled visits',
         'res_model':'realestate.visit',
         'view_mode':'list,form',
         'domain':[('id','in',visits.ids)],
      }
      
      
from odoo import models, fields


class RealEstateVisitChangeState(models.TransientModel):
   _name = 'realestate.visit.change.state'
   _description = 'Change visit states using a wizard'
    
   state = fields.Selection([
         ('draft', 'Draft'),
         ('scheduled', 'Scheduled'),
         ('done', 'Done'),
         ('canceled', 'Canceled')
   ],string= 'State' )
   
   
   def action_change_visit_state(self):
      active_ids = self.env.context.get('active_ids') or []
      visits = self.env['realestate.visit'].browse(active_ids)
      visits.write({'state': self.state})
      
      return{
         'type':'ir.actions.act_window',
         'name': 'Visits',
         'res_model':'realestate.visit',
         'view_mode':'list,form',
         'domain':[('id','in',active_ids)],
      }
      
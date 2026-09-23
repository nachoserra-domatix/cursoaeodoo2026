from odoo import models, fields, api


class RealEstateContract(models.Model):
   _name = 'realestate.contract'
   _description = 'Contract'
   
   name = fields.Char(string='Name')
   
   contract_type = fields.Selection([
      ('sale', 'Sale'),
      ('rent', 'Rent')
   ], string='Contract Type', default='rent')
   
   property_id = fields.Many2one(
      comodel_name='realestate.property', 
      string='Property',
      required=True
   )
   
   partner_id = fields.Many2one(
      comodel_name='res.partner',  
      string='Partner',
      required=True
   )
   
   start_date = fields.Date(string='Start Date')
   
   end_date = fields.Date(string='End Date')
   
   duration_days = fields.Integer(string='Duration (Days)', compute='_compute_duration_days', store=True)
   
   days_to_end = fields.Integer(string='Days to End', compute='_compute_days_to_end')
   
   days_in_progress = fields.Integer(string='Days in Progress', compute='_compute_days_in_progress')
   
   rent = fields.Float(string='Rent')
   
   deposit = fields.Float(string='Deposit')
   
   has_deposit = fields.Boolean(string='Has Deposit', compute='_compute_has_deposit', store=True)
   
   state = fields.Selection([
      ('draft', 'Draft'),
      ('in_progress', 'In Progress'),
      ('finished', 'Finished'),
      ('canceled', 'Canceled')
   ], default='draft', string='State')
   
  
   def action_draft(self):
      self.state = 'draft'
      
   def action_in_progress(self):
      self.state = 'in_progress'
   
   def action_finished(self):
      self.state = 'finished'
      
   def action_canceled(self):
      self.state = 'canceled'
      
   @api.depends('start_date', 'end_date')
   def _compute_duration_days(self):
      for record in self:
         if record.start_date and record.end_date:
            record.duration_days = (record.end_date - record.start_date).days
         else:
            record.duration_days = 0
   
   @api.depends('end_date')         
   def _compute_days_to_end(self):
      for record in self:
         if record.end_date:
            today = fields.Date.today()
            record.days_to_end = (record.end_date - today).days
         else:
            record.days_to_end = 0
            
   @api.depends('deposit')
   def _compute_has_deposit(self):
      for record in self:
         record.has_deposit = record.deposit > 0
            
   def _compute_days_in_progress(self):
      for record in self:
         if record.start_date and record.state == 'in_progress':
            today = fields.Date.today()
            record.days_in_progress = (today - record.start_date).days
         else:
            record.days_in_progress = 0
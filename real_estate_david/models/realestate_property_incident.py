from odoo import models, fields

class RealEstatePropertyIncident(models.Model):
   _name = 'realestate.property.incident'
   _description = 'Property Incident'
   
   name = fields.Char('name')

   description = fields.Char('Description')

   sequence = fields.Integer(string='Sequence', default=10)

   date = fields.Datetime(string='Date')

   property_id = fields.Many2one(
      comodel_name='realestate.property',
      string='Property',
      ondelete='cascade'
   )
   
   priority = fields.Selection([
      ('low', 'Low'),
      ('medium', 'Medium'),
      ('high', 'High'),
      ('very_high', 'Very high'),
   ], string='Priority', default='medium')

   state = fields.Selection([
        ('draft', 'Draft'), 
        ('in_progress', 'In Progress'), 
        ('done', 'Done'), 
        ('canceled', 'Canceled'),
   ], string="State",default='draft')

   user_id = fields.Many2one(
      comodel_name='res.users',
      string='User',
   )
   
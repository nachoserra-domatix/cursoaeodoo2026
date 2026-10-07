from odoo import models, fields, api, _


class RealEstateOwner(models.Model):
   _name = 'realestate.owner'
   _description = 'Owner'
   _inherit = ['mail.thread', 'mail.activity.mixin']
   _inherits = {'res.partner': 'partner_id'}
   
   partner_id = fields.Many2one(
      comodel_name='res.partner',
      string='Partner',
      required=True,
      ondelete='cascade'
   )

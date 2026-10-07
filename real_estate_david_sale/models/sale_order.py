from odoo import models, fields, api


class SaleOrder(models.Model):
   _inherit = 'sale.order'
   
   contract_id = fields.Many2one('realestate.contract', string='Contract')
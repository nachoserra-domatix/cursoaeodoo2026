from odoo import fields, models


class RealEstateAgent(models.Model):
    _name = 'real.estate.agent'
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Real Estate Agent'

    partner_id = fields.Many2one(
        'res.partner', string='Related Partner', required=True, ondelete='cascade')
    license_number = fields.Char(string='License Number')

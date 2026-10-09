from odoo import fields, models


class RealEstateOwner(models.Model):
    _name = 'real.estate.owner'
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Real Estate Owner'

    partner_id = fields.Many2one(
        'res.partner', string='Related Partner', required=True, ondelete='cascade')

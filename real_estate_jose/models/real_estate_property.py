from odoo import models, fields


class RealEstateProperty(models.Model):
    _name = 'real.estate.property'
    _description = 'Real Estate Property'

    def _default_stage_id(self):
        return self.env['real.estate.property.stage'].search(
            [],
            order='sequence, id',
            limit=1,
        )

    name = fields.Char(string='Name', required=True)
    reference = fields.Char(string='Reference')
    description = fields.Text(string='Description')
    price = fields.Float(string='Price')
    availability = fields.Boolean(string='Available', default=True)
    user_id = fields.Many2one('res.users', string='Responsible')
    category_id = fields.Many2one(
        'real.estate.category',
        string='Category',
    )
    stage_id = fields.Many2one(
        'real.estate.property.stage',
        string='Stage',
        default=_default_stage_id,
    )

    def action_reserve(self):
        self.ensure_one()
        self.availability = False

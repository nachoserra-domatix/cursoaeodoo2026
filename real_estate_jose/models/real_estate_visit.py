from odoo import models, fields


class RealEstateVisit(models.Model):
    _name = 'real.estate.visit'
    _description = 'Real Estate Visit'
    _rec_name = 'property_id'

    property_id = fields.Many2one(
        'real.estate.property',
        string='Property',
        required=True,
    )

    date = fields.Datetime(
        string='Visit Date',
        required=True,
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Contact',
    )

    user_id = fields.Many2one(
        'res.users',
        string='Agent',
    )

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('planned', 'Planned'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        required=True,
    )
    def action_set_draft(self):
        self.ensure_one()
        self.state = 'draft'

    def action_set_planned(self):
        self.ensure_one()
        self.state = 'planned'

    def action_set_done(self):
        self.ensure_one()
        self.state = 'done'

    def action_set_cancelled(self):
        self.ensure_one()
        self.state = 'cancelled'

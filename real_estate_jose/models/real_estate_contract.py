from odoo import models, fields


class RealEstateContract(models.Model):
    _name = 'real.estate.contract'
    _description = 'Real Estate Contract'

    name = fields.Char(
        string='Name',
        required=True,
    )
    contract_type = fields.Selection(
        [
            ('rent', 'Rental'),
            ('sale', 'Sale'),
        ],
        string='Type',
        default='rent',
        required=True,
    )
    property_id = fields.Many2one(
        'real.estate.property',
        string='Property',
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Tenant',
    )
    start_date = fields.Date(
        string='Start Date',
    )
    end_date = fields.Date(
        string='End Date',
    )
    rent = fields.Float(
        string='Rent',
    )
    deposit = fields.Float(
        string='Deposit',
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('progress', 'In Progress'),
            ('done', 'Finished'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        required=True,
    )

    def action_set_draft(self):
        self.ensure_one()
        self.state = 'draft'

    def action_set_progress(self):
        self.ensure_one()
        self.state = 'progress'

    def action_set_done(self):
        self.ensure_one()
        self.state = 'done'

    def action_set_cancelled(self):
        self.ensure_one()
        self.state = 'cancelled'

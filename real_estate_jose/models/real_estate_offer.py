from odoo import models, fields


class RealEstateOffer(models.Model):
    _name = 'real.estate.offer'
    _description = 'Real Estate Offer'
    _rec_name = 'partner_id'

    property_id = fields.Many2one(
        'real.estate.property',
        string='Property',
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Buyer',
    )
    amount = fields.Float(
        string='Amount',
    )
    date = fields.Date(
        string='Date',
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('sent', 'Sent'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
        ],
        string='Status',
        default='draft',
        required=True,
    )
    notes = fields.Html(
        string='Notes',
    )

    def action_set_draft(self):
        self.ensure_one()

        was_accepted = self.state == 'accepted'
        self.state = 'draft'

        if was_accepted:
            self.property_id.availability = True

    def action_set_sent(self):
        self.ensure_one()
        self.state = 'sent'

    def action_set_accepted(self):
        self.ensure_one()
        self.state = 'accepted'
        self.property_id.action_reserve()

    def action_set_rejected(self):
        self.ensure_one()

        was_accepted = self.state == 'accepted'
        self.state = 'rejected'

        if was_accepted:
            self.property_id.availability = True

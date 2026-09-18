# -*- coding: utf-8 -*-

from odoo import models, fields, api

class RealEstateOffer(models.Model):
    _name = 'realestate.offer'
    _description = 'RealEstateOffer'

    property_id = fields.Many2one(comodel_name="realestate.property", string="Property")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Buyer")
    offer = fields.Float(string='Offer')
    date =fields.Datetime(string="Offer date")
    status = fields.Selection([('D', 'Draft'), ('S', 'Sent'), ('A', 'Accepted'), ('R', 'Refused')], string='Status', default='D')
    notes = fields.Text(string='Notes')

    def action_draft(self):
        self.write({'status': 'D'})
        return True

    def action_sent(self):
        self.write({'status': 'S'})
        return True

    def action_accepted(self):
        self.write({'status': 'A'})
        self.write({'property_id.status': 'R'})
        return True

    def action_refused(self):
        self.write({'status': 'R'})
        return True
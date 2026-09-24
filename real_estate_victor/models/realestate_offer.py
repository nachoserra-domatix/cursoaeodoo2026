# -*- coding: utf-8 -*-

from odoo import models, fields, api

class RealEstateOffer(models.Model):
    _name = 'realestate.offer'
    _description = 'RealEstateOffer'

    property_id = fields.Many2one(comodel_name="realestate.property", string="Property")
    category_id = fields.Many2one(
        comodel_name="realestate.category",
        string="Category",
        related="property_id.category_id",
        readonly=True
    )
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
        self.property_id.availability = False
        return True

    def action_refused(self):
        self.write({'status': 'R'})
        return True

    def action_create_contract(self):
        vals = {
            'property_id': self.property_id.id,
            'partner_id': self.partner_id.id,
            'type': 'S',
            'start_date': fields.Date.today(),
            'status': 'D'
        }
        contract = self.env['realestate.contract'].create(vals)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'realestate.contract',
            'res_id': contract.id,
            'view_mode': 'form',
            'target': 'current',
        }
# -*- coding: utf-8 -*-

from odoo import models, fields, api

class RealEstateContract(models.Model):
    _name = 'realestate.contract'
    _description = 'RealEstateContract'

    name = fields.Char(string='Contract')
    type = fields.Selection([('R', 'Rent'), ('S', 'Sale')], string='Type')
    property_id = fields.Many2one(comodel_name="realestate.property", string="Property")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Tenant")
    start_date = fields.Date(string='Start date')
    end_date = fields.Date(string='End date')
    rent = fields.Float(string='Rent')
    bail = fields.Float(string='Bail')
    status = fields.Selection([('D', 'Draft'), ('E', 'Ended'), ('C', 'Canceled'), ('O', 'Ongoing')], string='Status', default='D')
    
    def action_draft(self):
        self.write({'status': 'D'})
        return True

    def action_ended(self):
        self.write({'status': 'E'})
        return True

    def action_canceled(self):
        self.write({'status': 'C'})
        return True

    def action_ongoing(self):
        self.write({'status': 'O'})
        return True
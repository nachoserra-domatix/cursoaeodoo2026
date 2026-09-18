# -*- coding: utf-8 -*-

from odoo import models, fields, api

class RealEstateVisit(models.Model):
    _name = 'realestate.visit'
    _description = 'RealEstateVisit'

    name = fields.Char(string='Visit')
    date = fields.Datetime(string='Date')
    property = fields.Many2one(comodel_name='realestate.property', string="Property")
    partner_id = fields.Many2one(comodel_name='res.partner', string='Contact')
    status = fields.Selection([('P', 'Pending'), ('V', 'Visited'), ('R', 'Reserved')], string='Status', default='P')

    def action_reserve(self):
        self.write({'status': 'R'})
        return True



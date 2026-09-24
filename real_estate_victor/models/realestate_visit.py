# -*- coding: utf-8 -*-

from odoo import models, fields, api

class RealEstateVisit(models.Model):
    _name = 'realestate.visit'
    _description = 'RealEstateVisit'

    name = fields.Char(string='Visit')
    date = fields.Datetime(string='Date')
    property_id = fields.Many2one(comodel_name='realestate.property', string="Property")
    partner_id = fields.Many2one(comodel_name='res.partner', string='Contact')
    user_id = fields.Many2one(comodel_name='res.users', string='Manager')
    phone = fields.Char(string="Phone", related="partner_id.phone", readonly=False, store=True)
    email = fields.Char(string="Email", related="partner_id.email", readonly=False, store=True)
    status = fields.Selection([('P', 'Pending'),('S','Scheduled'), ('V', 'Visited'), ('R', 'Reserved'), ('C', 'Cancelled')], string='Status', default='P')


    def action_reserve(self):
        self.write({'availability': False})
        return True



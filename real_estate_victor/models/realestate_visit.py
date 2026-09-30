# -*- coding: utf-8 -*-

from odoo import models, fields, api

class RealEstateVisit(models.Model):
    _name = 'realestate.visit'
    _description = 'RealEstateVisit'

    name = fields.Char(string='Visit')
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    property_id = fields.Many2one(comodel_name='realestate.property', string="Property")
    partner_id = fields.Many2one(comodel_name='res.partner', string='Contact')
    user_id = fields.Many2one(comodel_name='res.users', string='Manager')
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    status = fields.Selection([('P', 'Pending'),('S','Scheduled'), ('V', 'Visited'), ('R', 'Reserved'), ('C', 'Cancelled')], string='Status', default='P')


    def action_reserve(self):
        self.write({'availability': False})
        return True


    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.phone = self.partner_id.phone
            self.personal_email = self.partner_id.email

    def _cron_finish_visits(self):
        visits = self.env['realestate.visit'].search(
            [('date', '<', fields.Datetime.now()),
             ('status', '=', 'S')])
        visits.write({'status': 'V'})

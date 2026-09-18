# -*- coding: utf-8 -*-

from odoo import models, fields, api

class RealEstateProperty(models.Model):
    _name = 'realestate.property'
    _description = 'RealEstateProperty'

    name = fields.Char(string='Property')
    desc = fields.Char(string='Description')
    size = fields.Float(string='Size')
    user_id = fields.Many2one(comodel_name="res.users", string="Manager")
    category_id = fields.Many2one(comodel_name="realestate.category", string="Category")
    status = fields.Selection([('D', 'Draft'), ('N', 'Not available'), ('R', 'Reserved')], string='Status', default='D')

# -*- coding: utf-8 -*-

from odoo import models, fields, api

class RealEstateCategory(models.Model):
    _name = 'realestate.category'
    _description = 'RealEstateCategory'

    active = fields.Boolean(string="Active", default=True)
    name = fields.Char(string='Property')
    desc = fields.Char(string='Description')

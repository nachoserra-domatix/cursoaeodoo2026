# -*- coding: utf-8 -*-

from odoo import models, fields, api

class RealEstate(models.Model):
    _name = 'real.estate'
    _description = 'RealEstate'

    name = fields.Char(string='Propiedad')
    desc = fields.Char(string='Descripción')
    size = fields.Float(string='Metros cuadrados')

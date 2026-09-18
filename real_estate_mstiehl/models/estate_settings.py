from odoo import models, fields, api, _
from datetime import datetime
from datetime import timedelta

class EstateTag(models.Model):
    _name = "estate.tag"
    _description = "Estate Tag"
    
    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")
    active = fields.Boolean(string="Active", default=True)

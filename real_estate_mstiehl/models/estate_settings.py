from odoo import models, fields, api, _
from datetime import datetime
from datetime import timedelta

class EstateTag(models.Model):
    _name = "estate.tag"
    _description = "Estate Tag"
    
    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")
    active = fields.Boolean(string="Active", default=True)

class EstateStages(models.Model):
    _name = "estate.stage"
    _description = "Estate Stages"
    
    name = fields.Char(string="Name", required=True, translation=True)
    code = fields.Char(string="Code", required=True)
    active = fields.Boolean(string="Active", default=True)
    sequence = fields.Integer(string="Sequence", default=1)
    type_id = fields.Many2one(comodel_name="estate.stage.type", string="Type")

class EstateStageType(models.Model):
    _name = "estate.stage.type"
    _description = "Estate Stage Type"
    
    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    active = fields.Boolean(string="Active", default=True)
from odoo import models, fields

   
class DomainType(models.Model):
    _name = "realestate.domain.type"
    _description = "Domain Type"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    active = fields.Boolean(string="Active", default=True)
    
class Domain(models.Model):
    _name = "realestate.domain"
    _description = "Domain"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    code = fields.Char(string="Code", required=True)
    active = fields.Boolean(string="Active", default=True)
    domain_type_id = fields.Many2one(comodel_name="realestate.domain.type", string="Domain Type")
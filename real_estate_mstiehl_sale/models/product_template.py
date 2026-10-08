from odoo import models, fields, api, _

class ProductTemplate(models.Model):
    _inherit = "product.template"

    rent_ok = fields.Boolean(string="Rent", default=False)
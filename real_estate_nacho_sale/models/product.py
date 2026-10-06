from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_rental = fields.Boolean(string="Es de alquiler")
    estate_property_id = fields.Many2one(
        comodel_name="estate.property",
        string="Estate Property",
        ondelete="restrict",
    )

    @api.constrains("is_rental", "estate_property_id")
    def _check_rental_property(self):
        for product in self:
            if product.is_rental and not product.estate_property_id:
                raise ValidationError(
                    _("Select an estate property for rental products.")
                )
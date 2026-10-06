from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    contract_id = fields.Many2one(
        comodel_name="realestate.contract",
        string="Real Estate Contract",
        ondelete="set null",
    )

    def action_confirm(self):
        result = super().action_confirm()
        for order in self:
            if order.contract_id:
                continue

            rental_line = order.order_line.filtered(
                lambda line: line.product_id.is_rental
            )[:1]
            if not rental_line:
                continue

            contract = self.env["realestate.contract"].sudo().create(
                {
                    "name": f"Contract - {order.name}",
                    "contract_type": "rental",
                    "property_id": rental_line.product_id.estate_property_id.id,
                    "tenant_id": order.partner_id.id,
                    "product_id": rental_line.product_id.id,
                    "rent": rental_line.price_unit,
                    "start_date": fields.Date.today(),
                    "end_date": fields.Date.today(),
                    "deposit": 0.0,
                }
            )
            order.contract_id = contract
        return result
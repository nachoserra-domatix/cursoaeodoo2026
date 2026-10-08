from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    contract_id = fields.Many2one(comodel_name="estate.contract", string="Contract")
    
    
    def action_confirm(self):
        res = super().action_confirm()
        print("Sale Order Confirmed. Creating contract if applicable...")
        for order in self:
            if order.contract_id:
                continue
            rental_line = order.order_line.filtered(lambda l: l.product_id.rent_ok)[:1]
            if not rental_line:
                continue
            try:
                print(f"Creating contract for sale order {order.name} with rental line {rental_line.product_id.name}...")
                new_contract = self.env["estate.contract"].create({
                    "product_id": rental_line.product_id.id,
                    "price": order.amount_total,
                    "main_buyer_id": order.partner_id.id,
                })
                order.write({"contract_id": new_contract.id})
            except Exception as e:
                raise UserError(_("Error creating contract: %s") % e)
        return res
        
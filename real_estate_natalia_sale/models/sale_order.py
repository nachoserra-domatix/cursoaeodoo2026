from odoo import models, fields, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    contract_id = fields.Many2one(
        comodel_name='realestate.contract', 
        string='Contract'
    )

    def action_confirm(self):
        for order in self:
            rental_lines = order.order_line.filtered(lambda line: line.product_id.rental_ok)
            if len(rental_lines) > 1:
                raise UserError(_("Only one rental product is allowed per order."))
        res = super().action_confirm()
        for order in self:
            if order.contract_id:
                continue
            rental_lines = order.order_line.filtered(lambda line: line.product_id.rental_ok)
            if not rental_lines:
                continue
            rental_line = rental_lines[0]
            contract = self.env['realestate.contract'].create({
                'contract_type': 'rental',
                'property_id': rental_line.product_id.property_id.id,
                'partner_id': order.partner_id.id,
                'product_id': rental_line.product_id.id,
                'rent': rental_line.price_unit,
            })
            order.contract_id = contract.id        
        return res
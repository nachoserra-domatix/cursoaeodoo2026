from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EstateContract(models.Model):
    _inherit = "estate.contract"
    
    product_id = fields.Many2one(comodel_name="product.product", string="Product", tracking=True)
   
    order_ids = fields.One2many(comodel_name="sale.order", inverse_name="contract_id", string="Sale Orders") 
    
    num_orders = fields.Integer(string="Number of Orders", compute="_compute_num_orders")
    
    @api.depends("order_ids")
    def _compute_num_orders(self):
        for record in self:
            record.num_orders = len(record.order_ids)
    
    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id:
            self.price = self.product_id.lst_price
    
    def action_cancel(self):
        result = super().action_cancel()
        orders = self.env["sale.order"].search([("contract_id", "in", self.ids), ("state", "not in", ["done", "cancel"])])
        for order in orders:
            order.action_cancel()
        return result

    def action_confirm_and_invoice(self):
        self.ensure_one()
        draft_orders = self.env["sale.order"].search([
            ("contract_id", "=", self.id),
            ("state", "not in", ["sale", "done", "cancel"]),
        ])
        draft_orders.action_confirm()
        orders_to_invoice = self.env["sale.order"].search([
            ("contract_id", "=", self.id),
            ("state", "in", ["sale", "done"]),
            ("invoice_status", "=", "to invoice"),
        ])
        if not orders_to_invoice:
            raise UserError(_("There is nothing to invoice on this contract's sale orders."))
        invoices = orders_to_invoice._create_invoices()
        return {
            "name": _("Invoices"),
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "list,form" if len(invoices) > 1 else "form",
            "res_id": invoices.id if len(invoices) == 1 else False,
            "domain": [("id", "in", invoices.ids)],
        }

    def action_view_orders(self):
        return {
            "name": _("Sale Orders"),
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "view_mode": "list,form",
            "domain": [("contract_id", "=", self.id)],
            "context": {"default_contract_id": self.id},
        }
        
    def action_create_order(self):
        for record in self:
                if not record.product_id:
                    raise UserError(_("Please select a Product on the contract before creating a Sale Order."))

                order = self.env["sale.order"].create(
                    {
                        "partner_id": self.main_buyer_id.id,
                        "contract_id": self.id,
                        "order_line": [
                            (0,0,
                                {
                                    "product_id": self.product_id.id,
                                    "name": self.product_id.name,
                                    "product_uom_qty": 1,
                                    "price_unit": self.product_id.lst_price,
                                },
                            )
                        ],
                    }
                )
                return {
                    "name": _("Sale Order"),
                    "type": "ir.actions.act_window",
                    "res_model": "sale.order",
                    "view_mode": "form",
                    "res_id": order.id,
                }
                
            
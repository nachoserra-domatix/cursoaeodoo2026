from odoo import _, Command, api, fields, models
from odoo.exceptions import UserError

class RealEstateContract(models.Model):
    _inherit = "realestate.contract"

    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
    )
    order_ids = fields.One2many(
        comodel_name="sale.order",
        inverse_name="contract_id",
        string="Sales Orders",
    )
    order_count = fields.Integer(
        compute="_compute_order_count",
        string="Sales Orders",
    )

    @api.model_create_multi
    def create(self, vals_list):
        sequence_model = self.env["ir.sequence"]
        contract_vals_list = []
        for vals in vals_list:
            contract_vals = vals.copy()
            contract_name = sequence_model.next_by_code("realestate.contract")
            if not contract_name:
                raise UserError(_("No sequence configured for real estate contracts."))
            contract_vals["name"] = contract_name
            contract_vals_list.append(contract_vals)
        return super().create(contract_vals_list)

    @api.onchange("product_id")
    def _onchange_product_id(self):
        for record in self:
            record.rent = record.product_id.list_price if record.product_id else 0.0

    @api.depends("order_ids")
    def _compute_order_count(self):
        for record in self:
            record.order_count = len(record.order_ids)

    def action_view_orders(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Sales Orders"),
            "res_model": "sale.order",
            "view_mode": "list,form",
            "domain": [("contract_id", "=", self.id)],
            "context": {"default_contract_id": self.id},
        }

    def action_create_sale_order(self):
        self.ensure_one()
        if not self.product_id:
            raise UserError(_("Select a product before creating a sales order."))

        order = self.env["sale.order"].create(
            {
                "partner_id": self.tenant_id.id,
                "contract_id": self.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product_id.id,
                            "product_uom_qty": 1,
                            "price_unit": self.rent,
                        }
                    )
                ],
            }
        )
        return {
            "type": "ir.actions.act_window",
            "name": _("Sales Order"),
            "res_model": "sale.order",
            "res_id": order.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_mark_cancelled(self):
        orders = self.mapped("order_ids").filtered(
            lambda order: order.state != "cancel"
        )
        orders.action_cancel()
        return super().action_mark_cancelled()

    def action_confirm_and_invoice_orders(self):
        self.ensure_one()
        orders = self.order_ids.filtered(lambda order: order.state != "cancel")
        if not orders:
            raise UserError(_("This contract has no sales orders to invoice."))

        orders.filtered(lambda order: order.state in ("draft", "sent")).action_confirm()
        invoiceable_orders = orders.filtered(
            lambda order: order.state == "sale"
            and order.invoice_status == "to invoice"
        )
        if invoiceable_orders:
            invoices = invoiceable_orders._create_invoices()
        else:
            invoices = orders.mapped("invoice_ids").filtered(
                lambda invoice: invoice.state != "cancel"
            )
        if not invoices:
            raise UserError(
                _("The sales orders are not invoiceable yet. Check the product invoicing policy and delivered quantity.")
            )
        return orders.action_view_invoice(invoices)

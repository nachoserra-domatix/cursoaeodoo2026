from odoo import api, fields, models, _


class RealEstateContract(models.Model):
    _inherit = 'real.estate.contract'

    name = fields.Char(default=lambda self: _('New'))
    product_id = fields.Many2one('product.product', string='Product')
    order_ids = fields.One2many(
        'sale.order', 'contract_id', string='Sales Orders')
    order_count = fields.Integer(
        string='Sales Orders count', compute='_compute_order_count')

    @api.depends('order_ids')
    def _compute_order_count(self):
        for record in self:
            record.order_count = len(record.order_ids)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.amount = self.product_id.lst_price

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].sudo().next_by_code(
                    'real.estate.contract.sequence') or _('New')
        return super().create(vals_list)

    def action_view_orders(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales Orders',
            'res_model': 'sale.order',
            'view_mode': 'list,form',
            'domain': [('contract_id', '=', self.id)],
        }

    def action_create_sale_order(self):
        self.ensure_one()
        return self.env['sale.order'].create({
            'partner_id': self.tenant_id.id,
            'contract_id': self.id,
            'order_line': [(0, 0, {
                'product_id': self.product_id.id,
                'name': self.product_id.get_product_multiline_description_sale(),
                'product_uom_qty': 1,
                'price_unit': self.amount,
            })],
        })

    def action_cancel(self):
        result = super().action_cancel()
        self.order_ids.action_cancel()
        return result

    def action_confirm_and_invoice(self):
        self.ensure_one()
        self.order_ids.action_confirm()
        self.order_ids._create_invoices()

from odoo import models, fields
from datetime import timedelta

class RealEstateVisitLotCreate(models.TransientModel):
    _name = "realestate.visit.lot.create"
    _description = "Wizard to create visits by lots on specific property"

    start_date = fields.Datetime(string="Start Date", required=True)
        end_date = fields.Datetime(string="End Date", required=True)

    def action_visit_lot_create(self):
        vals_list = []
        current_date = self.start_date
        property = self.env['realestate.property'].browse(self.env.context.get('active_id'))
        while current_date <= self.end_date:
            vals_list.append({
                'property_id': property.id,
                'date': current_date,
                'user_id': property.user_id.id,
                'status': 'S',
            })
            current_date += timedelta(days=1)
        visits = self.env['realestate.visit'].create(vals_list)

        return {

            'type': 'ir.actions.act_window',
            'name': 'Scheduled Visits',
            'res_model': 'realestate.visit',
            'view_mode': 'list,form',
            'domain': [('id', 'in', visits.ids)],
        }





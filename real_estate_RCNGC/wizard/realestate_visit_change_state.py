from odoo import models, fields

class RealestateVisitChangeState(models.TransientModel):
    _name = 'realestate.visit.change.state'
    _description = 'Change State of Real Estate Visit'

    state = fields.Selection(
        [('pending', 'Pending'), ('done', 'Done'), ('canceled', 'Canceled')],
        string='State',
        required=True
    )   

    def action_change_state(self):
        active_ids = self._context.get('active_ids')
        contract = self.env['realestate.visit'].browse(active_ids)
        contract.write({
            'state': self.state
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Visits',
            'res_model': 'realestate.visit',
            'view_mode': 'list,form',
            'domain': [('id', 'in', active_ids)],
        } 
    

    
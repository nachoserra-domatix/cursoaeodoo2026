from odoo import models, fields, api, _
from datetime import datetime
from datetime import timedelta

class EstateVisitChangeState(models.TransientModel):
    _name = "estate.visit.change.stage"
    _description = "Estate Visit Change Stage"
    
    stage_id = fields.Many2one(comodel_name="estate.stage", string="Stage", domain="[('type_id.code','=','visit')]", required=True)

    def action_change_visit_stage(self):
        for visit in self.env['estate.property.visit'].browse(self.env.context.get('active_ids')):
            visit.stage_id = self.stage_id

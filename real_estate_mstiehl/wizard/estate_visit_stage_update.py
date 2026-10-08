from odoo import models, fields, api, _


class EstateVisitStageUpdate(models.TransientModel):
    _name = "estate.visit.stage.update"
    _description = "Estate Visit Stage Update"

    new_stage_id = fields.Many2one(comodel_name="estate.stage", string="New Stage", domain="[('type_id.code','=','visit')]", required=True)

    def action_apply_stage_update(self):
        visits = self.env["estate.property.visit"].browse(self.env.context.get("active_ids"))
        visits.write({"stage_id": self.new_stage_id.id})

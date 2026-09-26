from odoo import fields, models


class EstatePropertyStageWizard(models.TransientModel):
    _name = "estate.property.stage.wizard"
    _description = "Change Estate Property Stage"

    stage_id = fields.Many2one(
        comodel_name="realestate.property.stage",
        string="New Stage",
        required=True,
    )

    def action_apply(self):
        properties = self.env["estate.property"].browse(
            self.env.context.get("active_ids", [])
        ).exists()
        properties.write({"stage_id": self.stage_id.id})
        return {"type": "ir.actions.act_window_close"}

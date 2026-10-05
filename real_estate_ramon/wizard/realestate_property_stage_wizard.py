from odoo import models, fields

class RealEstatePropertyStageWizard(models.TransientModel):
    _name = "realestate.property.stage.wizard"
    _description = "Change Property Stage"

    stage_id = fields.Many2one(
        comodel_name="realestate",
        string="Stage",
        required=True,
    )

    def action_apply(self):
        properties = self.env["realestate.property"].browse(
            self.env.context.get("active_ids", [])
        )

        properties.write({
            "stage_id": self.stage_id.id
        })

        return {"type": "ir.actions.act_window_close"}
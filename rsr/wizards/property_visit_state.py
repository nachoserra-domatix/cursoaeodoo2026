from odoo import fields, models

class EstatePropertyVisitStateWizard(models.TransientModel):
    _name = "estate.property.visit.state.wizard"
    _description = "Change Visit State"

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("planned", "Planned"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        string="New State",
        required=True,
    )

    def action_apply(self):
        self.ensure_one()
        visits = self.env["estate.property.visit"].browse(
            self.env.context.get("active_ids", [])
        ).exists()
        visits.write({"state": self.state})
        return {"type": "ir.actions.act_window_close"}
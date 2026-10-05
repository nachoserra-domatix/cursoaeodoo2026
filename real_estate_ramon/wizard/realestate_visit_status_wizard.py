from odoo import models, fields


class RealEstateVisitStatusWizard(models.TransientModel):
    _name = "realestate.visit.status.wizard"
    _description = "Change Visit Status"

    status = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("scheduled", "Scheduled"),
            ("done", "Done"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        required=True,
    )

    def action_apply(self):
        visits = self.env["realestate.visit"].browse(
            self.env.context.get("active_ids", [])
        )

        visits.write({
            "status": self.status,
        })

        return {"type": "ir.actions.act_window_close"}
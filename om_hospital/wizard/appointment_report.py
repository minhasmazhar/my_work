from odoo import api, fields, models


class AppointmentReportWizard(models.TransientModel):
    _name = "appointment.report.wizard"
    _description = "Search Appointment Wizard"

    @api.model
    def default_get(self, fields):
        res = super(AppointmentReportWizard, self).default_get(fields)
        # print('context-------------- ', self._context)
        res['patient_id'] = self._context.get('active_id')
        return res

    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")

    def action_print_report(self):
        appointments = self.env['hospital.appointment'].search_read([])
        data = {
            'form': self.read()[0],
            'appointments': appointments
        }
        return self.env.ref('om_hospital.action_report_appointment').report_action(self, data=data)

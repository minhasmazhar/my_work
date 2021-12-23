from odoo import api, models, fields


class EvaluationModel(models.Model):
    _name = 'evaluation.model'
    _description = 'Evaluation'
    _rec_name = 'patient_id'

    patient_id = fields.Many2one('patient.model', string='Patient')
    doctor_id = fields.Many2one('doctor.model', string='Doctor')
    nurse_id = fields.Many2one('nurse.model', string='Nurse')
    date = fields.Date(string='Date')
    diagnosis = fields.Char(string='Diagnosis')
    recommendations = fields.Text(string='Recommendations')
    sale_order_ref = fields.Char(string="Sale Order Ref")

    def auto_email(self):
        print("my Cron job running")

from odoo import api, models, fields


class EvaluationModelWizard(models.TransientModel):
    _name = 'evaluation.model.wizard'
    _description = 'Evaluation Model Wizard'

    patient_id = fields.Many2one('patient.model', string='Patient')

    def action_print_report(self):
        # print(self.read()[0])
        data = {
            'model': 'evaluation.model.wizard',
            'form': self.read()[0]
        }
        print(data['form']['patient_id'])
        return self.env.ref('my_hospital.action_evaluation_card').report_action(self, data=data, config=False)

from odoo import api, models, fields


class EvaluationModelWizard(models.TransientModel):
    _name = 'employee.model.wizard'
    _description = 'Employee Model Wizard'

    employee_ids = fields.Many2many('employee.model', string='Employee')

    def action_print_report(self):
        employee_list = []
        for rec in self.employee_ids:
            print(rec.id)
            employee_list.append(rec.id)
        print("employee_list ", employee_list)
        print(self.read()[0])
        employees = self.env['employee.model'].search_read([])
        print(self.employee_ids)
        data = {'employee_id': employees,
                'form_data': self.read()[0]}
        return self.env.ref('my_hospital.report_employees_wizard_xls').report_action(self, data=data)

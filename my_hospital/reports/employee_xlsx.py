from odoo import models
import base64
import io


class EmployeeXlsx(models.AbstractModel):
    _name = 'report.my_hospital.report_employee_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, employees):
        print(employees)
        sheet = workbook.add_worksheet('Employees')
        bold = workbook.add_format({'bold': False})
        bold1 = workbook.add_format({'bold': True})
        format1 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'cyan'})
        sheet.set_column('B:G', 20)
        col = 1
        row = 1
        sheet.write(1, 1, 'Name', bold1)
        sheet.write(1, 2, 'Gender', bold1)
        sheet.write(1, 3, 'Phone', bold1)
        sheet.write(1, 4, 'Job Description', bold1)
        sheet.write(1, 5, 'Address', bold1)
        sheet.write(1, 6, 'Department Name', bold1)
        sheet.merge_range('B1:G1', 'Employees', format1)
        for obj in employees:
            row += 1
            sheet.write(row, col, obj.name, bold)
            sheet.write(row, col + 1, obj.gender, bold)
            sheet.write(row, col + 2, obj.phone, bold)
            sheet.write(row, col + 3, obj.job_description, bold)
            sheet.write(row, col + 4, obj.address, bold)
            sheet.write(row, col + 5, obj.department_id.name, bold)


class EmployeeWizardXlsx(models.AbstractModel):
    _name = 'report.my_hospital.report_employees_wizard_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, employees):
        # print("Data ====> ", data['employee_id'])
        sheet = workbook.add_worksheet('Employees')
        bold = workbook.add_format({'bold': False})
        bold1 = workbook.add_format({'bold': True})
        format1 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'cyan'})
        sheet.set_column('B:G', 20)
        col = 1
        row = 1
        sheet.write(1, 1, 'Name', bold1)
        sheet.write(1, 2, 'Gender', bold1)
        sheet.write(1, 3, 'Phone', bold1)
        sheet.write(1, 4, 'Job Description', bold1)
        sheet.write(1, 5, 'Address', bold1)
        sheet.write(1, 6, 'Department Name', bold1)
        sheet.merge_range('B1:G1', 'Employees', format1)
        for obj in data['employee_id']:
            # print("hi ", obj)
            row += 1
            sheet.write(row, col, obj['name'], bold)
            sheet.write(row, col + 1, obj['gender'], bold)
            sheet.write(row, col + 2, obj['phone'], bold)
            sheet.write(row, col + 3, obj['job_description'], bold)
            sheet.write(row, col + 4, obj['address'], bold)
            sheet.write(row, col + 5, obj['department_id'][1], bold)

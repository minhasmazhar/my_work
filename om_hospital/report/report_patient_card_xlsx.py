from odoo import models
import base64
import io


class PatientCardXlsx(models.AbstractModel):
    _name = 'report.om_hospital.report_patient_card_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patients):
        print(patients)
        sheet = workbook.add_worksheet('Patient ID Cards!')
        bold = workbook.add_format({'bold': True})
        format1 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'yellow'})
        sheet.set_column('C:C', 20)
        row = 1
        col = 1
        for obj in patients:
            report_name = obj.name
            # One sheet by partner
            sheet = workbook.add_worksheet(report_name[:31])
            row += 1
            sheet.merge_range(row, col, row, col + 5, 'ID Card', format1)

            row += 1
            if obj.image:
                product_image = io.BytesIO(base64.b64decode(obj.image))
                sheet.insert_image(row, col, "image.png", {'image_data': product_image, 'x_scale': 0.2, 'y_scale': 0.2})

                row += 5

            row += 1
            sheet.write(row, col, 'Name', bold)
            sheet.write(row, col + 1, obj.name)
            # row += 1
            sheet.write(row, col + 2, 'Age', bold)
            sheet.write(row, col + 3, obj.age)
            sheet.write(row, col + 4, 'Reference', bold)
            sheet.write(row, col + 5, obj.reference)
            row += 2

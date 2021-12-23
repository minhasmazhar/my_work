from datetime import date

from odoo import api, models, fields


class SaleOrderExt(models.Model):
    _inherit = 'sale.order'

    patient_id = fields.Many2one('patient.model', string='Patient')
    doctor_id = fields.Many2one('doctor.model', string='Doctor')
    invoice_paid = fields.Boolean(string='Invoice Paid', default=False, compute='_compute_invoice_paid')

    def action_evaluation(self):
        # print("Name ", self.invoice_ids.payment_state)
        # print("Name ", self.invoice_ids)
        # print(self.env['evaluation.model'].search_count([('sale_order_ref', '=', self.name)]))
        # print(self.doctor_id.id)
        if self.env['evaluation.model'].search_count([('sale_order_ref', '=', self.name)]) == 0:
            id_created = self.env['evaluation.model'].create(
                {'patient_id': self.patient_id.id, 'doctor_id': self.doctor_id.id, 'sale_order_ref': self.name,
                 'date': date.today(),
                 'diagnosis': 'Created using evaluation button!'}
            )

            view_id = self.env.ref('my_hospital.evaluation_model_view_form').id
            context = self._context.copy()
            print("Context ", context)
            print("View id ", view_id)
            print("id_created  ", id_created.id)
            return {
                'name': 'Evaluation',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'evaluation.model',
                'res_id': id_created.id,
                # 'target': 'new'
            }
        else:
            print("else")
            obj_list = self.env['evaluation.model'].search([('sale_order_ref', '=', self.name)])
            return {
                'name': 'Evaluation',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'evaluation.model',
                'res_id': obj_list.id,
                # 'target': 'new'
            }

    def _compute_invoice_paid(self):
        # count = self.env['sale.order'].search_count([('payment_state', '=', 'paid'), ('id', '=', self.id)])
        if self.invoice_ids:
            for rec in self.invoice_ids:
                print(rec.id)
                sr = self.env['account.move'].search_count([('id', '=', rec.id), ('payment_state', '=', 'paid')])
                if sr > 0:
                    self.invoice_paid = True
                    return
                else:
                    self.invoice_paid = False

        else:
            self.invoice_paid = False

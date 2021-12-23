from odoo import api, models, fields
from odoo.tools.translate import _


class Doctor(models.Model):
    _name = "hospital.doctor"
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Doctor'
    _rec_name = 'doctor_name'

    doctor_name = fields.Char(string="Name", required=True, tracking=True)
    age = fields.Integer(string="Age", tracking=True, copy=False)
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female'),
                               ('other', 'Other')], required=True, default='male', tracking=True)
    note = fields.Text(string="Description")
    image = fields.Binary(string="Doctor Image")
    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count')
    active = fields.Boolean(string="Active", default=True)

    def _compute_appointment_count(self):
        # print('self-------->', self.id)
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('doctor_id', '=', rec.id)])
            rec.appointment_count = appointment_count

    def copy(self, default=None):
        print("copy function overridden!")
        # raise exceptions.UserError(_('You cannot duplicate the doctor record.'))
        if default is None:
            default = {}
        if not default.get('doctor_name'):
            default['doctor_name'] = _("%s (copy)", self.doctor_name)
        default['note'] = 'Copied Record! (Copy Method)'
        return super(Doctor, self).copy(default)

    @api.model
    def name_create(self, name):
        print("Name Create override in Doctor!")
        # rtn = self.create({'doctor_name': name, 'age': 40})
        # return  rtn.name_get()[0]
        return super(Doctor, self).name_create(name)

    # def name_get(self):
    #     result = []
    #     for rec in self:
    #         result.append((rec.id, '%s - %s' % (rec.doctor_name, rec.gender.upper())))
    #
    #     return result

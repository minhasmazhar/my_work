from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital Patients"

    @api.model
    def default_get(self, fields):
        result = super(HospitalPatient, self).default_get(fields)
        # print('fields--------------->', fields)
        # print('result--------------->', result)
        if not result.get('gender'):
            result['gender'] = 'female'
        result['age'] = 26
        result['note'] = 'This is patient default value! (Set in default_get function)'
        return result

    name = fields.Char(string="Name", required=True, translate=True, tracking=True)
    reference = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                            index=True, default='New')
    age = fields.Integer(string="Age", tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], required=True,
                              default='male')
    note = fields.Text(string='Description')
    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')], default="draft",
        string="Status")
    responsible_id = fields.Many2one('res.partner', string="Responsible")
    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count')
    image = fields.Binary(string="Patient Image")
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointments')

    def _compute_appointment_count(self):
        # print('self-------->', self.id)
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            rec.appointment_count = appointment_count

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.model
    def create(self, vals):
        print("Successfully override create method.")
        if not vals.get('note'):
            vals['note'] = 'New Patient'
        vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        res = super(HospitalPatient, self).create(vals)
        # print('res -------->', res)
        # print('vals -------->', vals)
        return res

    @api.constrains('name')
    def check_name(self):
        for rec in self:
            patients = self.env['hospital.patient'].search([('name', '=', rec.name), ('id', '!=', rec.id)])
            if patients:
                raise ValidationError("Name %s already exists!" % rec.name)

    @api.constrains('age')
    def check_age(self):
        for rec in self:
            if rec.age == 0 or rec.age < 0:
                raise ValidationError("Age cannot be 0 (or less than 0)!")

    def name_get(self):
        result = []
        for rec in self:
            name = '[' + rec.reference + '] ' + rec.name + ' ' + rec.gender
            result.append((rec.id, name))
        return result

    def action_open_appointments(self):
        print("Open Appointments Clicked!")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'hospital.appointment',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
            'view_mode': 'tree,form',
            # 'target': 'new'
        }

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        print("Name ", name)
        print("Args ", args)
        print("operator ", operator)
        if name:
            records = self.search(
                ['|', '|', ('name', operator, name), ('state', operator, name), ('note', operator, name)])
            print("Records ", records)
            return records.name_get()
        return super(HospitalPatient, self).name_search(name=name, args=args, operator=operator, limit=limit)

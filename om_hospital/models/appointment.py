from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital Appointment"
    _order = "id desc"

    name = fields.Char(string="Name", translate=True, tracking=True)
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')], default="draft",
        string="Status")
    note = fields.Text(string='Description')
    date_appointment = fields.Date(string="Date")
    date_checkup = fields.Datetime(string="Date Checkup")
    age = fields.Integer(string="Age", related="patient_id.age", tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], required=True,
                              default='male')
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True)
    reference = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                            index=True, default='New')
    prescription = fields.Text(string='Prescription')
    prescription_line_ids = fields.One2many("appointment.prescription.lines", "appointment_id",
                                            string="Prescription Lines")

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        print("onchange triggered!")
        if self.patient_id:
            if self.patient_id.gender:
                self.gender = self.patient_id.gender
            if self.patient_id.note:
                self.note = self.patient_id.note

        else:
            self.gender = ''
            self.note = ''

    @api.model
    def create(self, vals):
        # print("Successfully override create method.")
        vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        res = super(HospitalAppointment, self).create(vals)
        # print('res -------->', res)
        # print('vals -------->', vals)
        return res

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_url(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'https://www.youtube.com/watch?v=7jbaJSZLL8A&list=PLqRRLx0cl0homY1elJbSoWfeQbRKJ-oPO&index=54',
        }

    def unlink(self):
        print("unlink override!")
        if self.state == 'done':
            raise ValidationError("You cannot delete a done state record! %s " % self.name)
        return super(HospitalAppointment, self).unlink()


class AppointmentPrescriptionLines(models.Model):
    _name = "appointment.prescription.lines"
    _description = "Appointment Prescription Lines"

    name = fields.Char(string="Medicine", required=True)
    qty = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")

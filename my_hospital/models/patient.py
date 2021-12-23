from odoo import api, models, fields


class PatientModel(models.Model):
    _name = 'patient.model'
    _description = 'Hospital Patients'

    name = fields.Char(string='Name')
    age = fields.Integer(string='Age')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='male',
                              string='Gender')
    description = fields.Char(string='Description')
    mobile_phone = fields.Char(string='Mobile Phone')

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        print(name)
        args = args or []
        recs = self.browse()
        if not recs:
            recs = self.search([('mobile_phone', operator, name)] + args, limit=limit)
        return recs.name_get()

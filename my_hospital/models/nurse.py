from odoo import api, models, fields


class NurseModel(models.Model):
    _name = 'nurse.model'
    _description = 'Hospital Nurses'

    name = fields.Char(string='Name')
    age = fields.Integer(string='Age')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='male',
                              string='Gender')
    description = fields.Char(string='Description')
    mobile_phone = fields.Char(string='Mobile Phone')

from odoo import api, fields, models


class CustomModel(models.Model):
    _name = 'custom.model'
    _description = 'Custom Model'
    name = fields.Char(string="Name", required=True)
    age = fields.Integer(string="Age")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='male')

    def button_click(self):
        for rec in self:
            self.name = 'default name (Button Clicked)'

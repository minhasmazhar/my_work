from odoo import api, models, fields


class DepartmentModel(models.Model):
    _name = 'department.model'
    _description = 'Department Model'

    name = fields.Char(string="Name")

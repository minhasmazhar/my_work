from datetime import date

from odoo import api, models, fields


class TasksModel(models.Model):
    _name = "tasks.model"
    _description = "Task Checklist Testing"

    name = fields.Char(string="Task")

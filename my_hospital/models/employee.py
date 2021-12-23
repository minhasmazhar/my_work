import logging
from time import timezone

from odoo import api, models, fields, exceptions, tools
from odoo.addons.base.models.res_users import check_identity
from zk import ZK
from datetime import datetime, timedelta
import pytz


# class HrEmployee(models.Model):
#     _inherit = 'hr.employee'
#
#     device_id = fields.Integer(string='Biometric Device ID', help="Give the biometric device id")


class ResCompanyExt(models.Model):
    _inherit = 'res.company'

    hours = fields.Integer(string='Hours', help="Hours to be adjusted!")


def device_connect(zk):
    try:
        conn = zk.connect()
        return conn
    except:
        print('Connection Error!')


class EmployeeModel(models.Model):
    _name = 'employee.model'
    _description = 'Employee Model'

    name = fields.Char(string="Name")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='male',
                              string='Gender')
    code = fields.Char(string="Code")
    phone = fields.Char(string="Phone")
    address = fields.Char(string="Address")
    department_id = fields.Many2one('department.model', string="Department")
    job_description = fields.Text(string="Job Description")
    picture = fields.Image(string="Image")
    task_checklist = fields.Many2many("tasks.model", string="Check List")
    checklist_progress = fields.Float(compute="_checklist_progress", string="Progress", store=True,
                                      default=0.0)
    checklist_count = fields.Integer(string="Checklist Count", compute="_compute_checklist_count")
    address_id = fields.Many2one('res.partner', string='Working Address')
    employee_id = fields.Many2one('hr.employee', string='Employee')

    @check_identity
    def action_open_checklist(self):
        pass

    def _compute_checklist_count(self):
        if self.task_checklist:
            self.checklist_count = len(self.task_checklist)
        else:
            self.checklist_count = 0

    @api.depends('task_checklist')
    def _checklist_progress(self):
        for rec in self:
            total_len = self.env['tasks.model'].search_count([])
            check_list_len = len(rec.task_checklist)
            if total_len != 0:
                rec.checklist_progress = (check_list_len * 100) / total_len

    max_rate = fields.Integer(string="Maximum Rate", default=100)

    @api.model
    def create(self, vals):
        print("Create method (Employee)")
        if 'picture' in vals:
            image = tools.ImageProcess(vals['picture'])
            # resize uploaded image into 250 X 250
            resize_image = image.resize(250, 250)
            resize_image_b64 = resize_image.image_base64()
            vals['picture'] = resize_image_b64
        obj = super(EmployeeModel, self).create(vals)
        return obj

    # @api.multi
    def write(self, values):
        print("Update/Write method! (employee)")
        return super(EmployeeModel, self).write(values)
        # your logic goes here

    # @api.multi
    def unlink(self):
        print("Delete/Unlink method! (employee)")
        raise exceptions.UserError('Deleting employee records is not allowed.')
        return super(EmployeeModel, self).unlink()

    def action_open_department(self, context=None):
        domain = [('id', '=', self.department_id.id)]
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'department.model',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': domain,
        }

    def action_send_email(self):
        logging.info('Starting Attendance Procedure!')

        d = datetime.today() - timedelta(hours=5, minutes=0)

        print(d.strftime('%H:%M:%S'))

        machine_ip = '192.168.18.234'
        zk_port = 4370
        timeout = 15

        try:
            zk = ZK(machine_ip, port=zk_port, timeout=timeout, password=0, force_udp=False, ommit_ping=False)
        except Exception as e:
            print("Exception: ", e)
        conn = device_connect(zk)
        print('connection: ', conn)
        if conn:
            try:
                attendance = conn.get_attendance()
                print(attendance)
            except:
                attendance = False
            if attendance:
                count = 0
                # print(attendance)
                for each in attendance:
                    # print(type(each))
                    check_out = None
                    check_in = None
                    count += 1
                    atten_time = each.timestamp - timedelta(hours=self.employee_id.company_id.hours, minutes=0)

                    if each.punch == 1:
                        check_out = atten_time
                    else:
                        check_in = atten_time
                    print(f'record id: {each.uid} User {each.user_id} attendance time {atten_time}')
                    employee = self.env['hr.employee'].search([('device_id', '=', each.user_id)])
                    if employee:
                        pass
                    else:
                        user = conn.get_users()
                        for uid in user:
                            if uid.user_id == each.user_id:
                                employee_name = uid.name

                        self.env['hr.employee'].create(
                            {'device_id': each.user_id, 'name': employee_name, 'address_id': self.address_id.id})
                        print('EMPLOYEE CREATED!')

                    self.env['employee.attendance'].create(
                        {'check_in': check_in, 'check_out': check_out, 'user_id': each.user_id})
                    res = self.env['employee.attendance'].search([])
                    # print(check_in, check_out)
                    # self.unlink(find_id.id)

                    zk.clear_attendance()

                    # print(zk.get_device_name())

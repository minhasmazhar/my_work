from odoo import api, models, fields, _
from odoo import api, models, fields, exceptions, tools
from odoo.exceptions import UserError, Warning
import datetime as dt


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    device_id = fields.Char(string='Biometric Device ID')


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    date_only = fields.Date(string='Date Only')
    active = fields.Boolean(string="Active")


def device_connect(zk):
    try:
        conn = zk.connect()
        return conn
    except Exception as e:
        raise UserError(_("Connection failed! please try again."))
        # print(e)


class EmployeeAttendance(models.Model):
    _name = 'employee.attendance'
    _description = 'Employee Attendance Model'

    machine_id = fields.Integer(string="Machine Id")
    user_id = fields.Integer(string="Machine User Id")
    check_in = fields.Datetime(string="Check In", default=fields.Datetime.now)
    check_out = fields.Datetime(string="Check Out")
    name = fields.Char(string="Employee Name", compute="_get_employee_name")
    address_id = fields.Many2one('res.partner', string='Working Address')
    process_flag = fields.Boolean(string='Process Flag')
    user_name = fields.Char(string="User Name")

    def _get_employee_name(self):
        for rec in self:
            # rec.name = 'Minhas'
            try:
                ls = rec.env['hr.employee'].search([('device_id', '=', rec.user_id)])
                rec.name = ls.name
                # print(ls.name)
            except Exception as e:
                rec.name = None
                # print(e)

    @api.model
    def get_attendance(self):
        tot = self.env['employee.attendance'].search([('process_flag', '=', False)],
                                                     order='id asc')
        # print(tot)
        date_only = False
        for rec in tot:

            # check if employee exists (Create if doesn't) (START)

            employee_id = self.env['hr.employee'].search([('device_id', '=', rec.user_id)])
            if not employee_id:
                employee_id = self.env['hr.employee'].create(
                    {'device_id': rec.user_id, 'name': rec.user_name, 'address_id': self.address_id.id, 'active': True})

            # check if employee exists (Create if doesn't) (END)
            print(employee_id.name, rec.check_in, rec.check_out)
            if rec.check_in:
                date_only = rec.check_in
                date_only = date_only.date()
            if rec.check_out:
                date_only = rec.check_out
                date_only = date_only.date()
            # print(date_only)
            # if employee_id and  date_only:
            attendance = self.env['hr.attendance'].search(
                [('employee_id', '=', employee_id.id), ('date_only', '=', date_only)])

            # Archive records whose checkouts are not available (START)
            mytime = dt.datetime.strptime('2359', '%H%M').time()
            my_checkout = dt.datetime.combine(date_only, mytime)

            previous_checkout_attendance = self.env['hr.attendance'].search(
                [('employee_id', '=', employee_id.id), ('check_out', '=', False), ('check_in', '!=', False),
                 ('date_only', '!=', date_only)])
            print('previous_checkout', previous_checkout_attendance, previous_checkout_attendance.check_in)
            previous_checkout_attendance.write({
                'check_out': my_checkout,
                'active': False
            })
            # Archive records whose checkouts are not available (END)

            # +++++++++++++++++++++++++> New entry scenario <+++++++++++++++++++++++++++++++

            # simple check out should be processed (START)

            pending_check_out = self.env['hr.attendance'].search(
                [('employee_id', '=', employee_id.id), ('date_only', '=', date_only), ('check_out', '=', False),
                 ('check_in', '!=', False)])

            if rec.check_in and pending_check_out:
                record_ids = self.env['employee.attendance'].search(
                    [('user_id', '=', rec.user_id), ('check_in', '=', rec.check_in)])

                for record in record_ids:
                    record.write({
                        'process_flag': True
                    })

            # simple check out should be processed (END)

            # print(rec.check_in, pending_check_out, attendance)
            if rec.check_in and not pending_check_out and attendance:
                print('Creating another Check In Entry', rec.check_in)

                self.env['hr.attendance'].create({
                    'employee_id': employee_id.id,
                    'check_in': rec.check_in,
                    'date_only': date_only,
                    'active': True
                })

                # Updating record

                record_ids = self.env['employee.attendance'].search(
                    [('user_id', '=', rec.user_id), ('check_in', '=', rec.check_in)])
                for record in record_ids:
                    record.write({
                        'process_flag': True
                    })

                # +++++++++++++++++++++++++> New entry scenario <+++++++++++++++++++++++++++++++

            # print('condition1:', attendance, employee_id.id, rec.check_in)
            # print('condition2:', attendance, rec.check_out)

            if not attendance and employee_id.id and rec.check_in:
                print('creating fresh check in entry')
                self.env['hr.attendance'].create({
                    'employee_id': employee_id.id,
                    'check_in': rec.check_in,
                    'date_only': date_only,
                    'active': True
                })

                # Updating record

                record_ids = self.env['employee.attendance'].search(
                    [('user_id', '=', rec.user_id), ('check_in', '=', rec.check_in)])
                for record in record_ids:
                    record.write({
                        'process_flag': True
                    })

            if attendance and rec.check_out:
                print('check out found!')

                attendance = self.env['hr.attendance'].search(
                    [('employee_id', '=', employee_id.id), ('check_in', '!=', False), ('date_only', '=', date_only)])

                # check out portion
                print(attendance, employee_id.id, date_only)
                # for i in attendance:
                #     print('check_out', i.employee_id.id, i.check_in, date_only)

                if attendance:
                    record = self.env['hr.attendance'].search(
                        [('employee_id', '=', employee_id.id), ('date_only', '=', date_only),
                         ('check_out', '=', False)])
                    record.write({
                        'check_out': rec.check_out
                    })

                    record_ids = self.env['employee.attendance'].search(
                        [('user_id', '=', rec.user_id), ('check_out', '=', rec.check_out)])
                    print(record_ids)
                    for i in record_ids:
                        i.write({
                            'process_flag': True
                        })

        return True

    def machine_attendance(self):
        pass

# -*- coding: utf-8 -*-
{
    'name': "My Hospital",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Assignment module!
    """,

    'author': "Minhas",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base_setup', 'hr_attendance', 'sale', 'base', 'report_xlsx',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'wizard/evaluation_wizard.xml',
        # 'wizard/employee_wizard.xml',
        'views/patient.xml',
        'views/doctor.xml',
        'views/nurse.xml',
        'views/evaluation.xml',
        'views/sale_order_ext.xml',
        'views/department.xml',
        'views/employee.xml',
        'views/task_stage.xml',
        'reports/paperformat.xml',
        'reports/report.xml',
        'reports/add_custom_footer_in_qweb_report.xml',
        'reports/add_custom_header_in_qweb_report.xml',
        'reports/sale_report_inherit.xml',
        'views/templates.xml',
        # 'data/auto.xml',
        # 'data/email_template.xml',
    ],
    'qweb': [
        'static/src/xml/dashboard.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'sequence': -10
}

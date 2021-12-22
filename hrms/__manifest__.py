# -*- coding: utf-8 -*-
{
    'name': "HRMS",

    'summary': """
        HRMS modules that manages all HRMS operations of employees.""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Minhas - Team Galaxy Solutions ITC",
    'website': "https://galaxyitc.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base','base_setup', 'hr_attendance', 'report_xlsx','attendance_report'
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/employee_attendance.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

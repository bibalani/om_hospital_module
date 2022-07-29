# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Hospital Management',
    'version': '2.0.0',
    'category': 'Hospital',
    'author': 'Morteza',
    'summary': 'Hospital Management System',
    'sequence': -100,
    'description': """Hospital Management Module""",
    'depends': ['mail','muk_web_searchpanel','base', 'product','sale','account'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/patient_data.xml',
        'data/appointment_data.xml',
        'wizard/create_appointment_wizard.xml',
        'views/menu.xml','views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/appointment_view.xml',
        'views/doctor_view.xml',
        'views/sale_order_view.xml',
        'views/account_invoice_view.xml',
        'views/lab.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'assets': {},
}

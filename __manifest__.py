# -*- coding: utf-8 -*-
{
    'name': "Internship",

    'summary': """
        Manage your internship program""",

    'description': """
        Internship Management System
        ====================
        Easy-to-use internship management system that allows keeping track of your institution's interns and training activities. 
    """,

    'author': "Achieve Without Borders, Inc.",
    'website': "https://www.achievewithoutborders.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Custom',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'project',
        'hr',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/interns.xml',
        'views/activities.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}
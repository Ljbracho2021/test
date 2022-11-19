# -*- coding: utf-8 -*-
{
    'name': "Solicitud de Becas de Estudio",

    'summary': """
        Gestiona las Solicitudes de Becas""",

    'description': """
        Long description of module's purpose
    """,
    'sequence': 1,
    'author'  : "3Par1 Corp",
    'website' : "http://www.3par1.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'license'     : 'AGPL-3',
    'category'    : 'Application',
    'version'     : '1.0',
    'installable' : True,
    'application' : True,
    'auto_install': True,
    # any module necessary for this one to work correctly
    "depends": ["base"],

    # always loaded
    'data': [  
        'security/beca_groups.xml', 
        'security/ir.model.access.csv',
        'data/data.xml',
 
    #     'report/persona_details.xml',  
    #     'report/report.xml',  

        'views/views.xml',

        'views/estado_view.xml',
        'views/municipio_view.xml',
        'views/parroquia_view.xml',
        'views/planilla_view.xml',
        #'views/candidato_view.xml',
        'views/carrera_view.xml',
        'views/universidad_view.xml',
        

    ],
    # only loaded in demonstration mode
    'demo': ['demo/beca_demo.xml'],
    'qweb': [],
}

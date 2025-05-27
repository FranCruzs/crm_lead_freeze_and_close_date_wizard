{
    'name': 'CRM Custom Date Update',
    'version': '1.0',
    'summary': 'Agrega botón para cambiar fecha de cierre en oportunidades',
    'description': """
        Este módulo agrega un botón en el formulario de CRM Lead que permite 
        cambiar la fecha de cierre mediante un wizard con calendario.
    """,
    'author': 'Tu Nombre',
    'website': 'https://www.tudominio.com',
    'category': 'CRM',
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',  # <-- Añade esta línea
        'views/crm_lead_views.xml',
        'views/date_update_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
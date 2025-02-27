{
    'name':'Estate',
    'installable': True,
    'application': True,
    "depends": [
        "base",
        "web",
    ],
    'data':[ 
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_view_kanban.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tag_view.xml',
        'views/inherited_res_users_model.xml',
        'reports/estate_property_report_action.xml',
        'reports/estate_property_report_template.xml',
        'views/estate_menus.xml',
    ],
    "demo": [
       'deta/estate_demo.xml',
    ],
    
}
from odoo import fields, models

class InheritedModel(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('estate_property', 'seller') 
    # remanning adding domain
    


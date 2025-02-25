from odoo import fields, models
class propertyTag(models.Model):
    _name = 'estate_property_tag'
    _description = 'This is Estate tag table'
    _order = "name"

    name = fields.Char(required = True)
    color = fields.Integer('Color', )
    _sql_constraints = [
        ('check_name', 'UNIQUE (name)',
         'Tag allrady exist')
    ]
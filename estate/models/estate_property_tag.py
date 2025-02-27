from odoo import fields, models
class propertyTag(models.Model):
    _name = 'estate_property_tag'
    _description = 'This is Estate tag table'
    _order = "name"

    name = fields.Char(required = True)
    color = fields.Integer('Color', )
    company_id=fields.Many2one('res.company', string='Company', required=True, index=True, default=lambda self: self.env.company)
    
    _sql_constraints = [
        ('check_name', 'UNIQUE (name)',
         'Tag allrady exist')
    ]
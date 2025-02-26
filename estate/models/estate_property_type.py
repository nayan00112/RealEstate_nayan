from odoo import fields, models, api
class propertyType(models.Model):
    _name = 'estate_property_type'
    _description = 'This is Estate property type table'
    _order = "sequence, name"
    name = fields.Char(required = True)
    property_ids = fields.One2many('estate_property', 'property_type_id')
    sequence = fields.Integer('Sequence')
    offer_ids = fields.One2many('estate_property_offer', 'property_type_id')
    offer_count = fields.Integer(compute='_count_number_of_offers')

    @api.depends('offer_ids')
    def _count_number_of_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ('check_name', 'UNIQUE (name)',
         'Property type allrady exist')
    ]
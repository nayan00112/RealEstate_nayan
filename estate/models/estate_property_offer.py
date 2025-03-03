from odoo import fields, models, api, exceptions
from odoo.tools import date_utils
class propertyOffer(models.Model):
    _name = 'estate_property_offer'
    _description = 'This is Estate offer table'
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False)

    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate_property', required=True)
    validity = fields.Integer(default = 7)
    date_deadline = fields.Date(compute = '_set_deadline', inverse='_set_validity')
    property_type_id = fields.Many2one('estate_property_type', related='property_id.property_type_id', store=True)

    company_id=fields.Many2one('res.company', string='Company', required=True, index=True, default=lambda self: self.env.company)

    @api.depends('validity')
    def _set_deadline(self):
        for record in self:
            record.date_deadline = date_utils.add(fields.Date.today(), days=record.validity)

    def _set_validity(self):
        for record in self:
            record.validity = abs(fields.Date.today() - record.date_deadline).days

    def action_estate_property_offer_uncheckbtn(self):
        for record in self:
            if record.status != 'accepted':
                record.status = 'refused'
            else:
                raise exceptions.UserError('Accepted property cannot be refuse!')
            
    def action_estate_property_offer_checkbtn(self):
        for record in self:
            if record.status != 'refused':
                    
                    
                # if record.property_id.seller:
                #     raise exceptions.UserError('allrady accepted!')
                # else:
                    record.status = 'accepted'
                    record.property_id.state = 'offer_accepted'
                    record.property_id.selling_price = record.price
                    record.property_id.buyers = record.partner_id
            else:
                raise exceptions.UserError('Refused property cannot be accept!')

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
         'The offer price must be positive!')
    ]
    
    def create(self, vals):
        for record in vals:
            if (self.env['estate_property'].browse((record['property_id'])).state == 'new'):
                self.env['estate_property'].browse((record['property_id'])).state = 'offer_received'
        for record in vals:
            if ( self.env['estate_property'].browse((record['property_id'])).best_price > record['price']):
                raise exceptions.UserError('Property must be heigher then '+str(self.env['estate_property'].browse((record['property_id'])).best_price))
                
        return super().create(vals)


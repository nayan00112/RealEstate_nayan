from odoo import fields, models, api, exceptions

class Property(models.Model):
    _name = 'estate_property'
    _description = 'Table for estate app'
    _order = "id desc"
    
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default= fields.date_utils.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area= fields.Integer()
    facades = fields.Boolean()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
    active = fields.Boolean()
    state = fields.Selection([
        ('new','New'), ('offer_received', 'Offer Received'), ('offer_accepted' ,'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')
    ], default='new')
    buyers = fields.Many2one('res.partner', name='Buyers', copy=False)
    seller = fields.Many2one('res.users', name='Seller', default=lambda self: self.env.user)
    property_type_id = fields.Many2one('estate_property_type', string='Property Type')
    tag_ids = fields.Many2many("estate_property_tag", string="Tags")
    offer_ids = fields.One2many("estate_property_offer", "property_id", string="Offer ids")
    total_area = fields.Float(compute="_total_area")
    best_price = fields.Float(compute='_best_price', default=0, store=True)

    @api.depends('living_area', 'garden_area')
    def _total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _best_price(self):
        for record in self:
            try:
                record.best_price = max(record.offer_ids.mapped("price"))
            except: 
                record.best_price = 0 # i think there is not offers then 0.

    @api.onchange('garden')
    def _setgardeninformation(self):
        for record in self:
            if record.garden == True:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = ''

    def action_estate_property_sold(self):
        for record in self:
            if record.state != 'cancelled':
                record.state = 'sold'
            else:
                raise exceptions.UserError('Cancelled property cannot be sold!')
            
    def action_estate_property_cancle(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'cancelled'
            else:
                raise exceptions.UserError('Sold property cannot be cancelled!')

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The expected price must be positive!'),

        ('check_selling_price', 'CHECK(selling_price > 0)',
         'The selling price must be positive!')
    ]

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            # if abs(record.selling_price - record.expected_price)/record.expected_price < 1-0.9 and record.selling_price > 0:
            if record.selling_price > 0 and record.selling_price < (0.9 * record.expected_price):
                raise exceptions.UserError('selling price cannot be lower than 90% of the expected priceed!')

    @api.ondelete(at_uninstall=False)
    def _prevent_delete_state_is_not_new_or_cancelled(self):
        for record in self:
            if record.state not in ['cancelled', 'new']:
                raise exceptions.UserError('Only new and cancelled property can be delete')
        
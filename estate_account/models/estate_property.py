from odoo import fields, models, Command

class inheritad_account_module(models.Model):
    _inherit = 'estate_property'

    def action_estate_property_sold(self):
        for record in self:
            property_details_dict = {
                'partner_id' :record.buyers.id,
                'move_type': 'out_invoice',
                'name':super().name,
                'invoice_line_ids': [
                    Command.create({
                        'name':super().name,
                        'price_unit': super().selling_price,
                        'quantity': 1,
                    }),
                    Command.create({
                        'name':'6%',
                        'price_unit': super().selling_price *0.06,
                        'quantity': 1,
                    }),
                    Command.create({
                        'name':'Additional charge',
                        'price_unit': 100,
                        'quantity': 1,
                    })
                    ]
            }

        self.env['account.move'].create(property_details_dict)
        return super().action_estate_property_sold()

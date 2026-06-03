from odoo import fields, models


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    spx_cod_currency_id = fields.Many2one(
        'res.currency',
        string='COD Currency',
        required=True,
        default=lambda self: self.env.company.currency_id,
        help='Currency used for the Cash on Delivery fee and order amount rules.'
    )

    spx_cod_enabled = fields.Boolean(
        string='Enable SPX Cash on Delivery Rules',
        help='Enable custom Cash on Delivery rules for this payment provider.'
    )

    spx_cod_fee_amount = fields.Monetary(
        string='COD Fee',
        currency_field='spx_cod_currency_id',
        help='Fixed fee to charge when Cash on Delivery is selected.'
    )

    spx_cod_min_amount = fields.Monetary(
        string='Minimum Order Amount',
        currency_field='spx_cod_currency_id',
        help='Minimum order total required for Cash on Delivery. Leave 0 for no minimum.'
    )

    spx_cod_max_amount = fields.Monetary(
        string='Maximum Order Amount',
        currency_field='spx_cod_currency_id',
        help='Maximum order total allowed for Cash on Delivery. Leave 0 for no maximum.'
    )

    spx_cod_message = fields.Char(
        string='Checkout Message',
        default='Cash on Delivery is available for eligible orders.',
        help='Message to show customers when Cash on Delivery is available.'
    )

    spx_cod_country_ids = fields.Many2many(
        'res.country',
        'spx_cod_provider_country_rel',
        'provider_id',
        'country_id',
        string='Allowed Countries',
        help='Restrict COD to selected shipping countries. Leave empty to allow all countries.'
    )

    spx_cod_excluded_product_ids = fields.Many2many(
        'product.template',
        'spx_cod_provider_product_rel',
        'provider_id',
        'product_tmpl_id',
        string='Excluded Products',
        help='Products that should not allow Cash on Delivery.'
    )

    spx_cod_excluded_partner_ids = fields.Many2many(
        'res.partner',
        'spx_cod_provider_partner_rel',
        'provider_id',
        'partner_id',
        string='Excluded Customers',
        help='Customers that should not be allowed to use Cash on Delivery.'
    )

    def spx_cod_is_order_eligible(self, order):
        self.ensure_one()
        if not self.spx_cod_enabled:
            return False, 'Cash on Delivery rules are disabled.'

        amount_total = order.amount_total or 0.0

        if self.spx_cod_min_amount and amount_total < self.spx_cod_min_amount:
            return False, 'Order amount is below the minimum allowed for Cash on Delivery.'

        if self.spx_cod_max_amount and amount_total > self.spx_cod_max_amount:
            return False, 'Order amount is above the maximum allowed for Cash on Delivery.'

        shipping_partner = order.partner_shipping_id or order.partner_id
        if self.spx_cod_country_ids and shipping_partner.country_id not in self.spx_cod_country_ids:
            return False, 'Cash on Delivery is not available for the selected country.'

        if order.partner_id in self.spx_cod_excluded_partner_ids:
            return False, 'Cash on Delivery is not available for this customer.'

        excluded_templates = self.spx_cod_excluded_product_ids
        order_templates = order.order_line.filtered(lambda line: not line.display_type).product_id.product_tmpl_id
        if excluded_templates and any(tmpl in excluded_templates for tmpl in order_templates):
            return False, 'Cash on Delivery is not available for one or more products in the cart.'

        return True, self.spx_cod_message or 'Cash on Delivery is available.'

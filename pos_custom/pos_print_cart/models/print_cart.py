from odoo import models, fields, api

import odoo.addons.decimal_precision as dp

class CartItem(models.Model):
	_inherit = 'pos.order'

	@api.model
	def get_orderline_details(self):

		orders = self.env['pos.order'].sudo()
		print orders

		user_currency = self.env.user.company_id.currency_id

		total = 0.0
		products_sold = {}
		taxes = {}
		for order in orders:
			if user_currency != order.pricelist_id.currency_id:
				total += order.pricelist_id.currency_id.compute(order.amount_total, user_currency)
			else:
				total += order.amount_total
			currency = order.session_id.currency_id
			print currency
			print '>>>>>>>>'

			for line in order.lines:
				key = (line.product_id, line.price_unit, line.discount)
				products_sold.setdefault(key, 0.0)
				products_sold[key] += line.qty
				print '<<<<<<<<'

				if line.tax_ids_after_fiscal_position:
					line_taxes = line.tax_ids_after_fiscal_position.compute_all(line.price_unit * (1-(line.discount or 0.0)/100.0), currency, line.qty, product=line.product_id, partner=line.order_id.partner_id or False)
					for tax in line_taxes['taxes']:
						taxes.setdefault(tax['id'], {'name': tax['name'], 'total':0.0})
						taxes[tax['id']]['total'] += tax['amount']

		

		return {
			'currency_precision': user_currency.decimal_places,
			'total_paid': user_currency.round(total),
			'company_name': self.env.user.company_id.name,
			'taxes': taxes.values(),
			'products': sorted([{
				'product_id': product.id,
				'product_name': product.name,
				'code': product.default_code,
				'quantity': qty,
				'price_unit': price_unit,
				'discount': discount,
				'uom': product.uom_id.name
			} for (product, price_unit, discount), qty in products_sold.items()], key=lambda l: l['product_name'])
		}

	@api.multi
	def render_html(self, docids, data=None):
		data = dict(data or {})
		# configs = self.env['pos.config'].browse(data['config_ids'])
		data.update(self.get_orderline_details())
		return self.env['report'].get_action([], 'point_of_sale.report_saledetails', data=data)


	

	# 	
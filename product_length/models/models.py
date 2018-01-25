from odoo import api, fields, models


class ProductLength(models.Model):
	_inherit = 'product.product'

	length = fields.Float(string='Product Length', required=True, )
	order_line_id = fields.One2many('sale.order.line', 'product_id')




class SalesOrderline(models.Model):
	_inherit='sale.order.line'


	@api.depends('total_length', 'discount', 'price_unit', 'tax_id')
	def _compute_amount(self):
		res = super(SalesOrderline, self)._compute_amount()
		for line in self:
			print '))))))))))))))))))', line
			print '(((((((((', line.total_length, type(line.total_length)
			total_length = float(line.total_length)
			print '------------', total_length
			price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
			taxes = line.tax_id.compute_all(price, line.order_id.currency_id, quantity=total_length, product=line.product_id, partner=line.order_id.partner_shipping_id)
			
			line.update({
				'price_tax': taxes['total_included'] - taxes['total_excluded'],
				'price_total': taxes['total_included'],
				'price_subtotal': taxes['total_excluded'],
			})
		

	@api.depends('product_id', 'product_uom_qty',)
	def _total_length(self):
		for line in self:
			if line.product_id:
				line.length = line.product_id.length
				line.total_length = line.product_uom_qty * line.length


		

	length = fields.Float(related='product_id.length')
	total_length = fields.Char(string='Total length', compute='_total_length')


	@api.onchange('product_uom_qty', 'length')
	def _check_total_length(self):
		for m in self:
			print '>>>>>>>', m.product_id
			if m.length and m.product_uom_qty:
				m.product_id.length = m.length
				m.total_length = m.product_uom_qty * m.length

	@api.multi
	def _prepare_invoice_line(self, qty):
		res = super(SalesOrderline, self)._prepare_invoice_line(qty)
		print '---------------', res
		res['length'] = self.length
		res['total_length'] = self.total_length

		print '??????????????', res

		return res


class AccountInvoiceLine(models.Model):
	_inherit = 'account.invoice.line'

	@api.depends('length', 'quantity',)
	def _total_length(self):
		for line in self:
			if line.product_id:
				line.length = line.product_id.length
				line.total_length = line.quantity * line.length


	@api.one
	@api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'total_length',
		'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
		'invoice_id.date_invoice', 'invoice_id.date')
	def _compute_price(self):
		res = super(AccountInvoiceLine, self)._compute_price()
		currency = self.invoice_id and self.invoice_id.currency_id or None
		price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
		taxes = False
		total_length = float(self.total_length)
		if self.invoice_line_tax_ids:
			taxes = self.invoice_line_tax_ids.compute_all(price, currency, total_length, product=self.product_id, partner=self.invoice_id.partner_id)
		self.price_subtotal = price_subtotal_signed = taxes['total_excluded'] if taxes else total_length * price
		if self.invoice_id.currency_id and self.invoice_id.company_id and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id:
			price_subtotal_signed = self.invoice_id.currency_id.with_context(date=self.invoice_id._get_currency_rate_date()).compute(price_subtotal_signed, self.invoice_id.company_id.currency_id)
		sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
		self.price_subtotal_signed = price_subtotal_signed * sign


	# sale_lines = fields.Many2many('sale.order.line', 'sale_order_line_invoice_rel', 'invoice_line_id', 'order_line_id')
	length = fields.Float(string='Length', related='product_id.length')
	total_length = fields.Float(string='Total Length', compute='_total_length')


	

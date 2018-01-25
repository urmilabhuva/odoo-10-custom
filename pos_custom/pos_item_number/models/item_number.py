from odoo import models, fields, api

class PosItem(models.Model):
	_inherit = 'pos.order.line'
		
	sequence = fields.Integer('Sequence')
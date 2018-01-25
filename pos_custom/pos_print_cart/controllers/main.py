import json
import logging
import werkzeug.utils

from odoo import http
from odoo.http import request

from odoo.http import Response

_logger = logging.getLogger(__name__)



class OrderlineController(http.Controller):

	@http.route('/pos/online_details_report', type='json', auth='user', website=True)
	def print_orderline_details(self, **kw):
		# cr, context, pool, uid = request.cr, request.context, request.registry, request.uid
		input_data = kw.get('input_data')
		print input_data
		print '>>>>>>>>>>>'

		return {

        'type': 'ir.actions.report.xml',

        'report_name': 'pos_print_cart.report_orderlines',

        'datas': input_data,

    }
    	
		# return self.request.registry['report'].get_action([], 'pos_print_cart.report_orderlines', data=input_data, context=request.context)
		
		




odoo.define('pos_print_cart.cart', function (require) {
"use strict";

console.log('-------------------------');
alert('helllo------------');

var core = require('web.core');
var QWeb = core.qweb;

var screens = require('point_of_sale.screens');
var ActionpadWidget = screens.ActionpadWidget.prototype;
var module = require('point_of_sale.models');
var Order = module.Order.prototype;

var ajax = require('web.ajax');

module.Order = module.Order.extend({

	orderline_for_printing: function(){
		var orderlines = [];
        var self = this;

        this.orderlines.each(function(orderline){
            orderlines.push(orderline.export_for_printing());
        });

        
        var client  = this.get('client');
        var cashier = this.pos.cashier || this.pos.user;
        var company = this.pos.company;
        var shop    = this.pos.shop;
        var date    = new Date();


        var receipt = {
            orderlines: orderlines,
            subtotal: this.get_subtotal(),
            total_with_tax: this.get_total_with_tax(),
            total_without_tax: this.get_total_without_tax(),
            total_tax: this.get_total_tax(),
            total_paid: this.get_total_paid(),
            total_discount: this.get_total_discount(),
            tax_details: this.get_tax_details(),
            change: this.get_change(),
            name : this.get_name(),
            client: client ? client.name : null ,
            invoice_id: null,   //TODO
            cashier: cashier ? cashier.name : null,
            precision: {
                price: 2,
                money: 2,
                quantity: 3,
            },
            date: { 
                year: date.getFullYear(), 
                month: date.getMonth(), 
                date: date.getDate(),       // day of the month 
                day: date.getDay(),         // day of the week 
                hour: date.getHours(), 
                minute: date.getMinutes() ,
                isostring: date.toISOString(),
                localestring: date.toLocaleString(),
            }, 
            company:{
                email: company.email,
                website: company.website,
                company_registry: company.company_registry,
                contact_address: company.partner_id[1], 
                vat: company.vat,
                name: company.name,
                phone: company.phone,
                logo:  this.pos.company_logo_base64,
            },
            shop:{
                name: shop.name,
            },
            currency: this.pos.currency,
        };
        
        return receipt;

	},

});


	
screens.ActionpadWidget = screens.ActionpadWidget.include({
	print: function() {
		
        var receipt = this.pos.get_order().orderline_for_printing();
        
        // console.log(receipt);
        return receipt;

       
    },


	renderElement: function() {
        var self = this;
        this._super();

        this.$('.print').click(function(){
            alert('>>>>>>>');
            var receipt = self.print();
            console.log(receipt);
            ajax.jsonRpc("/pos/online_details_report", 'call', {
                    'input_data': JSON.stringify(receipt),
                });
            });

        



    },


});




});
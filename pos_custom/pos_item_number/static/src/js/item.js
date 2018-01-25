odoo.define('pos_item_number.item', function (require) {
"use strict";


var module = require('point_of_sale.models');
var screens = require('point_of_sale.screens');

var Order = module.Order.prototype;
var Orderline = module.Orderline.prototype;
var OrderWidget = screens.OrderWidget.prototype;



module.Order = module.Order.extend({
	

    add_product: function(product, options){
        if(this._printed){
            this.destroy();
            return this.pos.get_order().add_product(product, options);
        }
        this.assert_editable();
        options = options || {};
        var attr = JSON.parse(JSON.stringify(product));
        attr.pos = this.pos;
        attr.order = this;
        var line = new module.Orderline({}, {pos: this.pos, order: this, product: product});
        if(options.quantity !== undefined){
            line.set_quantity(options.quantity);
        }

        if(options.price !== undefined){
            line.set_unit_price(options.price);
        }

        //To substract from the unit price the included taxes mapped by the fiscal position
        this.fix_tax_included_price(line);

        if(options.discount !== undefined){
            line.set_discount(options.discount);
        }

        alert('sequence added');

        var all_lines = this.get_orderlines();
        var max_sequence = 0;
        for (var i = all_lines.length - 1; i >= 0; i--) {
            max_sequence= Math.max(all_lines[i].sequence, max_sequence);
        }

        line.sequence = max_sequence + 1

        if(options.extras !== undefined){
            for (var prop in options.extras) { 
                line[prop] = options.extras[prop];
            }
        }

        var last_orderline = this.get_last_orderline();
        if( last_orderline && last_orderline.can_be_merged_with(line) && options.merge !== false){
            last_orderline.merge(line);
        }else{
            this.orderlines.add(line);
        }
        this.select_orderline(this.get_last_orderline());

        if(line.has_product_lot){
            this.display_lot_popup();
        }
    },


    rearrange_sequence_orderline: function( line ){
        var all_lines = this.get_orderlines();
        for (var i = all_lines.length - 1; i >= 0; i--) {
            if(all_lines[i].sequence>line.sequence){
                all_lines[i].sequence = all_lines[i].sequence-1;
            }
        }
    },

});

module.Orderline = module.Orderline.extend({


    init_from_JSON: function(json) {
        Orderline.init_from_JSON.call(this, json);
        this.sequence = json.sequence;
    },
    get_sequence_str: function(){
        return this.sequence;
    },
    export_as_JSON: function() {
        var ret=Orderline.export_as_JSON.call(this);
        ret.sequence = this.sequence;
        return ret;
    },
    set_quantity: function(quantity){
        if(quantity === 'remove'){
            this.order.rearrange_sequence_orderline(this);
        }
        Orderline.set_quantity.call(this, quantity);
    },

});


screens.OrderWidget.include({
    remove_orderline: function(order_line){
        this._super(order_line);
        var all_lines = this.pos.get_order().get_orderlines();
        for(var i = 0; i < all_lines.length; i++){
            this.rerender_orderline(all_lines[i]);
        }
    },
});

});
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
class tai_sale(osv.osv):
    _inherit = 'sale.order'

    def count(self,cr,uid,ids,id_fee,arg,context=None):
        res ={}

        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = 0
            kq = 0
            for fee in obj.id_fee:
                kq += fee.amount
            res[obj.id] = kq
        return res

    def _amount_all_wrapper(self, cr, uid, ids, field_name, arg, context=None):
        """ Wrapper because of direct method passing as parameter for function fields """
        return self._amount_all(cr, uid, ids, field_name, arg, context=context)
    def _get_order(self, cr, uid, ids, context=None):
        line_obj = self.pool.get('sale.order.line')
        return list(set(line['order_id'] for line in line_obj.read(
            cr, uid, ids, ['order_id'], load='_classic_write', context=context)))
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'amount_untaxed': 0.0,
                'amount_tax': 0.0,
                'amount_total': 0.0,
            }
            val = val1 = 0.0
            cur = order.pricelist_id.currency_id
            for line in order.order_line:
                val1 += line.price_subtotal
                val += self._amount_line_tax(cr, uid, line, context=context)
            res[order.id]['amount_tax'] = cur_obj.round(cr, uid, cur, val)
            res[order.id]['amount_untaxed'] = cur_obj.round(cr, uid, cur, val1)
            res[order.id]['amount_total'] = res[order.id]['amount_untaxed'] + res[order.id]['amount_tax'] + order.amount_fee
        return res
    _columns = {
        'test' : fields.integer('test'),
        'id_fee' : fields.one2many('fee','id_tai',string = 'order_fee'),
        'amount_fee': fields.function(count, string='Fee amount', type='float'),
        'amount_total': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='Total',
                                        store={
                                            'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line','id_fee'], 10),
                                            'sale.order.line': (
                                            _get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
                                        },
                                        multi='sums', help="The total amount."),
    }
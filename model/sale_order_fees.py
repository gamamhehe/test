from openerp.osv import fields,osv
class fees(osv.osv):
    _name = 'fee'
    _columns = {
        'fee' : fields.char('fee'),
        'amount' : fields.integer('amount'),
        'id_tai' : fields.many2one('tai.sale',string = 'Fee')
    }

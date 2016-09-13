from openerp.osv import fields,osv
class fees(osv.osv):
    _name = 'fee'
    _columns = {
        'fee' : fields.char('fee'),
        'amount' : fields.integer('amount'),
<<<<<<< HEAD
        'id_tai' : fields.many2one('sale.order',string = 'Fee')
=======
        'id_tai' : fields.many2one('tai.sale',string = 'Fee')
>>>>>>> 90521546acbbe5f0718c961c4f22201c22141967
    }

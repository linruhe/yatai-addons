
from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _
import xlrd,base64
from openerp.osv import fields, osv
import datetime
import time

class membercard_import_wizard(osv.osv_memory):

    _name = 'membercard.import.wizard'
    _description = 'Wizard that import membercards'
    _columns = {
        'choose_date': fields.boolean('Choose a Particular Date'),
        'select_excel': fields.binary('Select a Excel'),
        'date': fields.datetime('Date', required=True),
    }
    _defaults = {
        'date': fields.datetime.now,
        'choose_date': True,
    }


    def open_table(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.read(cr, uid, ids, context=context)[0]
        ctx = context.copy()
        ctx['history_date'] = data['date']
        #ctx['search_default_group_by_product'] = True
        #ctx['search_default_group_by_location'] = True
        xlsfile = data['select_excel']
        excel = xlrd.open_workbook(file_contents=base64.decodestring(xlsfile))
        date_import=time.strftime('%Y-%m-%d %H:%M:%S')       
        sheet_list = excel.sheet_names()
        for shn in sheet_list:
            table = excel.sheet_by_name(shn)
            for lin in range(table.nrows):
                if  lin != 0 :
                    val = {
                        "date_sale" : str(datetime.date.fromordinal(693594+int(table.row_values(lin)[0]))),
                        "name" : int(table.row_values(lin)[1]),
                        "ref" : table.row_values(lin)[2],
                        "mobile" : str(table.row_values(lin)[3]).split(".")[0],
                        "village" : table.row_values(lin)[4],
                        "housenumber" : table.row_values(lin)[5],
                        "state" : table.row_values(lin)[12],
                        "city" : table.row_values(lin)[13],
                        "store" : table.row_values(lin)[7],
                        "category" : table.row_values(lin)[15],
                        "brand" : table.row_values(lin)[6],
                        "team" : table.row_values(lin)[16],
                        "saleperson" : table.row_values(lin)[8],
                        "area" : table.row_values(lin)[9],
                        "progress" : table.row_values(lin)[10],
                        "note" : table.row_values(lin)[11],    
                        "campaign" : table.row_values(lin)[14],
                        "date_import" : data['date'],                                                                        
                    }
                    card_id=self.pool.get('yatai.member.card').create(cr, uid,val,context=context)
                                          
        return {
            'domain': "[('date_import', '=', '" + data['date'] + "')]",
            'name': _('Imported'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'yatai.member.card',
            'type': 'ir.actions.act_window',
            'context': ctx,
        }
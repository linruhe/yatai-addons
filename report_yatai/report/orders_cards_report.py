# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import tools
from openerp.osv import fields, osv

class orders_cards_report(osv.osv):
    _name = "orders.cards.report"
    _description = "Orders cards Statistics"
    _auto = False
    _rec_name = 'date_day'

    _columns = {
        'date_day': fields.char('Date day', readonly=True),
        'cat': fields.char('Cat', size=64, readonly=True),
        'state': fields.char('state', size=64, readonly=True), 
        'user_import_id': fields.many2one('res.users', 'Import User', readonly=True),
        'nbr': fields.integer('nbr', readonly=True),
    }
    _order = 'date_day desc'

    def init(self, cr):

        """
            CRM Lead Report
            @param cr: the current row, from the database cursor
        """
        tools.drop_view_if_exists(cr, 'orders_cards_report')
        cr.execute("""
            CREATE OR REPLACE VIEW orders_cards_report AS (
                select id as id, '\xe3\x80\x90\xe5\x94\xae\xe5\x8d\xa1\xe3\x80\x91'  as cat , p.state as state , p.user_id as user_import_id, to_char(p.date_sale , 'yyyy-mm-dd') as date_day, count(*) as nbr from yatai_member_card p  where p.name is not null group by id,date_import 
                UNION all
                select c.id as id,'\xe3\x80\x90\xe8\xae\xa2\xe5\x8d\x95\xe3\x80\x91' as cat ,p.state as state ,c.user_id as user_import_id,  to_char(c.date_order , 'yyyy-mm-dd') as date_day, count(*) as nbr from yatai_campaign_order  c  left join yatai_member_card p  on (c.vcard_id=p.id) group by c.id,c.date_import,p.state
            )""")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

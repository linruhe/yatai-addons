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

class campaign_order_report(osv.osv):
    _name = "campaign.order.report"
    _description = "Campaign order Statistics"
    _auto = False
    _rec_name = 'date_order'

    _columns = {
        'date_order': fields.datetime('Date Order', readonly=True),
        'nbr': fields.integer('\xe8\xae\xa2\xe5\x8d\x95\xe6\x95\xb0\xe9\x87\x8f', readonly=True),
        'order_brand': fields.char('Order Brand', size=64, readonly=True),
        'card_brand': fields.char('Card Brand', size=64, readonly=True),
        'state': fields.char('state', size=64, readonly=True), 
        'user_card_import_id': fields.many2one('res.users', 'Import User', readonly=True),
        'user_order_import_id': fields.many2one('res.users', 'Import User', readonly=True),
        'money': fields.float('\xe4\xb8\x8b\xe8\xae\xa2\xe9\x87\x91\xe9\xa2\x9d', digits=(16,2), readonly=True),
        'city': fields.char('City', size=64, readonly=True),
        'campaign': fields.char('Campaign', size=64, readonly=True),
    }
    _order = 'date_order desc'

    def _select(self):
        select_str = """
             SELECT c.id as id ,
                    c.date_order as date_order,
                    count(*) as nbr,
                    c.brand as order_brand,
                    c.user_id as user_order_import_id,
                    sum(c.money) as money,
                    p.state as state,
                    p.city as city,
                    p.campaign as campaign,
                    p.user_id as user_card_import_id,
                    p.brand as card_brand
        """
        return select_str

    def _from(self):
        from_str = """
               yatai_campaign_order c
                  left join yatai_member_card p  on (c.vcard_id=p.id)
        """
        return from_str

    def _group_by(self):
        group_by_str = """ GROUP BY
                c.id,
                c.brand,
                c.date_order, 
                p.brand,
                p.user_id,
                c.user_id,
                p.state,
				p.city,
				p.campaign
        """
        return group_by_str

    def init(self, cr):
        #self._table = campaign_order_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM  %s 
            %s
            )""" % (self._table, self._select(), self._from(), self._group_by()))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

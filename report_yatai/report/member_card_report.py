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

class member_card_report(osv.osv):
    _name = "member.card.report"
    _description = "Member card Statistics"
    _auto = False
    _rec_name = 'date_sale'

    _columns = {
        'date_sale': fields.date('\xe5\x94\xae\xe5\x8d\xa1\xe6\x97\xa5\xe6\x9c\x9f', readonly=True),
        'date_sale_day': fields.char('Sale Date (day)', size=64, readonly=True),
        'date_sale_month': fields.char('Sale Date (month)', size=64, readonly=True),
        'village': fields.char('Village', size=64, readonly=True),
        'brand': fields.char('Brand', size=64, readonly=True),
        'name': fields.char('Vip Card', size=64, readonly=True),
        'team': fields.char('Team', size=64, readonly=True),
        'city': fields.char('city', size=64, readonly=True),
        'state': fields.char('state', size=64, readonly=True),        
        'saleperson': fields.char(' Sale Person', size=64, readonly=True),
        'user_id': fields.many2one('res.users', 'Import User', readonly=True),
        'nbr': fields.integer('\xe5\x94\xae\xe5\x8d\xa1\xe6\x95\xb0', readonly=True),
        'checkin': fields.integer('\xe7\xad\xbe\xe5\x88\xb0\xe6\x95\xb0', readonly=True),
        'checkin_rate': fields.float('\xe7\xad\xbe\xe5\x88\xb0\xe7\x8e\x87(%)', digits=(16,2), readonly=True,group_operator='avg'),
        'card_dealed': fields.integer('\xe7\xad\xbe\xe5\x8d\x95\xe6\x88\xb7',  readonly=True),
        'card_orders': fields.integer('\xe4\xb8\x8b\xe5\xae\x9a\xe5\x8d\x95\xe6\x95\xb0',  readonly=True),
        'accurate_rate': fields.float('\xe7\xb2\xbe\xe5\x87\x86\xe7\x8e\x87(%)', digits=(16,2), readonly=True,group_operator='avg'),
        'card_brand_orders': fields.integer('\xe8\x87\xaa\xe7\xad\xbe\xe5\x8d\x95',  readonly=True),
        'card_ontribution_orders': fields.integer('\xe8\xb4\xa1\xe7\x8c\xae\xe5\x8d\x95',  readonly=True),
        'orders_per_card_dealed': fields.float('\xe5\x9d\x87\xe5\x8d\x95', digits=(16,2), readonly=True,group_operator='avg'),
        'campaign': fields.char('Campaign', size=64, readonly=True),
                

    }
    _order = 'date_sale desc'

    def _select(self):
        select_str = """
             SELECT p.date_sale as date_sale,
                    to_char(p.date_sale , 'yyyy-mm-dd') as date_sale_day,
                    to_char(p.date_sale , 'yyyy-mm') as date_sale_month,
                    id as id,
                    p.city as city,
                    p.state as state,
                    p.name as name,
                    p.village as village,
                    p.brand as brand,
                    p.team as team,
                    p.saleperson as saleperson,
                    p.campaign as campaign,
                    p.user_id as user_id,
                    count(p.name) as nbr,
                    sum(case when p.checkin=True then 1 else 0 end) as checkin,
                    sum(case when p.checkin=True then 1 else 0 end)/count(p.name)*100.00 as checkin_rate,
                    sum(case when card_orders>0 then 1 else 0 end) as card_dealed,
                    sum(card_orders) as card_orders,
                    (sum(case when card_orders>0 then 1 else 0 end)/count(*))*100.00 as accurate_rate,
                    sum(p.card_brand_orders) as card_brand_orders,
                    sum(card_orders)-sum(p.card_brand_orders) as card_ontribution_orders,
                    (case when sum(case when card_orders>0 then 1 else 0 end)= 0 then null else sum(card_orders)/sum(case when card_orders>0 then 1.00 else 0 end) end) as orders_per_card_dealed
        """
        return select_str

    def _from(self):
        from_str = """
               yatai_member_card p where p.name is not null
        """
        return from_str

    def _group_by(self):
        group_by_str = """ GROUP BY
                id,
                p.team,
                p.brand,
                p.city,
                p.state,
                p.saleperson,
                p.campaign,
                p.date_sale,
                p.village         
        """
        return group_by_str

    def init(self, cr):
        # self._table = sale_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM  %s 
            %s
            )""" % (self._table, self._select(), self._from(), self._group_by()))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

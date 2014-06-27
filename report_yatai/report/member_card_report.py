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
        'date_sale': fields.date('Date Sale', readonly=True),
        'nbr': fields.integer('# Total Cards', readonly=True),
        'village': fields.char('Village', size=64, readonly=True),
        'brand': fields.char(' Brand', size=64, readonly=True),
        'team': fields.char(' Team', size=64, readonly=True),
        'saleperson': fields.char(' Sale Person', size=64, readonly=True),
        'checkin': fields.integer('# Check In', readonly=True),
        'checkin_rate': fields.float('Check IN%', digits=(16,2), readonly=True,group_operator='avg'),
    }
    _order = 'date_sale desc'

    def _select(self):
        select_str = """
             SELECT p.date_sale as date_sale,
                    count(*) as nbr,
                    id as id,
                    p.city as city,
                    p.name as name,
                    p.village as village,
                    p.brand as brand,
                    p.team as team,
                    p.saleperson as saleperson,
                    sum(case when checkin=True then 1 else 0 end) as checkin,
                    avg(checkin_rate) as checkin_rate
        """
        return select_str

    def _from(self):
        from_str = """
               yatai_member_card p
        """
        return from_str

    def _group_by(self):
        group_by_str = """ GROUP BY
                id,
                p.team,
                p.brand,
                p.saleperson,
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

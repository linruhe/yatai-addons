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
        'date_order': fields.date('Date Order', readonly=True),
        'nbr': fields.integer('# Total Orders', readonly=True),
        'brand': fields.char(' Brand', size=64, readonly=True),
        'money': fields.float('Money', digits=(16,2), readonly=True),
    }
    _order = 'date_order desc'

    def _select(self):
        select_str = """
             SELECT id as id ,
                    c.date_order as date_order,
                    count(*) as nbr,
                    c.brand as brand,
                    sum(c.money) as money
        """
        return select_str

    def _from(self):
        from_str = """
               yatai_campaign_order c
        """
        return from_str

    def _group_by(self):
        group_by_str = """ GROUP BY
                id,
                c.brand,
                c.date_order    
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

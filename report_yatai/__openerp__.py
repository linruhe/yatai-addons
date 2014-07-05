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

{
    'name': 'Yatai Report',
    'version': '1.0',
    'category': 'Sales Management',
    'sequence': 14,
    'summary': 'report',
    'description': """
The Dashboard for the Sales Manager will include
------------------------------------------------
* My Quotations
* Monthly Turnover (Graph)
    """,
    'author': 'lihaihe',
    'website': 'http://www.b-honest.com',
    'images': [],
    'depends': [],
    'data': [
    	 'member_card_view.xml',
    	 'campaign_oder.xml',
    	 'report/member_card_report.xml',
    	 'report/campaign_oder_report.xml',
    	 'report/orders_cards_report.xml',
    ],
    'demo': [],
    'test': [
  
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

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

from openerp.osv import fields,osv
from openerp.tools.translate import _

class yatai_campaign_order(osv.osv):
    '''campaign order'''
    _name = "yatai.campaign.order"
    _order = 'date_import desc'

    _columns = {
        'name': fields.char('#Receipt', size=64),
        'brand': fields.char('Brand Ordered', size=64),
        'campaign': fields.char('Campaign', size=64),
        'money': fields.float('money', digits=(16,2)),  
        'vcard_id': fields.many2one('yatai.member.card', 'Vip Card', select=True),
        'date_order': fields.datetime('Date Order'),
        'date_import': fields.datetime('Date Import'),
        'user_id': fields.many2one('res.users', 'Import User', select=True, track_visibility='onchange'),

    }
    _sql_constraints = [
        ('name_key', 'UNIQUE (name)',  'You can not have two id with the same order !')
    ]

    _defaults = {
        'date_import': fields.datetime.now,
        'user_id': lambda obj, cr, uid, context: uid,
    }
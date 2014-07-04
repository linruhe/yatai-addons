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

class yatai_member_card(osv.osv):
    '''Member Card'''
    _name = "yatai.member.card"
    _order = 'date_import desc'
    
    def _checkin_rate(self, cursor, user, ids, name, arg, context=None):
        res={}
        for partner in self.browse(cursor, user, ids, context=context):
            if partner.checkin :
                res[partner.id]=100.00
            else :
                res[partner.id]=0.00        
        return res

    def _card_orders_total(self, cursor, user, ids, name, arg, context=None):
        res={}
        for partner in self.browse(cursor, user, ids, context=context):
            if partner.campaign_order_ids:
                orders_total = 0
                for order_id in partner.campaign_order_ids :
                    orders_total=orders_total+order_id.money
                res[partner.id]=orders_total
            else :
                res[partner.id]=0.00        
        return res
    
    def _card_orders(self, cursor, user, ids, name, arg, context=None):
        res={}
        for partner in self.browse(cursor, user, ids, context=context):
            if partner.campaign_order_ids:
                res[partner.id]=len(partner.campaign_order_ids)
            else :
                res[partner.id]=0.00        
        return res
        
    def _card_brand_orders(self, cursor, user, ids, name, arg, context=None):
        res={}
        for partner in self.browse(cursor, user, ids, context=context):
            if partner.campaign_order_ids:
                card_brand_orders = 0
                for order_id in partner.campaign_order_ids :
                    if order_id.brand == partner.brand :
                        card_brand_orders = card_brand_orders +1
                res[partner.id] = card_brand_orders
            else :
                res[partner.id]=0.00        
        return res

    _columns = {
        'name': fields.char('#Vip Card',select=True,size=64),
        'state': fields.char('State', size=64),
        'city': fields.char('City', size=64),
        'ref': fields.char('Name', size=64),
        'mobile': fields.char('Mobile', size=64),
        'date_sale': fields.date('Date Sale'),
        'village': fields.char('village', size=64),
        'housenumber': fields.char('House Number', size=64),
        'brand': fields.char('Brand', size=64),
        'team': fields.char('Team', size=64),
        'saleperson': fields.char('Sale Person', size=64,),
        'checkin': fields.boolean('CheckIn'),
        'campaign_order_ids': fields.one2many('yatai.campaign.order', 'vcard_id', 'Camaign orders'),
        'date_import': fields.datetime('Date Import'),
        #'card_orders': fields.function(_card_orders, string='Card Orders', type='integer',store=True),
        'card_orders': fields.integer('Card Orders'),
        #'card_orders_total': fields.function(_card_orders_total, string='Card Orders Total', type='float',digits=(16,2),store=True),
        'card_orders_total': fields.float('Card Orders total',digits=(16,2)),
        #'card_brand_orders': fields.function(_card_brand_orders, string='Card Brand Orders', type='integer',store=True),
        'card_brand_orders': fields.integer('Card Brand Orders'),
        'user_id': fields.many2one('res.users', 'Import User', select=True, track_visibility='onchange'),
    }
    _sql_constraints = [
        ('name_key', 'UNIQUE (name)',  'You can not have two id with the same VCard !')
    ]

    _defaults = {
        'date_import': fields.datetime.now,
        'user_id': lambda obj, cr, uid, context: uid,
    }
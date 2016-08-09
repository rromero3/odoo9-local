from openerp.osv import fields, osv
import time
import datetime
from openerp import tools
from openerp.osv.orm import except_orm
from openerp.tools.translate import _
from dateutil.relativedelta import relativedelta

def str_to_datetime(strdate):
    return datetime.datetime.strptime(strdate, tools.DEFAULT_SERVER_DATE_FORMAT)

class fleet_vehicle_hoursmeter(osv.Model):
    _name='fleet.vehicle.hoursmeter'
    _description='Hoursmeter log for a vehicle'
    _order='date desc'

    def _vehicle_log_name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            name = record.vehicle_id.name
            if not name:
                name = record.date
            elif record.date:
                name += ' / '+ record.date
            res[record.id] = name
        return res

    def on_change_vehicle(self, cr, uid, ids, vehicle_id, context=None):
        if not vehicle_id:
            return {}

    _columns = {
        'name': fields.function(_vehicle_log_name_get_fnc, type="char", string='Name', store=True),
        'date': fields.date('Date'),
        'value': fields.float('Hoursmeter Value', group_operator="max"),
        'notes': fields.char('Notes'),
        'vehicle_id': fields.many2one('fleet.vehicle', 'Vehicle', required=True)
    }
    _defaults = {
        'date': fields.date.context_today,
    }

class empro_vehicle(osv.osv):

  _inherit = "fleet.vehicle"

  def _count_hoursmeter(self, cr, uid, ids, field_name, arg, context=None):
        Hoursmeter = self.pool['fleet.vehicle.hoursmeter']
        return {
            vehicle_id: {
                'hoursmeter_count': Hoursmeter.search_count(cr, uid, [('vehicle_id', '=', vehicle_id)], context=context),
               }
            for vehicle_id in ids
        }

  def _get_hoursmeter(self, cr, uid, ids, hoursmeter_id, arg, context):
        res = dict.fromkeys(ids, 0)
        for record in self.browse(cr,uid,ids,context=context):
            ids = self.pool.get('fleet.vehicle.hoursmeter').search(cr, uid, [('vehicle_id', '=', record.id)], limit=1, order='value desc')
            if len(ids) > 0:
                res[record.id] = self.pool.get('fleet.vehicle.hoursmeter').browse(cr, uid, ids[0], context=context).value
        return res

  def _set_hoursmeter(self, cr, uid, id, name, value, args=None, context=None):
        if value:
            date = fields.date.context_today(self, cr, uid, context=context)
            data = {'value': value, 'date': date, 'vehicle_id': id}
            return self.pool.get('fleet.vehicle.hoursmeter').create(cr, uid, data, context=context)

  _columns = {
    'vehicle_code': fields.char('Empro Code', required=True),
    'year': fields.integer('Year'),
    'is_rented': fields.boolean('Is Rented'),
    'hoursmeter_count': fields.function(_count_hoursmeter, type='integer', string='Hoursmeter', multi=True),
    'hoursmeter': fields.function(_get_hoursmeter, fnct_inv=_set_hoursmeter, type='float', string='Last Hoursmeter', help='Hoursmeter measure of the vehicle at the moment of this log')
  }

  _defaults ={
    'vehicle_code': 'XXX-000'
  }

empro_vehicle()
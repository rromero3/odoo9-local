from openerp.osv import fields, osv
import time
import datetime
from openerp import tools, api
from openerp.osv.orm import except_orm
from openerp.tools.translate import _
from dateutil.relativedelta import relativedelta

def str_to_datetime(strdate):
    return datetime.datetime.strptime(strdate, tools.DEFAULT_SERVER_DATE_FORMAT)

class empro_employee(osv.osv):
    _inherit = "hr.employee"

    _columns = {
        'employee_code': fields.char('Codigo Empro', required=True),
        'legal_name': fields.char('Nombre Legal'),
        'personal_email': fields.char('Email Personal'),
        'personal_phone': fields.char('Telefono Personal'),
        'personal_mobile': fields.char('Celular Personal'),
        'personal_address': fields.char('Direccion Personal'),
        'dependents_count': fields.integer('Numero de Dependientes'),
        'spouse_name': fields.char('Nombre del Conyuge'),
        'emergency_contact': fields.char('Contacto de Emergencia'),
        'driver_license': fields.char('Licencia de Conducir'),
        'driver_license_expiration' : fields.date("Expiracion Licencia de Conducir"),
        'interview_date' : fields.date("Fecha de entrevista"),
        'start_date' : fields.date("Fecha de Inicio", required=True),
        'end_date' : fields.date("Fecha de Salida"),
        'exit_reason': fields.char('Razon de Salida'),
        'years_hired': fields.integer('Anos Contratados'),
        'months_hired': fields.integer('Meses Contratados'),
        'days_hired': fields.integer('Dias Contratados'),
        'start_project': fields.char('Primer Proyecto'),
        'last_settlement' : fields.date("Ultima Liquidacion"),
        'years_settlement': fields.integer('Anos para liquidacion'),
        'months_settlement': fields.integer('Meses para liquidacion'),
        'days_settlement': fields.integer('Dias para liquidacion')
    }

    _defaults ={
        'start_date': datetime.date.today()
    }

    @api.onchange('start_date')
    def set_antiguedad(self):
        if self.start_date:
            start_date = str_to_datetime(self.start_date)
            today_date = datetime.datetime.now()
            rd = relativedelta(today_date, start_date)
            self.years_hired = rd.years
            self.months_hired = rd.months
            self.days_hired = rd.days

    @api.onchange('last_settlement')
    def set_liquidacion(self):
        if self.start_date:
            last_settlement = str_to_datetime(self.last_settlement)
            today_date = datetime.datetime.date()
            rd = relativedelta(today_date, last_settlement)
            self.years_settlement = rd.years
            self.months_settlement = rd.months
            self.days_settlement = rd.days

empro_employee()
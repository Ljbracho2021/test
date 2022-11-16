# -*- coding: utf-8 -*-

from email.policy import default
from odoo import api, fields, models
import calendar, datetime

class Wizard(models.TransientModel):
    _name = 'report.wizard'
    _description = 'Report Wizard'

    date_start       = fields.Date('Fecha Inicio', required=True, default=fields.Date.today )
    date_end         = fields.Date('Fecha Fin', required=True, default=fields.Date.today)
    carrera_id       = fields.Many2one('beca.carrera', string="Carrera", required=True)
    nombre_carrera    = fields.Char(string='Nombre', related='carrera_id.nombre', readonly=True, store=True)
    #nombre_parroquia = fields.Char(string='Nombre', related='comuna_id.parroquia_id.nombre', readonly=True, store=True)
    
    
    def primer_dia_mes(self):
        now = datetime.datetime.now()
        year = now.year
        month = now.month

        return datetime.date(year,month,1)

    def ultimo_dia_mes(self):
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        last_day = calendar.monthrange(year, month)[1] ## último día

        return datetime.date(year,month,last_day)

    def action_search_salida(self):
        form_data = self.read()[0]


        salida          = self.env['beca.planilla'].search_read(['|',('opcion1_id','=', self.carrera_id.id),('opcion2_id','=', self.carrera_id.id),'|',('opcion3_id','=', self.carrera_id.id),
                                                                     ('state', 'in', ['censado', 'becado'])
                                                                ], order ='opcion1_id asc')
 
        data = {
            'form_data': form_data,
            'salida'   : salida
        }

        return self.env.ref('reporteBeca.action_report').report_action(self, data=data)
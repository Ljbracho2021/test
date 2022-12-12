# -*- coding: utf-8 -*-

from email.policy import default
from odoo import api, fields, models
import calendar, datetime

class WizardA(models.TransientModel):
    _name = 'report.wizardb'
    _description = 'Report wizardb'

    date_start       = fields.Date('Fecha Inicio', required=True, default=fields.Date.today )
    date_end         = fields.Date('Fecha Fin', required=True, default=fields.Date.today)

   

    

    
    
    
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
        
        salida    = []

        conjunto       = self.env['beca.beca'].search([], order ='numero asc')
        compania       = self.env['res.company'].search([])

        for itera in conjunto: 

            indice     = self.env['beca.planilla'].search([('numero', '=', itera.numero)])
            
            if indice:
                cedula     = indice.cedula
                numero     = indice.name
                apellido   = indice.apellido1 
                if indice.apellido2:
                   apellido   = apellido + "  " + indice.apellido2
                
                nombre     = indice.nombre1 
                if indice.nombre2:
                   nombre   = nombre + "  " + indice.nombre2
 
                namefull   = apellido + "-" + nombre
                municipio  = indice.municipio_id.nombre
                parroquia  = indice.parroquia_id.nombre
                opcion1    = indice.opcion1_id.nombre
                opcion2    = indice.opcion2_id.nombre
                opcion3    = indice.opcion3_id.nombre
                modalidad  = indice.modalidad
                state      = indice.state

                if modalidad == "0":
                   modalidadName = "PUBLICA"
                elif modalidad == "1": 
                     modalidadName = "PRIVADA"
                else:
                    modalidadName = "VIRTUAL"
                
                salida.append({
                    
                    'numero'        : numero,         
                    'cedula'        : cedula, 
                    'apellido'      : apellido,  
                    'nombre'        : nombre,    
                    'namefull'      : namefull,
                    'municipio'     : municipio,
                    'parroquia'     : parroquia,
                    'modalidad'     : modalidadName,
                    'opcion1'       : opcion1,
                    'opcion2'       : opcion2,
                    'opcion3'       : opcion3,
                    'state'         : state,    

                    'company': self.env.user.company_id
                })

 
        data = {
            'form_data': form_data,
            'salida'   : salida
        }

        return self.env.ref('reporteBeca.action_report_b').report_action(self, data=data)
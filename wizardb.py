# -*- coding: utf-8 -*-

from email.policy import default
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import calendar, datetime
import random

class WizardA(models.TransientModel):
    _name = 'analytic.wizardb'
    _description = 'analytic Wizardb'

    date_start  = fields.Date('Fecha Inicio', required=True, default=fields.Date.today )
    date_end    = fields.Date('Fecha Fin', required=True, default=fields.Date.today)
    municipio_id = fields.Many2one('beca.municipio', string='Municipio *', help="Seleccione el Municipio (es campo Obligatorio).")

    cantidad    = fields.Integer(string="Cantidad de Becas *", required=True, default=0)
   
      
    
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


    def action_search_reiniciar(self):
        form_data = self.read()[0]
        salida    = []
        
        planillaSet     = self.env['beca.beca'].search([])
        planillaSet.unlink()

        productSet     = self.env['product.template'].search([])
        productSet.unlink()

        return 

    def action_search_cargar(self):
        form_data = self.read()[0]
        salida    = []
        
        temporalSet     = self.env['beca.temporal'].search([])
        temporalSet.unlink()

        planillaSet     = self.env['beca.planilla'].search([('municipio_id', '=', self.municipio_id.id),('state', '=', 'censado')])
        temporalSet     = self.env['beca.temporal']

        for indice in planillaSet:
            new = temporalSet.create({'numero'  : indice.numero})

        return 

    def action_search_cargar_product(self):
        form_data = self.read()[0]
        salida    = []
        
               
        productSet     = self.env['product.template'].search([])
        conjunto       = self.env['beca.beca'].search([], order ='numero asc')

        for itera in conjunto: 

            indice     = self.env['beca.planilla'].search([('numero', '=', itera.numero)])
            
            if indice:
               
                apellido   = indice.apellido1 
                if indice.apellido2:
                   apellido   = apellido + "  " + indice.apellido2
                
                nombre     = indice.nombre1 
                if indice.nombre2:
                   nombre   = nombre + "  " + indice.nombre2
    
                namefull   = apellido + " " + nombre
                barcode    = indice.cedula + "-" + indice.name
               
                new = productSet.create({'name'         : namefull,
                                         'barcode'      : barcode
                                       })
        return 
                                 
#-------------------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------------------
    def action_search_salida(self):
        form_data = self.read()[0]
        salida    = []
        
        #-------------------------------------------------------------------------------------------
        #  PUBLICA
        #-------------------------------------------------------------------------------------------
        contador = 0
        
        becaCreate  = self.env['beca.beca']

        seguir = True

        while seguir:

              numero = (random.randint(1,790000))
              auxNumero = str(numero)

              if len(auxNumero) <= 7:
                 aux = len(auxNumero)
                 falta = 7-aux

                 for i in range(falta):
                     auxNumero = "0" + str(auxNumero) 

              encontro = self.env['beca.temporal'].search([('numero', '=', auxNumero)], limit=1) 
              
              if encontro: 
                 

                 if contador < self.cantidad:

                    encontroBeca = self.env['beca.beca'].search([('numero', '=', auxNumero)], limit=1)
                    
                    if not encontroBeca:
                       new = becaCreate.create({'numero'  : encontro.numero})
                       contador = contador + 1

              if contador==self.cantidad:
                 seguir = False
   
        data = {
            'form_data': form_data,
            'salida'   : salida
        }

        return 
        
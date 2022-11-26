# -*- coding: utf-8 -*-

from email.policy import default
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import calendar, datetime

class WizardAnularn(models.TransientModel):
    _name = 'beca.wanularn'
    _description = 'Report Wizard'

    date_start       = fields.Date('Fecha Inicio', required=True, default=fields.Date.today )
    date_end         = fields.Date('Fecha Fin', required=True, default=fields.Date.today)
    numero       = fields.Char(string='Número Planilla *', required = True, help="Escriba el Nùmero de Planilla, debe contener solo nùmeros (es campo Obligatorio).")
 

    anulada_id = fields.Selection([
        ('0', 'EXTRAVIADA'),
        ('1', 'DETERIORADA'),
        ('2', 'NÙMERO DUPLICADO'),
        ('3', 'CON TACHADURAS'),
        ('4', 'OTRO'),
    ], required=True, string='Motivo Anulaciòn *', help="Seleccione la Modalidad de Estudios (es campo Obligatorio).")

    note_anulada = fields.Text(string="Observaciones", help="Escriba las Observaciones (es Opcional)." )

    #--------------------------------------------------------------------------------#
    #  VALIDACIONES PARA EL NUMERO DE PLANILLA                                       #
    #--------------------------------------------------------------------------------#
    @api.onchange('numero')
    def _onchange_numero(self):
        if not self.numero:
            return

        digito = self.numero.isdigit()
        if not digito:
            aux = self.numero
            self.numero = ""
            return {'warning': {
                'title': ("Mensaje de Error:"), 
                'message': ("Error: El NÚMERO DE PLANILLA debe contener solo números..! "), 
            }}

        if len(self.numero) > 7:
            aux = self.numero
            self.numero = ""
            return {'warning': {
                'title': ("Mensaje de Error:"), 
                'message': ("Error: El NÚMERO DE PLANILLA debe tener hasta 7 dígitos..! "), 
            }}

        if len(self.numero) <= 7:
            aux = len(self.numero)
            falta = 7-aux

            for i in range(falta):
                self.numero = "0" + str(self.numero)

            domain = [('numero', '=', self.numero)]
            if self.id.origin:
               domain.append(('id', '!=', self.id.origin))
        
            if self.env['beca.planilla'].search(domain, limit=1):
               aux_numero = self.numero
               self.numero = ""
               return {'warning': {
                        'title': ("Mensaje de Error:"), 
                        'message': ("Error: El NÚMERO DE PLANILLA ya existe..! ", aux_numero), 
                       }}

    def action_censado(self):
        form_data = self.read()[0]

        registro  = self.env['beca.planilla'].search([('numero','=', self.planilla_id.numero)])
        planilla  = self.env['beca.planilla'].browse([registro.id])

        if planilla:
           planilla.state = 'censado'
          
        return

    def action_anular(self):
        form_data = self.read()[0]

        registro  = self.env['beca.planilla']
        new = registro.create({'numero':self.numero,
                               'state': 'anulada',
                               'cedula': 'ANULADA',
                               'date_nacimiento': self.date_start,
                               'apellido1': 'ANULADA',
                               'apellido2': 'ANULADA',
                               'nombre1': 'ANULADA',
                               'nombre2': 'ANULADA',
                               'municipio_id': '001',
                               'parroquia_id': '001',
                               'direccion': 'ANULADA',
                               'telefono1': 'ANULADA',
                               'telefono2': 'ANULADA',
                               'modalidad': '0',
                               'anoegreso': '0',
                               'opcion1_id': '001',
                               'opcion2_id': '001',
                               'opcion3_id': '001',
                               'anulada_id': self.anulada_id,
                               'note_anulada': self.note_anulada

                              })

        return
# -*- coding: utf-8 -*-

from email.policy import default
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta

class BecaPlanilla(models.Model):
    _name        = 'beca.planilla'
    _description = 'Gestión de Becas - planilla'
    _rec_name    = 'name'

    name         = fields.Char(string='Nro.', required=True, copy=False, readonly=True, default=lambda self: _('New'))   
    numero       = fields.Char(string='Número Planilla (*)', required = True, help="Escriba el Nùmero de Planilla, debe contener solo nùmeros (es campo Obligatorio).")

    cedula       = fields.Char(string='Cédula Identidad', required = True, help="Escriba el Nùmero de Cedula, debe contener solo nùmeros (es campo Obligatorio).")
    apellido1    = fields.Char(string='1er. Apellido', required = True, help="Escriba el 1er. Apellido (es campo Obligatorio).")
    apellido2    = fields.Char(string='2do. Apellido', help="Escriba el 2do. Apellido (es campo Opcional).")
    nombre1      = fields.Char(string='1er. Nombre', required = True, help="Escriba el 1er. Nombre (es campo Obligatorio).")
    nombre2      = fields.Char(string='2do. Nombre', help="Escriba el 2do. Nombre (es campo Opcional).")
    
    date_nacimiento = fields.Date(string="Fecha Nacimiento", required=True, help="Escriba la Fecha de Nacimiento, formato DD/MM/AA (es campo Obligatorio).")
    estado_id    = fields.Many2one('beca.estado', store=True)
    municipio_id = fields.Many2one('beca.municipio', store=True, required = True, help="Seleccione el Municipio (es campo Obligatorio).")
    parroquia_id = fields.Many2one('beca.parroquia', store=True, required = True, help="Seleccione la Parroquia (es campo Obligatorio).")

    direccion    = fields.Char(string='Dirección', required = True, help="Escriba la Dirección (es campo Obligatorio).")
    telefono1    = fields.Char(string='Teléfono 1', required = True, help="Escriba el Nùmero de Teléfono, debe contener solo nùmeros (es campo Obligatorio).")
    telefono2    = fields.Char(string='Teléfono 2', help="Escriba el Nùmero de Teléfono, debe contener solo nùmeros (es campo Opcional).")

    opcion1_id   = fields.Many2one('beca.carrera', store=True, required = True, string='Opción 1', help="Seleccione el la Carrera (es campo Obligatorio).")
    opcion2_id   = fields.Many2one('beca.carrera', store=True, required = True, string='Opción 2', help="Seleccione el la Carrera (es campo Obligatorio).")
    opcion3_id   = fields.Many2one('beca.carrera', store=True, required = True, string='Opción 3', help="Seleccione el la Carrera (es campo Obligatorio).")

    #anoegreso    = fields.Char(string='Año Egreso Bachiller', required = True)
    #anoegreso    = fields.Many2one('beca.egreso', store=True, required = True,string='Año Egreso', help="Seleccione el Año de Egreso de bachillerato (es campo Obligatorio).")
    modalidad = fields.Selection([
        ('0', 'PRESENCIAL'),
        ('1', 'VIRTUAL'),
    ], required=True, string='Opciones de Estudio')

    anoegreso = fields.Selection([
        ('0', '2000'),
        ('1', '2001'),
        ('2', '2002'),
        ('3', '2003'),
        ('4', '2004'),
        ('5', '2005'),
        ('6', '2006'),
        ('7', '2007'),
        ('8', '2008'),
        ('9', '2009'),
        ('10', '2010'),
        ('11', '2011'),
        ('12', '2012'),
        ('13', '2013'),
        ('14', '2014'),
        ('15', '2015'),
        ('16', '2016'),
        ('17', '2017'),
        ('18', '2018'),
        ('19', '2019'),
        ('20', '2020'),
        ('21', '2021'),
        ('22', '2022'),
    ], required=True, string='Año Egreso')
    
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Favorito'),
    ], required=True, default='0', tracking=True)

    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the product without removing it.")
    note = fields.Text(string="Observaciones", help="Escriba las Observaciones (es Opcional)." )

    state = fields.Selection([('censado', 'CENSADO'), ('becado', 'BECADO'),
                              ('en proceso', 'EN PROCESO'), ('ejecutada', 'EJECUTADA'), ('cancelada', 'CANCELADA')], default='censado',
                             string="Status", tracking=True)     

    def action_aprobar(self):
        self.state = 'becado'

    def action_proceso(self):
        self.state = 'en proceso'

    def action_done(self):
        self.state = 'ejecutada'

    def action_draft(self):
        self.state = 'censado'

    def action_cancel(self):
        self.state = 'cancelada'  

    #--------------------------------------------------------------------------------#
    #  VALIDACIONES PARA EL NUMERO DE TELEFONO                                       #
    #--------------------------------------------------------------------------------#
    @api.onchange('telefono1')
    def _onchange_telefono1(self):
        if not self.telefono1:
            return

        digito = self.telefono1.isdigit()
        if not digito:
            aux = self.telefono1
            self.telefono1 = ""
            return {'warning': {
                'title': ("Precauciòn:"), 
                'message': ("Error en el Número de Teléfono, escribió ", aux + ". Debe contener solo números..! "), 
            }}

        if len(self.telefono1) != 11:
            self.telefono1 = ""
            return {'warning': {
                'title': ("Precauciòn:"), 
                'message': ("Error en el Número de Teléfono..! "), 
            }}

    #--------------------------------------------------------------------------------#
    #  VALIDACIONES PARA EL NUMERO DE TELEFONO                                       #
    #--------------------------------------------------------------------------------#
    @api.onchange('telefono2')
    def _onchange_telefono2(self):
        if not self.telefono2:
            return

        digito = self.telefono2.isdigit()
        if not digito:
            aux = self.telefono2
            self.telefono2 = ""
            return {'warning': {
                'title': ("Precauciòn:"), 
                'message': ("Error en el Número de Teléfono, escribió ", aux + ". Debe contener solo números..! "), 
            }}

        if len(self.telefono2) != 11:
            self.telefono2 = ""
            return {'warning': {
                'title': ("Precauciòn:"), 
                'message': ("Error en el Número de Teléfono..! "), 
            }}

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
                'title': ("Precauciòn:"), 
                'message': ("Error en el Número de Planilla, escribió ", aux + ". Debe contener solo números..! "), 
            }}

        if len(self.numero) != 5:
            aux = self.numero
            self.numero = ""
            return {'warning': {
                'title': ("Precauciòn:"), 
                'message': ("Error en el Número de Planilla, escribió ", aux + ". Debe tener 5 digitos..! "), 
            }}

        aux_int = int(self.numero)
        if aux_int > 99999:
            aux = self.numero
            self.numero = ""
            return {'warning': {
                'title': ("Precauciòn:"), 
                'message': ("Error en el Número de Planilla, escribió ", aux + ". El Número debe estar entre 1 y 99.999"), 
            }}

        aux_int = int(self.numero)
        if aux_int < 1:
            aux = self.numero
            self.numero = ""
            return {'warning': {
                'title': ("Precauciòn:"), 
                'message': ("Error en el Número de Planilla, escribió ", aux + ". El Número debe estar entre 1 y 99.999"), 
            }}

        domain = [('numero', '=', self.numero)]
        if self.id.origin:
            domain.append(('id', '!=', self.id.origin))
        
        if self.env['beca.planilla'].search(domain, limit=1):
            aux_numero = self.numero
            self.numero = ""
            return {'warning': {
                'title': ("Precauciòn:"), 
                'message': ("Número de Planilla ya existe  ", aux_numero), 
            }}
    #--------------------------------------------------------------------------------#
    #  VALIDACIONES PARA LA CEDULA DE IDENTIDAD                                      #
    #--------------------------------------------------------------------------------#
    @api.onchange('cedula')
    def _onchange_cedula(self):
        if not self.cedula:
            return

        digito = self.cedula.isdigit()
        if not digito:
            aux = self.cedula
            self.cedula = ""
            return {'warning': {
                'title': ("Precauciòn:"), 
                'message': ("Error en el Número de Cédula, escribió ", aux + ". Debe contener solo números..! "),  
            }}

        aux_int = int(self.cedula)
        if aux_int > 99999999:
            aux = self.cedula
            self.cedula = ""
            return {'warning': {
                'title': ("Precauciòn:"), 
                'message': ("Error en el Número de Cédula, escribió ", aux  + ". El número debe estar entre 10.000.000 y 99.999.999"), 
            }}

        aux_int = int(self.cedula)
        if aux_int < 10000000:
            aux = self.cedula
            self.cedula = ""
            return {'warning': {
                'title': ("Precauciòn:"), 
                'message': ("Error en el Número de Cédula, escribió ", aux  + ". El número debe estar entre 10.000.000 y 99.999.999"),  
            }}
        
        domain = [('cedula', '=', self.cedula)]
        if self.id.origin:
            domain.append(('id', '!=', self.id.origin))
        
        if self.env['beca.planilla'].search(domain, limit=1):
            aux_cedula = self.cedula
            self.cedula = ""
            return {'warning': {
                'title': ("Precauciòn:"), 
                'message': ("El Número de Cédula de Identidad ya existe  ", aux_cedula), 
            }}
    #--------------------------------------------------------------------------------#
    #  VALIDACIONES PARA AÑO EGRESO                                                  #
    #--------------------------------------------------------------------------------#
    # @api.onchange('anoegreso')
    # def _onchange_anoegreso(self):
    #     if not self.anoegreso:
    #         return

    #     digito = self.anoegreso.isdigit()
    #     if not digito:
    #         self.anoegreso = ""
    #         return {'warning': {
    #             'title': ("Precauciòn:"), 
    #             'message': ("Error en el año de egreso..! "), 
    #         }}

    #     if len(self.anoegreso)<4:
    #         self.anoegreso = ""
    #         return {'warning': {
    #             'title': ("Precauciòn:"), 
    #             'message': ("Error en el año de egreso..! "), 
    #         }}

    #     aux_fecha = "01/01/" + self.anoegreso
    #     fecha_dt = datetime.strptime(aux_fecha, '%d/%m/%Y')

    #     d1 = fecha_dt
    #     d2 = datetime.today().date()
    #     rd = relativedelta(d2, d1)
    #     cantidad = str(rd.years)
    #     aux_int = int(cantidad)
        
    #     if aux_int > 20:
            
    #         self.anoegreso = ""
    #         return {'warning': {
    #             'title': ("Precauciòn:"), 
    #             'message': ("Número de años de egresado exede el lìmite (10). Tiene: ", str(aux_int) + " años de egesado..!"), 
    #         }}

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('beca.planilla') or _('New')
        res = super(BecaPlanilla, self).create(vals)
        return res

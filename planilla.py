# -*- coding: utf-8 -*-

from email.policy import default
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta

class BecaPlanilla(models.Model):
    _name        = 'beca.planilla'
    _description = 'Gestión de Becas - planilla'
    _rec_name    = 'numero'

    name         = fields.Char(string='Número Planilla', required=True, copy=False, readonly=True, default=lambda self: _('New'))   
    numero       = fields.Char(string='Número Planilla *', required = True, help="Escriba el Nùmero de Planilla, debe contener solo nùmeros (es campo Obligatorio).")
    
    cedula       = fields.Char(string='Cédula *', required = True, help="Escriba el Nùmero de Cedula, debe contener solo nùmeros (es campo Obligatorio).")
    apellido1    = fields.Char(string='1er. Apellido *', required = True, help="Escriba el 1er. Apellido (es campo Obligatorio).")
    apellido2    = fields.Char(string='2do. Apellido', help="Escriba el 2do. Apellido (es campo Opcional).")
    nombre1      = fields.Char(string='1er. Nombre *', required = True, help="Escriba el 1er. Nombre (es campo Obligatorio).")
    nombre2      = fields.Char(string='2do. Nombre', help="Escriba el 2do. Nombre (es campo Opcional).")
    
    date_nacimiento = fields.Date(string="Fecha de Nac. *", required=True, help="Escriba la Fecha de Nacimiento, formato DD/MM/AA (es campo Obligatorio).")
    estado_id    = fields.Many2one('beca.estado', store=True)
    municipio_id = fields.Many2one('beca.municipio', string='Municipio *', required = True, help="Seleccione el Municipio (es campo Obligatorio).")
    parroquia_id = fields.Many2one('beca.parroquia', string='Parroquia *', required = True, help="Seleccione la Parroquia (es campo Obligatorio).")

    direccion    = fields.Char(string='Dirección *', required = True, help="Escriba la Dirección (es campo Obligatorio).")
    telefono1    = fields.Char(string='Teléfono Celular *', required = True, help="Escriba el Nùmero de Teléfono, debe contener solo nùmeros (es campo Obligatorio).")
    telefono2    = fields.Char(string='Teléfono Celular 2', help="Escriba el Nùmero de Teléfono, debe contener solo nùmeros (es campo Opcional).")

    opcion1_id   = fields.Many2one('beca.carrera', store=True, required = True, string='Opción 1 *', help="Seleccione la Carrera (es campo Obligatorio).")
    opcion2_id   = fields.Many2one('beca.carrera', store=True, string='Opción 2 *', help="Seleccione la Carrera (es campo Obligatorio).")
    opcion3_id   = fields.Many2one('beca.carrera', store=True, string='Opción 3 *', help="Seleccione la Carrera (es campo Obligatorio).")

    modalidad = fields.Selection([
        ('0', 'UNIVERSIDAD PUBLICA'),
        ('1', 'UNIVERSIDAD PRIVADA'),
        ('2', 'PLATAFORMA EDUCATIVA VIRTUAL'),
    ], required=True, string='Opciones Estudio *', help="Seleccione la Modalidad de Estudios (es campo Obligatorio).")

    anoegreso = fields.Selection([
         ('0', '1950'),('1', '1951'),('2', '1952'),('3', '1953'),('4', '1954'),('5', '1955'),('6', '1956'),('7', '1957'),('8', '1958'),('9', '1959'),('10', '1960'),
                      ('11', '1961'),('12', '1962'),('13', '1963'),('14', '1964'),('15', '1965'),('16', '1966'),('17', '1967'),('18', '1968'),('19', '1969'),('20', '1970'),
                      ('21', '1971'),('22', '1972'),('23', '1973'),('24', '1974'),('25', '1975'),('26', '1976'),('27', '1977'),('28', '1978'),('29', '1979'),('30', '1980'),
                      ('31', '1981'),('32', '1982'),('33', '1983'),('34', '1984'),('35', '1985'),('36', '1986'),('37', '1987'),('38', '1988'),('39', '1989'),('40', '1990'),
                      ('41', '1991'),('42', '1992'),('43', '1993'),('44', '1994'),('45', '1995'),('46', '1996'),('47', '1997'),('48', '1998'),('49', '1999'),('50', '2000'),
                      ('51', '2001'),('52', '2002'),('53', '2003'),('54', '2004'),('55', '2005'),('56', '2006'),('57', '2007'),('58', '2008'),('59', '2009'),('60', '2010'),
                      ('61', '2011'),('62', '2012'),('63', '2013'),('64', '2014'),('65', '2015'),('66', '2016'),('67', '2017'),('68', '2018'),('69', '2019'),('70', '2020'),
                      ('71', '2021'),('72', '2022')   
    ], string='Año Egreso *', required = True, help="Seleccione el Año de Egres de Bachillerato (es campo Obligatorio).")
    
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Favorito'),
    ], required=True, default='0', tracking=True)

    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the product without removing it.")
    note = fields.Text(string="Observaciones", help="Escriba las Observaciones (es Opcional).")

    anulada_id = fields.Selection([
        ('EXTRAVIADA', 'EXTRAVIADA'),
        ('DETERIORADA', 'DETERIORADA'),
        ('NUMERO DUPLICADO', 'NUMERO DUPLICADO'),
        ('CON TACHADURAS', 'CON TACHADURAS'),
        ('OTRO', 'OTRO'),
    ], string='Motivo Anulaciòn *', help="Seleccione el Motivo de Anulaciòn de la Planilla (es campo Obligatorio).")

    note_anulada = fields.Text(string="Observaciones", help="Escriba las Observaciones (es Opcional)." )
   
    state = fields.Selection([('censado', 'CENSADO'), 
                              ('becado', 'BECADO'),
                              ('anulada', 'ANULADA')], default='censado',
                             string="Status", tracking=True)   


    def action_aprobar(self):
        self.state = 'becado'

    def action_draft(self):
        self.state = 'censado'

    def action_cancel(self):
        self.state = 'anulada'  

    def action_a_becado(self):
        self.state = 'becado'

    #--------------------------------------------------------------------------------#
    #  VALIDACIONES PARA EL NUMERO DE PLANILLA                                       #
    #--------------------------------------------------------------------------------#
    @api.constrains('numero')
    def _check_numero(self):
        if self.env['beca.indice'].search_count([
                ('numero', '=', self.numero)                
            ]) > 1:
            raise ValidationError(_("Error: El NÚMERO DE PLANILLA ya existe..!"))

    #--------------------------------------------------------------------------------#
    #  VALIDACIONES PARA EL NUMERO DE CEDULA                                      #
    #--------------------------------------------------------------------------------#
    @api.constrains('cedula')
    def _check_cedula(self):
        if self.env['beca.indice'].search_count([
                ('cedula', '=', self.cedula)                
            ]) > 1:
            raise ValidationError(_("Error: El NÚMERO DE CÉDULA ya existe..!"))

    #--------------------------------------------------------------------------------#
    #  VALIDACIONES PARA EL NUMERO DE TELEFONO                                       #
    #--------------------------------------------------------------------------------#
    @api.onchange('modalidad')
    def _onchange_modalidad(self):
        if not self.modalidad:
            return

        self.opcion1_id = ""
        self.opcion2_id = ""
        self.opcion3_id = ""

    #--------------------------------------------------------------------------------#
    #  VALIDACIONES PARA EL NUMERO DE TELEFONO                                       #
    #--------------------------------------------------------------------------------#
    @api.onchange('opcion1_id')
    def _onchange_opcion1_id(self):
        
        if not self.opcion1_id and self.opcion2_id:
            self.opcion1_id = self.opcion2_id
            self.opcion2_id = ""
            return

        # if not self.opcion2_id and self.opcion3_id:
        #     self.opcion2_id = self.opcion3_id
        #     self.opcion3_id = ""
        #     return

    #--------------------------------------------------------------------------------#
    #  VALIDACIONES PARA EL NUMERO DE TELEFONO                                       #
    #--------------------------------------------------------------------------------#
    @api.onchange('opcion2_id')
    def _onchange_opcion2_id(self):
        
        if not self.opcion1_id and self.opcion2_id:
            self.opcion1_id = self.opcion2_id
            self.opcion2_id = ""
            return

        if not self.opcion2_id and self.opcion3_id:
            self.opcion2_id = self.opcion3_id
            self.opcion3_id = ""
            return

    #--------------------------------------------------------------------------------#
    #  VALIDACIONES PARA EL NUMERO DE TELEFONO                                       #
    #--------------------------------------------------------------------------------#
    @api.onchange('opcion3_id')
    def _onchange_opcion3_id(self):
        if not self.opcion3_id:
            return

        if not self.opcion2_id and self.opcion3_id:
            self.opcion2_id = self.opcion3_id
            self.opcion3_id = ""
            return

        
    #--------------------------------------------------------------------------------#
    #  VALIDACIONES PARA EL NUMERO DE TELEFONO                                       #
    #--------------------------------------------------------------------------------#
    @api.onchange('municipio_id')
    def _onchange_municipio_id(self):
        if not self.municipio_id:
            return

        self.parroquia_id = ""

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
                'title': ("Mensaje de Error:"), 
                'message': ("Error: El NÚMERO DE TELÉFONO debe contener solo números..! "), 
            }}

        if len(self.telefono1) != 11:
            self.telefono1 = ""
            return {'warning': {
                'title': ("Mensaje de Error:"), 
                'message': ("Error: El NÚMERO DE TELÉFONO debe contener 11 dígititos..! "), 
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
                'title': ("Mensaje de Error:"), 
                'message': ("Error: El NÚMERO DE TELÉFONO debe contener solo números..!"), 
            }}

        if len(self.telefono2) != 11:
            self.telefono2 = ""
            return {'warning': {
                'title': ("Mensaje de Error:"), 
                'message': ("Error: El NÚMERO DE TELÉFONO debe contener 11 dígititos..! "), 
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
        
            if self.env['beca.indice'].search(domain, limit=1):
               aux_numero = self.numero
               self.numero = ""
               return {'warning': {
                         'title': ("Mensaje de Error:"), 
                         'message': ("Error: El NÚMERO DE PLANILLA ya existe..! ", aux_numero), 
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
                'title': ("Mensaje de Error:"), 
                'message': ("Error: eL número de cédula debe contener solo números..! "),  
            }}

        aux_int = int(self.cedula)
        if aux_int > 9999999999:
            aux = self.cedula
            self.cedula = ""
            return {'warning': {
                'title': ("Mensaje de Error:"), 
                'message': ("Error: EL NÚMERO DE CÉDULA debe estar entre 9.999.999.999 y 1.000.000"), 
            }}

        aux_int = int(self.cedula)
        if aux_int < 1000000:
            aux = self.cedula
            self.cedula = ""
            return {'warning': {
                'title': ("Mensaje de Error:"), 
                'message': ("Error: EL NÚMERO DE CÉDULA debe estar entre 9.999.999.999 y 1.000.000"),  
            }}
        
        domain = [('cedula', '=', self.cedula)]
        if self.id.origin:
            domain.append(('id', '!=', self.id.origin))
        
        if self.env['beca.indice'].search(domain, limit=1):
            aux_cedula = self.cedula
            self.cedula = ""
            return {'warning': {
                'title': ("Mensaje de Error:"), 
                'message': ("Error: El NÚMERO DE CÉDULA Identidad ya existe  ", aux_cedula), 
            }}
 
    @api.onchange('nombre1')
    def _onchange_nombre1(self):
         
        if self.nombre1:
            self.nombre1 = self.nombre1.upper()

    @api.onchange('nombre2')
    def _onchange_nombre2(self):
         
        if self.nombre2:
            self.nombre2 = self.nombre2.upper()
    
    @api.onchange('apellido1')
    def _onchange_apellido1(self):
         
        if self.apellido1:
            self.apellido1 = self.apellido1.upper()

    @api.onchange('apellido2')
    def _onchange_apellido2(self):
         
        if self.apellido2:
            self.apellido2 = self.apellido2.upper()

    @api.onchange('direccion')
    def _onchange_direccion(self):
         
        if self.direccion:
            self.direccion = self.direccion.upper()

    
    def _create_indice(self,nro,cedu):
         
        registro  = self.env['beca.indice']
        new = registro.create({'numero': nro,
                               'cedula': cedu,
                              })

    @api.model
    def create(self, vals):
 
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = "PC-" + vals['numero']

        self._create_indice(vals['numero'],vals['cedula'])
        res = super(BecaPlanilla, self).create(vals)
        
        return res



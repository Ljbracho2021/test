from email.policy import default
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class BecaRegistro(models.Model):
    _name        = 'beca.registro'
    _description = 'Gestion de Becas - Permite registrt el eMail'
    

    cedula         = fields.Char(string='Número Cédula', required=True) 
    nombre         = fields.Char(string='Nombre *')
    modalidad      = fields.Char(string='Modalidad *')
    condicion      = fields.Char(string='Condicion *')  
    correo         = fields.Char(string='eMail *')

    #--------------------------------------------------------------------------------#
    #  VALIDACIONES PARA EL CORREO                                                   #
    #--------------------------------------------------------------------------------#
    @api.constrains('correo')
    def check_correo(self):
        if not self.correo:
            return

        registro = self.env['beca.planilla'].search_read([('cedula', '=', self.cedula)], limit=1)
        if registro:
           id = registro[0]['id']

           auxReg = self.env['beca.planilla'].browse(id)
           auxReg.correo = self.correo
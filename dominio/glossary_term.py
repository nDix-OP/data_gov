import datetime

from odoo import fields, models, api
from odoo.exceptions import UserError
from .category_type import CategoryType
from .status import Status as St


class GlossaryTerm(models.Model):
    # nombre de la tabla de la BD (convierte . a _)
    _name = 'datagov.glossary.term'
    _description = 'Glossary term'
    _sql_constraints = [  # los check o unique
        ('name_unique', 'unique(name)', 'El atributo "Nombre" (name) debe ser único')
    ]

    # atributos mapeados
    id = fields.Id('Id', required=True)  # defecto es falso, id lo crea solo pero esta bien tenerlo tambien aqui
    name = fields.Text('Nombre', required=True)
    status = fields.Selection(selection=[  # lista valor - etiqueta
        (St.CURRENT.name, 'Vigente'),
        (St.NOT_IN_FORCE.name, 'Retirado'),
        (St.PROPOSED.name, 'Propuesto')
    ], string='Estado', required=True)
    statusDate = fields.Date('Fecha de estado', required=True,
                             default=datetime.date.today())  # se tiene que cambiar en onChange de status
    acronym = fields.Text('Acrónimo')
    definition = fields.Text('Definición', required=True)
    misunderstanding = fields.Text('No confundir con')
    category = fields.Many2one('datagov.category', 'Categoría', required=True)  # clase Category
    termSource = fields.Text('Fuente', required=True)
    owner = fields.Many2one('datagov.actor', 'Propietario', required=True)   # many2one (tabla BD, descripcion)

    # al cambiar el status, la fecha de modificación es la actual
    @api.onchange("status")
    def _onchange_status_date(self):
        self.statusDate = fields.Date.today()

    # restricción de que la categoría sea de rol
    @api.onchange('category')
    def on_change_category(self):
        # comparar con el __eq__, si se pone vacío no salta pero después no deja guardar
        if self.category.type != CategoryType.GLOSSARY_TERM and self.category.name is not False:
            self.category = False  # dejar el valor anterior
            # lanzar notificación
            raise UserError("La categoría del término debe ser una del tipo 'Término del glosario'.")
        return

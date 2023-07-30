import datetime

from odoo import fields, models, api
from odoo.exceptions import UserError
from .category_type import CategoryType
from .status import Status as St


class Actor(models.Model):
    # nombre de la tabla de la BD (convierte . a _)
    _name = 'datagov.principle'
    _description = 'Data Governance Principle'
    _sql_constraints = [  # los check o unique
        ('name_unique', 'unique(name)', 'El atributo "Nombre" (name) debe ser único')
    ]

    id = fields.Id('Id', required=True)
    name = fields.Text('Nombre', required=True)
    category = fields.Many2one('datagov.category', 'Categoría', required=True)  # clase Category
    status = fields.Selection(selection=[  # lista valor - etiqueta
        (St.CURRENT.name, 'Vigente'),
        (St.NOT_IN_FORCE.name, 'Retirado'),
        (St.PROPOSED.name, 'Propuesto')
    ], string='Estado', required=True)
    statusDate = fields.Date('Fecha de estado', required=True,
                             default=datetime.date.today())  # se tiene que cambiar en onChange de status

    statement = fields.Text('Definición', required=True)
    rationale = fields.Text('Justificación', required=True)
    implication = fields.Text('Implicaciones', required=True)
    # aunque se use Many2one y de ese tipo, no se crean FK en la BD
    owner = fields.Many2one('datagov.actor', 'Propietario', required=True)

    # restricción de la categoría
    @api.onchange('category')
    def on_change_category(self):
        # comparar con el __eq__, si se pone vacío no salta pero después no deja guardar
        if self.category.type != CategoryType.PRINCIPLE and self.category.name is not False:
            self.category = False  # dejar el valor anterior
            # lanzar notificación
            raise UserError("La categoría del principio debe ser una del tipo 'Principio'.")
        return

    # al cambiar el status, la fecha de modificación es la actual
    @api.onchange("status")
    def _onchange_status_date(self):
        self.statusDate = fields.Date.today()

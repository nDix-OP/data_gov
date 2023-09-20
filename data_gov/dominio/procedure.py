"""
Clase de domino de Procedure, se persiste automáticamente en la BD.
"""
import datetime

from .category_type import CategoryType
from odoo import fields, models, api
from odoo.exceptions import UserError
from .status import Status


class Procedure(models.Model):  # subclase de esta para persistir automáticamente en BD
    id = fields.Id('Id', required=True)
    name = fields.Text('Nombre', required=True)
    category = fields.Many2one('datagov.category', 'Categoría', required=True)  # clase Category
    description = fields.Text('Descripción', required=True)
    status = fields.Selection(selection=[  # lista valor - etiqueta
        (Status.CURRENT.name, 'Vigente'),
        (Status.NOT_IN_FORCE.name, 'Retirado'),
        (Status.PROPOSED.name, 'Propuesto')
    ], string='Estado', required=True)
    statusDate = fields.Date('Fecha de estado', required=True,
                             default=datetime.date.today())  # se tiene que cambiar en onChange de status
    version = fields.Text('Versión', required=True)
    docLink = fields.Text('Enlace al documento', required=True)
    owner = fields.Many2one('datagov.actor', 'Propietario', required=True)   # many2one

    # oculto, no se ve en la interfaz
    policy = fields.Many2many(relation='datagov_policy_procedure', comodel_name='datagov.policy',
                              column1='id_procedure', column2='id_policy', string='Políticas')

    # ---------------------------------------- Private Attributes ---------------------------------
    #  para la base de datos, no se muy bien que son cada una
    _name = 'datagov.procedure'  # nombre de la tabla BD
    _description = 'Procedimiento'
    _order = 'id desc'  # orden del indice por defecto
    _sql_constraints = [  # los check o unique
        ('name_unique', 'unique(name)', 'El atributo "Nombre" (name) debe ser único')
    ]

    # restricción de que la categoría sea de rol
    @api.onchange('category')
    def on_change_category(self):
        # comparar con el __eq__, si se pone vacío no salta pero después no deja guardar
        if self.category.type != CategoryType.PROCEDURE and self.category.name is not False:
            self.category = False  # dejar el valor anterior
            # lanzar notificación
            raise UserError("La categoría del procedimiento debe ser una del tipo 'Procedimiento'.")
        return

    # al cambiar el status, la fecha de modificación es la actual
    @api.onchange("status")
    def _onchange_status_date(self):
        self.statusDate = fields.Date.today()

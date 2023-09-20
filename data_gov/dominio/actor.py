"""
    Clase de domino de Actor, se persiste automáticamente en la BD.
"""
from odoo import fields, models, api
from odoo.exceptions import UserError
from .category_type import CategoryType


class Actor(models.Model):
    # nombre de la tabla de la BD (convierte . a _)
    _name = 'datagov.actor'
    _description = 'Data Governance Actor'
    _sql_constraints = [  # los check o unique
        ('name_unique', 'unique(name)', 'El atributo "Nombre" (name) debe ser único')
    ]

    id = fields.Id('Id', required=True)
    name = fields.Text('Nombre', required=True)
    category = fields.Many2one('datagov.category', 'Categoría', required=True)  # clase Category
    description = fields.Text('Descripción', required=True)
    organizationUnit = fields.Many2one('datagov.organization.unit', 'Departamento', required=True)
    location = fields.Many2one('datagov.location', 'Ubicación', required=True)
    # Many2one (otra tabla y descripción)
    owner = fields.Many2one('datagov.actor', 'Propietario')   # IMPORTANTE: no requerido para poder añadir uno
    # Many2many (otra tabla, nombre de la tabla N-N, nombres de las columnas y nombre en la interfaz)
    performs = fields.Many2many(comodel_name='datagov.role', relation='datagov_role_actor', column1='id_actor',
                                column2='id_role', string='Roles')
    # One2many (otra tabla, atributo otra clase y descripción), poner many2one en la otra clase
    objective = fields.One2many('datagov.dg.objective', 'actor', string='Objetivos como responsable')

    # atributo oculto para la indicar que se le difunde el KPI
    kpi_disseminatedTo = fields.Many2many(relation='datagov_kpi_disseminated_to', comodel_name='datagov.kpi',
                                          column1='id_actor', column2='id_kpi', string='KPIs a los que se le difunde')

    # restricción de que la categoría sea de actor
    @api.onchange('category')
    def on_change_category(self):
        # comparar con el __eq__, si se pone vacío no salta pero después no deja guardar
        if self.category.type != CategoryType.ACTOR and self.category.name is not False:
            self.category = False  # dejar el valor anterior
            # lanzar notificación
            raise UserError("La categoría del actor debe ser una del tipo 'Actor'.")
        return

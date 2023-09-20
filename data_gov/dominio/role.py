"""
Clase de domino de Role, se persiste automáticamente en la BD.
"""
from .category_type import CategoryType
from odoo import fields, models, api
from odoo.exceptions import UserError


class Role(models.Model):  # subclase de esta para persistir automáticamente en BD
    id = fields.Id('Id', required=True)
    name = fields.Text('Nombre', required=True)
    mainTasks = fields.Text('Tareas principales', required=True)
    profile = fields.Text('Perfil', required=True)
    category = fields.Many2one('datagov.category', 'Categoría', required=True)  # clase Category
    owner = fields.Many2one('datagov.actor', 'Propietario', required=True)   # many2one (tabla BD, descripcion)
    # Many2many(otra tabla objeto, nombre tabla relacion, fkcolumna1, fkcolumna2, descripcion)
    performedBy = fields.Many2many(comodel_name='datagov.actor', relation='datagov_role_actor', column1='id_role',
                                   column2='id_actor', string='Actores con el rol')

    # ---------------------------------------- Private Attributes ---------------------------------
    #  para la base de datos, no se muy bien que son cada una
    _name = 'datagov.role'  # nombre de la tabla BD
    _description = 'Rol'
    _order = 'id desc'  # orden del indice por defecto
    _sql_constraints = [  # los check o unique
        ('name_unique', 'unique(name)', 'El atributo "Nombre" (name) debe ser único')
    ]

    # restricción de que la categoría sea de rol
    @api.onchange('category')
    def on_change_category(self):
        # comparar con el __eq__, si se pone vacío no salta pero después no deja guardar
        if self.category.type != CategoryType.ROLE and self.category.name is not False:
            self.category = False  # dejar el valor anterior
            # lanzar notificación
            raise UserError("La categoría del rol debe ser una del tipo 'Rol'.")
        return
    
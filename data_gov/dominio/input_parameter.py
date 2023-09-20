"""
Clase de domino de parámetro de entrada, se persiste automáticamente en la BD.
"""
from .category_type import CategoryType
from odoo import fields, models, api
from odoo.exceptions import UserError


class InputParameter(models.Model):  # subclase de esta para persistir automáticamente en BD
    id = fields.Id('Id', required=True)
    name = fields.Text('Nombre', required=True)
    description = fields.Text('Descripción', required=True)
    category = fields.Many2one('datagov.category', 'Categoría', required=True)   # many2one

    # ---------------------------------------- Private Attributes ---------------------------------
    #  para la base de datos, no se muy bien que son cada una
    _name = 'datagov.input.parameter'  # nombre de la tabla BD
    _description = 'Input parameter for KPI'
    _order = 'id desc'  # orden del indice por defecto
    _sql_constraints = [  # los check o unique
        ('name_unique', 'unique(name)', 'El atributo "Nombre" (name) debe ser único')
    ]

    # restricción de la categoría
    @api.onchange('category')
    def on_change_category(self):
        # comparar con el __eq__, si se pone vacío no salta pero después no deja guardar
        if self.category.type != CategoryType.INPUT_PARAMETER and self.category.name is not False:
            self.category = False  # dejar el valor anterior
            # lanzar notificación
            raise UserError("La categoría del parámetro de entrada debe ser una del tipo 'Parámetro de entrada'.")
        return

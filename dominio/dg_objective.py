"""
Clase de domino de Objetivo de Gobernanza de Datos, se persiste automáticamente en la BD.
"""
import datetime

from .category_type import CategoryType
from odoo import fields, models, api
from odoo.exceptions import UserError


class DgObjective(models.Model):  # subclase de esta para persistir automáticamente en BD
    id = fields.Id('Id', required=True)
    name = fields.Text('Nombre', required=True)
    date = fields.Date('Fecha de cumplimiento', required=True, default=datetime.date.today())
    description = fields.Text('Descripción', required=True)
    category = fields.Many2one('datagov.category', 'Categoría', required=True)  # clase Category
    owner = fields.Many2one('datagov.actor', 'Propietario', required=True)  # many2one (tabla BD, descripción)
    actor = fields.Many2one('datagov.actor', 'Responsable', required=True)

    # es One2Many, por lo que no se puede agregar desde la vista de formulario
    metric = fields.One2many('datagov.kpi', 'objective', string='KPIs asociados al objetivo')

    # ---------------------------------------- Atributos privados ---------------------------------
    #  para la base de datos, no se muy bien que son cada una
    _name = 'datagov.dg.objective'  # nombre de la tabla BD
    _description = 'Objetivo de Gobernanza de Datos'
    _order = 'id desc'  # orden del indice por defecto
    _sql_constraints = [  # los check o unique
        ('name_unique', 'unique(name)', 'El atributo "Nombre" (name) debe ser único')
    ]

    # restricción de que la categoría sea de DG OBJECTIVE
    @api.onchange('category')
    def check_category(self):
        if self.category.type != CategoryType.DG_OBJECTIVE and self.category.name is not False:
            self.category = False  # dejar el valor anterior
            # lanzar notificación
            raise UserError("La categoría del objetivo de gobernanza de datos debe ser una del tipo " +
                            "'Objetivo Gob. datos'.")
        return

    @api.constrains('metric')
    def check_has_metric(self):
        if len(self.metric.ids) == 0:
            raise UserError("El objetivo de gobernanza debe tener, al menos, una métrica asociada.")


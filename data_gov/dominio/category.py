from odoo import fields, models, api
from odoo.exceptions import UserError
from . import category_type as tipo


class Category(models.Model):
    # nombre de la tabla de la BD (convierte . a _)
    _name = "datagov.category"
    _description = "Category type"
    _order = "id DESC"

    id = fields.Id("Id", required=True)
    name = fields.Text("Nombre", required=True)
    description = fields.Text("Descripción", required=True)
    type = fields.Selection(selection=[  # lista valor - etiqueta
        # no veo otra forma que poner uno a uno cada valor
        # hay que meter el nombre, no deja poniendo el objeto entero
        (tipo.CategoryType.INPUT_PARAMETER.name, tipo.CategoryType.INPUT_PARAMETER.value),
        (tipo.CategoryType.ROLE.name, tipo.CategoryType.ROLE.value),
        (tipo.CategoryType.ACTOR.name, tipo.CategoryType.ACTOR.value),
        (tipo.CategoryType.SECURITY_CLASSIFICATION.name, tipo.CategoryType.SECURITY_CLASSIFICATION.value),
        (tipo.CategoryType.DATA_ENTITY.name, tipo.CategoryType.DATA_ENTITY.value),
        (tipo.CategoryType.DG_OBJECTIVE.name, tipo.CategoryType.DG_OBJECTIVE.value),
        (tipo.CategoryType.INFORMATION_ASSET.name, tipo.CategoryType.INFORMATION_ASSET.value),
        (tipo.CategoryType.KPI.name, tipo.CategoryType.KPI.value),
        (tipo.CategoryType.POLICY.name, tipo.CategoryType.POLICY.value),
        (tipo.CategoryType.PROCEDURE.name, tipo.CategoryType.PROCEDURE.value),
        (tipo.CategoryType.PRINCIPLE.name, tipo.CategoryType.PRINCIPLE.value),
        (tipo.CategoryType.GLOSSARY_TERM.name, tipo.CategoryType.GLOSSARY_TERM.value),
        (tipo.CategoryType.GLOSSARY_TERM.name, tipo.CategoryType.GLOSSARY_TERM.value)
    ],
        string="Tipo de categoría", required=True)

    _sql_constraints = [  # los check o unique
        ('name_unique', 'unique(name)', 'El atributo "Nombre" (name) debe ser único')
    ]

    # que la generada por el sistema no se pueda modificar ni borrar
    @api.onchange('name', 'description')
    def check_no_actualizar(self):
        nombre = 'Medida de calidad de datos'
        desc = 'Categoría generada por el sistema exclusivamente para las métricas de calidad de datos. ' \
               'No se puede modificar.'
        # para que no salga al crearlo
        if self.name == nombre or self._origin.name == nombre:
            if self.description != desc or self.name != nombre:
                raise UserError("No se puede modificar esta categoría predefinida por el sistema.")

    def unlink(self):
        for record in self:
            if record.name == 'Medida de calidad de datos':
                raise UserError("No se puede borrar esta categoría.")
        return super(Category, self).unlink()

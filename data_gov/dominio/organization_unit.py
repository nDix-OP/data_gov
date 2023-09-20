from odoo import fields, models


class OrganizationUnit(models.Model):
    # nombre de la tabla de la BD (convierte . a _)
    _name = "datagov.organization.unit"
    _description = "Unidad de organización, se usa para el actor"

    # Decir que atributo se usa en los dropdown para buscar cuando se use como FK (como org del actor)
    # Por defecto es 'name' y por eso no hay que tocarlo en otros objetos como actor
    # _rec_name = 'organizName'

    id = fields.Id("Id", required=True)
    name = fields.Text("Nombre", required=True)
    description = fields.Text("Descripción", required=True)

    _sql_constraints = [  # los check o unique
        ('name_unique', 'unique(name)', 'El atributo "Nombre" (name) debe ser único')
    ]

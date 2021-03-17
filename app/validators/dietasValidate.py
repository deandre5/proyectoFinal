from marshmallow import Schema, fields, validate


class CreateDietSchema(Schema):
    """
    paremeters:
    -nombre (string)
    -categoria (string)
    -descripcion (string)
    """

    nombre = fields.String(required=True, validate=validate.Length(min=1, max=50), data_key='nombre')
    categoria = fields.String(required=True, validate=validate.OneOf(['aumento de masa muscular', 'bajar de peso']), data_key='categoria')
    descripcion = fields.String(required=True, validate=validate.Length(min=1,max=20000), data_key='descripcion')
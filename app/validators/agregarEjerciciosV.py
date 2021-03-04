from marshmallow import Schema, fields, validate


class CreateExerciseSchema(Schema):
    """
    parameters:
     -nombre (str)
     -descripcion (str)
     -imagen (str)
     -tipo (str)
    """

    nombre = fields.String(required=True, validate=validate.Length(
        min=1, max=45), data_key='nombre')

    descripcion = fields.String(required=True, validate=validate.Length(
        min=1, max=258), data_key='descripcion')

    # imagen = fields.String(required=True, validate=validate.Length(
    # min=1, max=258), data_key='imagen')

    tipo = fields.String(required=True, validate=validate.Length(
        min=1, max=45), data_key='tipo')

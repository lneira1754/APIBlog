from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6), load_only=True)
    role = fields.Str(dump_only=True)
    is_active = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

class UserUpdateSchema(Schema):
    username = fields.Str(validate=validate.Length(min=3, max=100))
    email = fields.Email()
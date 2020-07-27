from wtforms import Form, BooleanField, StringField, PasswordField, validators, FloatField, IntegerField, ValidationError
from wtforms.widgets import TextArea


class Require_Specific_Radio(object):
    def __init__(self, other_field, message = None):
        self.other_field_name = other_field
        if not message:
            message = "Please give correct input"
        self.message = message

    def __call__(self, form, field):
        other_field = form.get(self.other_field_name)
        print other_field
        if other_field == None or other_field == '':
            raise ValidationError()


class Required_If(object):
    def __init__(self, other_field, message = None):
        self.other_field_name = other_field
        if not message:
            message = "Please fill out all fields"
        self.message = message

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field == None:
            raise ValidationError(self.message)


class Valid_Pep_Seq(object):
    valid_pep = ['A','R', 'N', 'D', 'C', 'E', 'Q', 'G','H','I','L','K','M', 'F','P', 'S','T','W','Y','V' ]
    def __init__(self, message = None):
        if not message:
            message = "Please input valid protein sequence"
        self.message = message

    def __call__(self, form, field):
        data = field.data
        if not self.correct_input(data):
            raise ValidationError(self.message)

    def correct_input(self, data):
        for val in data:
            try:
                if val.upper() in self.valid_pep:
                    pass
                else:
                    raise ValidationError(self.message)
            except (AttributeError):
                raise ValidationError(self.message)
        return True


class Valid_Nuc_Seq(object):
    valid_nuc = ['A','T','G','C']
    def __init__(self, message = None):
        if not message:
            message = "Invalide DNA Sequence"
        self.message = message

    def __call__(self, form, field):
        data = field.data
        if not self.correct_input(data):
            raise ValidationError(self.message)

    def correct_input(self, data):
        for val in data:
            try:
                if val.upper() in self.valid_nuc:
                    pass
                else:
                    raise ValidationError(self.message)
            except(AttributeError):
                raise ValidationError(self.messages)
        return True


class Valid_Tree(object):
    def __init__(self, type ,message = None):
        if not message:
            message = "Invalide Sequence"
        self.message = message
        self.type = type

        def __call__(self, form, field):
            data = field.data
            if self.type == "pep":
                if not Valid_Pep_Seq.correct_input(data):
                    raise ValidationError(self.message)
            else:
                if not Valid_Nuc_Seq.correct_input(data):
                    raise ValidationError(self.message)

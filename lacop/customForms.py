from wtforms import Form, validators, FloatField, RadioField


class LacopForm(Form):
    """
    Form validation class for the lactose operon webpage form input. The lacOp Lab webpage
    contains one form that has 3 Float Fields, and 11 checkbox (or BooleanField) inputs. The 3
    FloatFields must be filled out, but only certain BooleanField must be true or checked. Floats
    cannot be greater than 1000 or less than 0. If the form is valid it will return true.
    """

    #TODO build a internal validation

    def __init__(self):
        fields = {
            'allo': FloatField('Allolactose', validators=[validators.input_required()], default=0),
            'lac_out': FloatField('Lactose Outside', validators=[validators.input_required()], default=200),
            'lac_in': FloatField('Lactose Inside', validators=[validators.input_required()], default=0),
            'glucose': FloatField('Glucose', validators=[validators.input_required()], default=0),
            'promoter': RadioField('Promoter', choices=['none', 'lacP-']),
            'operator': RadioField('Operator', choices=['none', 'lacOc']),
            'repressor': RadioField('Repressor', choices=['none', 'lacI-', 'lacIs']),
            'permease': RadioField('Permease', choices=['none', 'lacY-']),
            'bgal': RadioField('Beta-Galactasidase', choices=['none', 'lacZ-']),
            'cap_camp': RadioField('CAP-cAMP', choices=[('Inactive', 'Active')])
        }

    def validate(self):
        for val in self.data:
            if val != "plasmid_option":
                if type(self.data[val]) != type(0.0) or self.data[val] < 0.0:
                    return False
        return True

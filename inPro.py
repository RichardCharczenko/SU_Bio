from wtforms import Form, BooleanField, StringField, PasswordField, validators

class ValidatedLO(Form):
  ConcentrationA = StringField('allo', [validators.Length(min=1, max=4)])
  ConcentrationI = StringField('lacIn', [validators.])
  ConcentrationO =

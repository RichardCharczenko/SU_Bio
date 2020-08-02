from flask import Flask, render_template, request, url_for
from wtforms import Form, BooleanField, StringField, PasswordField, validators, FloatField, IntegerField, \
    ValidationError, RadioField
from wtforms.widgets import TextArea

from customValidation import Required_If, Valid_Pep_Seq, Valid_Nuc_Seq, Require_Specific_Radio
from fase import main_fase
from faseTree import main_tree


class FaseProteinForm(Form):
    """ Form validation for the FaSe webpage input """
    divergence = IntegerField('Divergence', validators=[Required_If('OutPerIns'), Required_If('sequence'),
                                                        validators.NumberRange(min=10, max=100)])
    OutPerIns = IntegerField('Out sequences per In sequence',
                             validators=[Required_If('divergence'), Required_If('sequence')])
    sequence = StringField('Sequence', widget=TextArea(),
                           validators=[Valid_Pep_Seq(), Required_If('divergence'), Required_If('OutPerIns')])


class FaseDNAForm(Form):
    """ Form validation for the FaSe webpage input """
    divergenceN = IntegerField('Divergence', validators=[Required_If('OutPerInsN'), Required_If('sequenceNuc'),
                                                         validators.NumberRange(min=10, max=100)])
    OutPerInsN = IntegerField('Out sequences per In sequence',
                              validators=[Required_If('divergenceN'), Required_If('sequenceNuc')])
    sequenceNuc = StringField('Sequence', widget=TextArea(),
                              validators=[Valid_Nuc_Seq(), Required_If('divergenceN'), Required_If('OutPerInsN')])


class Fase_Form(Form):
    """Form validation for fase"""
    generation_type = RadioField('Generation Type', choices=[('Phylogentic Tree', 'Phylogentic Tree'),
                                                             ('Sequence Mutator', 'Sequence Mutator')],
                                 validators=[Required_If('divergence'), Required_If('sequence'),
                                             Required_If('MaxChildren')])
    seq_type = RadioField('Sequence Type', choices=[('Peptide', 'Peptide'), ('Nucleotide', 'Nucleotide')],
                          validators=[Required_If('divergence'), Required_If('sequence'), Required_If('MaxChildren')])
    sequence = StringField(u'Sequence', widget=TextArea(),
                           validators=[Required_If('divergence'), Required_If('MaxChildren')])
    divergence = IntegerField('Percent Divergence', validators=[Required_If('MaxChildren'), Required_If('sequence'),
                                                                validators.NumberRange(min=10, max=100)])
    MaxChildren = IntegerField('Max children per parent',
                               validators=[Required_If('divergence'), Required_If('sequence')])


class fase_tree_form(Form):
    """Form validation for the phylogentic tree inputs on the FaSe webpage"""
    tree_seq_type = RadioField('Sequence Type', choices=[('Peptide', 'Peptide'), ('Nucleotide', 'Nucleotide')],
                               validators=[Required_If('tree_divergence'), Required_If('tree_sequence'),
                                           Required_If('tree_MaxChildren')])
    tree_sequence = StringField(u'Sequence', widget=TextArea(),
                                validators=[Required_If('tree_divergence'), Required_If('tree_MaxChildren')])
    tree_divergence = IntegerField('Percent Divergence',
                                   validators=[Required_If('tree_MaxChildren'), Required_If('tree_sequence'),
                                               validators.NumberRange(min=10, max=100)])
    tree_MaxChildren = IntegerField('Max children per parent',
                                    validators=[Required_If('tree_divergence'), Required_If('tree_sequence')])


def fase_form():
    """
    Handles POST and GET URL request for FaSe webpage, form data is validated
    and if form is valid, FaSe program is run under user specified conditions.
    """
    fase_form = Fase_Form(request.form)
    dataPep = ""
    dataNuc = ""

    if fase_form.validate():
        sequence_type = request.form.get('seq_type')[:3].lower()
        sequence = request.form.get('sequence')

        if request.form.get('generation_type') == 'Phylogentic Tree':
            data = main_tree(sequence, sequence_type, int(request.form.get('MaxChildren')),
                             float(request.form.get('divergence')))
            return render_template('fase.html', dataTree=data[0], dataSeq=data[1], f_form=fase_form, dataM=None)
        else:
            data = main_fase(sequence, float(request.form.get("divergence")), sequence_type,
                             float(request.form.get('MaxChildren')))
            return render_template('fase.html', dataM=data, f_form=fase_form, dataTree=None)
    return render_template('fase.html', f_form=fase_form)

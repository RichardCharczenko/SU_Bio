from flask import Flask, render_template, request  # Common to all flaskr files
from wtforms import Form, validators, FloatField, RadioField
import pygal
import os
from LacOp import RunLO  # Lactose Webpage backend program

PNG_FOLDER = os.path.join('static', 'images')
application = app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PNG_FOLDER


class lacopForm(Form):
    """
    Form validation class for the lactose operon webpage form input. The lacOp Lab webpage
    contains one form that has 3 Float Fields, and 11 checkbox (or BooleanField) inputs. The 3
    FloatFields must be filled out, but only certain BooleanField must be true or checked. Floats
    cannot be greater than 1000 or less than 0. If the form is valid it will return true.
    """

    #TODO build a internal validation

    ALLO = FloatField('Allolactose', validators=[validators.input_required()], default=0)
    LO = FloatField('Lactose Outside', validators=[validators.input_required()], default=200)
    LI = FloatField('Lactose Inside', validators=[validators.input_required()], default=0)
    GLU = FloatField('Glucose', validators=[validators.input_required()], default=0)

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

    plasmid_option = RadioField('Optional plasmid', choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def validate(self):
        for val in self.data:
            if val != "plasmid_option":
                if type(self.data[val]) != type(0.0) or self.data[val] < 0.0:
                    return False
        return True


def build_mut_list():
    """
    properly formats form data into a list that can be passed
    into lacoperon function
    """
    mutL = []
    plasmid = []
    for item in request.form:
        if item[:2] == 'p_':
            plasmid.append(item)
            pass
        else:
            mutL.append(item)
    return mutL, plasmid


def generate_title(list):
    """Generates a graph title for lacop Webpage graphical dsiplay. The title is based
    on user given input"""
    title = ''
    for item in list:
        if item != 'none' and item != 'Inactive':
            if item != 'Active':
                title = title + ' ' + item + ','
        if item == 'Inactive' or item == 'Active':
            title = title + ' CAP-' + item + ','
    if title != '' and title[-1] == ',':
        title = title[0:-1]
    if title == '':
        title = 'Wild Type'
    return title


def format_legend(labels, values, plasmid):
    """

    :param plasmid: a dictionary of mutaions
    """
    sorted = {"Sugar Concentration": [], "Lactose Operon": [], "Plasmid": plasmid}
    plasmid_legend = {"Promoter": None,
                      "Operator": None,
                      "Repressor": None,
                      "Permease": None,
                      "Beta-Galactasidase": None}
    if plasmid:
        plasmid = plasmid.mut
        for mutation in plasmid:
            if mutation == "RepMutation":
                if plasmid[mutation] == 'lacIs':
                    plasmid_legend["Repressor"] = "Super Repressor"
                elif plasmid[mutation]:
                    plasmid_legend["Repressor"] = "No Repressor"
            if not plasmid[mutation]:
                if mutation == "ProMutation":
                    plasmid_legend["Promoter"] = "Present"
                if mutation == "RepMutation":
                    plasmid_legend["Repressor"] = "Functional wildtype present"
                if mutation == "BgalMutation":
                    plasmid_legend["Beta-Galactasidase"] = "Present"
                if mutation == "OpMutation":
                    plasmid_legend["Operator"] = "Present"
                if mutation == "PermMutation":
                    plasmid_legend["Permease"] = "Present"
    sorted["Plasmid"] = plasmid_legend
    for item in values:
        sorted["Sugar Concentration"].append(values[item][0])
    for item in labels:
        if item != "ALLO" and item != "GLU" and item != "LI" and item != "LO":
            sorted["Lactose Operon"].append(item)
    return sorted


def plasmid_present():
    for item in request.form:
        if item == "plasmid-present":
            return True
    return False


def lacop_form():
    """
    Handles URL request to lacop Lab webpage, there IS formdata gatherered from
    one form on the LacOp lab. The data is validated and if valid, the lactose
    operon program is run using user specified data
    """
    form = lacopForm(request.form)
    image_file = os.path.join(app.config['UPLOAD_FOLDER'], 'LacOp_img.png')
    lesson_file = os.path.join(app.config['UPLOAD_FOLDER'], 'LacOP_Web_Lab.docx')
    form_warning = ''

    if request.method == "POST" and form.validate():
        form_data = build_mut_list()
        if "plasmist=present" in request.form:
            cell = RunLO(form_data[0], form_data[1], int(request.form.get('ALLO')), int(request.form.get('LI')),
                         int(request.form.get('LO')), int(request.form.get('GLU')))
        else:
            cell = RunLO(form_data[0], [], int(request.form.get('ALLO')), int(request.form.get('LI')),
                         int(request.form.get('LO')), int(request.form.get('GLU')))
        concentration_dict = cell.archiveConditions

        try:
            graph = pygal.XY(x_title='Psuedo Seconds', y_title='Molecular Units')
            graph.title = "Operon Graph"  # generateTitle(form_data[0])
            graph.x_labels = range(0, 401, 20)
            for item in concentration_dict:
                graph_points = []
                for index in range(len(concentration_dict[item])):
                    graph_points.append((index, concentration_dict[item][index]))
                if item == "allo":
                    item = 'Allolactose'
                if item == "lacIn":
                    item = 'Lactose Intracellular'
                if item == "lacOut":
                    item = 'Lactose Extracellular'
                if item == 'gulcose + galactose':
                    item = 'Glucose Inside Cell'
                if item == 'perm':
                    item = 'Permease'
                if item == 'bgal':
                    item = 'Beta-Galactasidase'
                graph.add(item, graph_points)
            graph_data = graph.render_data_uri()
            legend_data = format_legend(form_data[0], cell.archiveConditions, cell.plasmid_data)
            return render_template('lacop.html',
                                   graph_data=graph_data,
                                   form=form,
                                   user_image=image_file,
                                   is_valid=form_warning,
                                   legend=legend_data,
                                   lesson_file=lesson_file)
        except Exception, e:
            return (str(e))
    else:
        graph = pygal.Line()
        graph.title = 'Operon Graph'
        graph.x_labels = range(200)
        graph_data = graph.render_data_uri()
        plasmid_legend = {"Promoter": None,
                          "Operator": None,
                          "Repressor": None,
                          "Permease": None,
                          "Beta-Galactasidase": None}
        return render_template('lacop.html',
                               graph_data=graph_data,
                               form=form,
                               user_image=image_file,
                               is_valid=form_warning,
                               legend={"Sugar Concentration": [], "Lactose Operon": [], "Plasmid": plasmid_legend},
                               lesson_file=lesson_file)

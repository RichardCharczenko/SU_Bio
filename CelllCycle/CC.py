import os

from Prototype import main
from flask import Flask, render_template, request, url_for
import pygal

PNG_FOLDER = os.path.join('static', 'images')
application = app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PNG_FOLDER


def CC():
    ''' Handles general URL request for EVO webpage'''
    graph = pygal.Line()
    graph.title = "Cell Cycle graph"
    graph.x_labels = [0, 10, 20, 30, 40, 50, 60, 70]
    graph_data = graph.render_data_uri()
    return render_template('CC.html', graph_data=graph_data)


def CC_form():
    ''' Handles POST URL request for EVO webpage, form data is validated
    and if form is valid, EVO program is run under user specified conditions'''
    if request.method != 'POST':
        return CC()
    data = []

    if request.form.get('Scenario1'):  # p53 DNAdamage rB
        data = main(True, False, True)
    if request.form.get('Scenario2'):
        data = main(False, True, True)
    if request.form.get('Scenario3'):
        data = main(True, True, True)
    if request.form.get('Scenario4'):
        data = main(False, False, True)
    if request.form.get('Scenario5'):
        data = main(False, True, False)
    if request.form.get('Scenario6'):
        data = main(False, False, False)

    graph = pygal.Line(x_title='Hours since G0', y_title='Protein Activity')
    graph.title = "Cell Cycle"
    graph.x_labels = data[0]
    for i in range(len(data)):
        if i == 0:
            continue
        label = ''
        if i == 1:
            label = 'CyclinA'
        if i == 2:
            label = 'CyclinB'
        if i == 3:
            label = 'CyclinE'
        if i == 4:
            label = 'CyclinD'
        if i == 5:
            label = 'p53'
        if i == 6:
            label = 'rB'
        graph.add(label, data[i])
    graph_data = graph.render_data_uri()

    return render_template('CC.html', graph_data=graph_data)

from Evo import generate_scenario
from flask import Flask, render_template, request
import pygal
import os

PNG_FOLDER = os.path.join('static', 'images')
application = app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PNG_FOLDER


def evo():
    """ Handles general URL request for EVO webpage"""
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], '.png')
    evo_page_image = os.path.join(app.config['UPLOAD_FOLDER'], 'Evo_Image.png')
    lesson_file = os.path.join(app.config['UPLOAD_FOLDER'], 'EvoPopGen _Web_Lab.docx')

    graph = pygal.Line()
    graph.title = "Evo graph"
    graph.x_labels = [0, 10, 20, 30, 40, 50, 60, 70]
    graph_data = graph.render_data_uri()
    snow_melt_graph = pygal.Line()
    snow_melt_graph.title = "Climate"
    snow_melt_graph_data = snow_melt_graph.render_data_uri()
    return render_template('evo.html',
                           graph_data=graph_data,
                           snow_melt_graph=snow_melt_graph_data,
                           user_image=evo_page_image,
                           lesson_file=lesson_file)


def evo_form():
    """ Handles POST URL request for EVO webpage, form data is validated
    and if form is valid, EVO program is run under user specified conditions"""
    if request.method != 'POST':
        return evo()
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], '.png')
    evo_page_image = os.path.join(app.config['UPLOAD_FOLDER'], 'Evo_Image.png')
    lesson_file = os.path.join(app.config['UPLOAD_FOLDER'], 'EvoPopGen _Web_Lab.docx')

    if request.form.get('Scenario1'):
        data = generate_scenario(1)
    elif request.form.get('Scenario2'):
        data = generate_scenario(2)
    elif request.form.get('Scenario3'):
        data = generate_scenario(3)
    elif request.form.get('Scenario4'):
        data = generate_scenario(4)
    elif request.form.get('Scenario5'):
        data = generate_scenario(5)
    elif request.form.get('Scenario6'):
        data = generate_scenario(6)

    graph = pygal.Line(x_title='Time (years)', y_title='Allele frequency')
    graph.title = "Allele Frequency Over Time"
    reversed_data = data[0].reverse()
    graph.x_labels = range(0, 50, 10)  # data[0]
    graph.y_labels = 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0
    if request.form.get('Scenario1'):
        graph.add('A.Wk.' + str(data[-1][0]), data[2])
        graph.add('A.Wk.' + str(data[-1][1]), data[3])
        graph.add('A.Wk.' + str(data[-1][2]), data[4])
        graph.add('A.Wk.' + str(data[-1][3]), data[5])
    elif request.form.get('Scenario6'):
        graph.add('A.Wk.' + str(data[-1][0]), data[2])
        graph.add('A.Wk.' + str(data[-1][1]), data[3])
        graph.add('A.Wk.' + str(data[-1][2]), data[4])
        graph.add('A.Wk.' + str(data[-1][3]), data[5])
        # graph.add('A.Wk.' + str(data[-1][4]), data[6])
    else:
        graph.add('A.Wk.:' + str(data[-1][0]), data[2])
        graph.add('A.Wk.' + str(data[-1][1]), data[3])
        graph.add('A.Wk.' + str(data[-1][2]), data[4])
        graph.add('A.Wk.' + str(data[-1][3]), data[5])
    graph_data = graph.render_data_uri()

    snow_melt_graph = pygal.XY(x_title='Time (years)', y_title='Week of Snowmelt')
    snow_melt_graph.title = 'Climate'
    snow_melt_graph.y_labels = range(10, 30, 2)
    if request.form.get('Scenario6'):
        snow_melt_graph.x_labels = range(0, 50, 10)
        count = 0
        graph_points = []
        for item in data[1]:
            graph_points.append((count, item))
            count += 1
        snow_melt_graph.add('Climate', graph_points)
    else:
        snow_melt_graph.x_labels = range(0, 51, 10)
        count = 0
        graph_points = []
        for item in data[1]:
            graph_points.append((count, item))
            count += 1
        snow_melt_graph.add('Climate', graph_points)
    snow_melt_graph_data = snow_melt_graph.render_data_uri()
    return render_template('evo.html',
                           graph_data=graph_data,
                           snow_melt_graph=snow_melt_graph_data,
                           user_image=evo_page_image,
                           lesson_file=lesson_file)

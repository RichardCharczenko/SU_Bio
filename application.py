import os

from flask import Flask, render_template, request

from fase.faseApp import fase_form
from evo.EVO_App import evo, evo_form
from lacop.lacOp_App import lacop_form
from CellCycle.CC import CC_form


PROJECTS_FOLDERS = os.path.join('projects')
PNG_FOLDER = os.path.join('static', 'images')
application = app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PNG_FOLDER


@app.route('/')
def index_post():
    """
    Handles Homepage URL request, there is no form data from the Homepage
    """
    lacOp_page_image = os.path.join(app.config['UPLOAD_FOLDER'], 'perm_image.png')
    evo_page_image = os.path.join(app.config['UPLOAD_FOLDER'], 'Evo_Image.png')
    fase_page_image = os.path.join(app.config['UPLOAD_FOLDER'], 'DNA.png')
    return render_template('index.html', lacOpImg=lacOp_page_image, evoImg=evo_page_image, faseImg=fase_page_image)


@app.route('/about')
def about():
    """
    Handles about page URL request, there is no form data from about page,
    see inline description in HTML page for more information
    """
    return render_template('about.html')


@app.route('/lacop', methods=['POST', 'GET'])
def lacop_page():
    """
    Handles lacop page requests, only handles POST and GET requests
    """
    return lacop_form()


@app.route('/fase', methods = ['POST', 'GET'])
def fase_page():
    """
    Handles URL requests to fase_page, only intakes POST and GET requests
    """
    return fase_form()


@app.route('/evo', methods=['POST', 'GET'])
def run_evo():
    """
    Handles URL requests to evo, only intakes POST and GET requests
    """
    if request.method == 'POST':
        return evo_form()
    return evo()


@app.route('/CC', methods=['POST', 'GET'])
def run_CC():
    """
    Handles URL requests to CC page, only intakes POST and GET requests
    """
    return CC_form()


if __name__ == '__main__':
    #website_url = 'supergenetics.org'
    #app.config['SERVER_NAME'] = website_url
    app.run(debug=False)

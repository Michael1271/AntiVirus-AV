from flask import Flask, redirect, render_template, send_file
from Secret_Variables import secret_session_key

# A Flask (Framework of WEB Application) Program for AntiVirus AV Website. This script runs on replit.com
# link: https://AntiVirus-AV-Website.micha1245.repl.co

__author__ = 'Michael Khoshahang'

app = Flask(__name__)
app.secret_key = secret_session_key


@app.route('/')  # declaring that the https route is the main WEB page
def home():
    """
    The home function.
    :return: the home web page
    """
    return render_template('Home.html')


@app.route('/Downloads')
def downloads():
    """
    The downloads function.
    :return: the downloads web page
    """
    return render_template('Downloads.html')


@app.route('/DownloadVersion3.1')
def download_file():
    """
    The download_file function.
    :return: the download_file web page
    """
    return send_file("AntiVirus-AV.zip", as_attachment=True)


@app.route('/GitHub')
def git_hub():
    """
    The GitHub Function.
    :return: the GitHub web page
    """
    return redirect('https://github.com/Michael1271/AntiVirus-AV-Project')


@app.route('/Contact-Us')
def contact():
    """
    The contact function.
    :return: the Contact web page
    """
    return render_template('Contact-Us.html')


@app.route('/About')
def about():
    """
    The about function.
    :return: the About web page
    """
    return render_template('About.html')


@app.route('/Gmail')
def gmail():
    """
    The about function.
    :return: the user's Gmail web page
    """
    return redirect("mailto:antivirus.software.org@gmail.com")


@app.errorhandler(404)
def page_not_found(error):
    """
    The page not found function
    :param error: the error
    :return: Not found page
    """
    return render_template('NotFound.html'), 404


def run():
    """
    The function runs the application.
    :return: None
    """
    app.run(debug=True, host='0.0.0.0', port=8080)  # running the WEB page

from flask import Flask
import os

app = Flask(__name__)

import wolfdvd.views


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

app.config.update(dict(
  DATABASE = os.path.join(app.root_path, 'wolfdvd.db'),
  DEBUG = True,
  SECRET_KEY='development key',
  USERNAME ='admin',
  PASSWORD='default'
))
app.config.from_envvar('WOLFDVD_SETTINGS', silent=True)

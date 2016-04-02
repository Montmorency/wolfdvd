from flask import Flask
import os

app = Flask(__name__)

import wolfdvd.views

#@app.errorhandler(404)
#def not_found(error):
#    return render_template('404.html'), 404

app.config.update(dict(
  DATABASE = os.path.join(app.root_path, './static/tits_protected.pckl'),
  DEBUG = True,
  SECRET_KEY='development key',
  USERNAME ='isaiah',
  PASSWORD='berlin'
))

app.config.from_envvar('WOLFDVD_SETTINGS', silent=True)

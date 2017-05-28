from flask import Flask, render_template, request, session, redirect
import models
import os
from flask_sqlalchemy import SQLAlchemy
from get_info import get_plugins_dict

app = Flask(__name__)

# Config things
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, 'static/CSCDemo.db')

# Set up the SQLAlchemy DB config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(DB_PATH)
app.secret_key = 'Leeeeeerooooooooooooooy Jenkinsssssssssss'
db = SQLAlchemy(app)


@app.route('/', methods=["GET", "POST"])
def csc_demo():
    if 'reload' not in session:
        session['reload'] = False

    if session.get('reload'):
        session['reload'] = False
        _reload = True
    else:
        _reload = False

    return render_template('base.html', reload=_reload)


@app.route('/select_plugin', methods=['GET', 'POST'])
def select_plugin():

    name_query = models.PluginIds.query.all()
    name_list = []
    cnt = 0
    session['new_plugins'] = True
    for i in name_query:
        cnt += 1
        name_list.append(i.plugin_name)

    return render_template('select_plugin.html', names=name_list, list_len=cnt)


@app.route('/view_settings', methods=["GET", "POST"])
def settings():
    _plugins = request.values
    if session.get('new_plugins') is True:
        session['new_plugins'] = False
        names = []
        for i in _plugins:
            q = models.PluginIds.query.filter_by(plugin_name=i).first().plugin_name
            names.append(q)
    else:
        names = session.get('names')

    settings_dict = {}
    for i in names:
        settings_query = models.PluginSettings.query.filter_by(plugin_id=i).all()

        plugin_settings = {}
        for j in settings_query:
            plugin_settings[j.setting_name] = j.setting_value

        settings_dict[i] = plugin_settings

    session['names'] = names

    return render_template('view_settings.html', plugin_settings=settings_dict)


@app.route('/change_settings', methods=['GET', 'POST'])
def change_settings():

    names = session.get('names')

    settings_dict = {}
    for i in names:
        settings_query = models.PluginSettings.query.filter_by(plugin_id=i).all()

        plugin_settings = {}
        for j in settings_query:
            plugin_settings[j.setting_name] = j.setting_value

        settings_dict[i] = plugin_settings

    return render_template('change_settings.html', plugin_settings=settings_dict, names=names)


@app.route('/_update', methods=["GET", "POST"])
def _update():
    this = request.values
    names = session.get('names')

    for i in names:

        for j, v in this.items():
            _q = models.PluginSettings.query.filter_by(plugin_id=i, setting_name=j).first()
            if _q is not None:
                q = models.PluginSettings.query.filter_by(plugin_id=i, setting_name=j).first()
                q.setting_value = v
                models.db.session.commit()

    return redirect('/view_settings')


@app.route('/_initialise', methods=['GET', 'POST'])
def _initialise():
    plugin_dict = get_plugins_dict()
    models.db.drop_all()
    models.db.create_all()
    for name in plugin_dict:
        p_name = models.PluginIds(plugin_name=name)
        models.db.session.add(p_name)
        models.db.session.commit()

        _plugin_id = models.PluginIds.query.filter_by(plugin_name=name).first()
        if _plugin_id is not None:
            plugin_id = _plugin_id.plugin_name

            for setting_name in plugin_dict[name]:
                setting_value = plugin_dict[name][setting_name]
                s = models.PluginSettings(plugin_id=plugin_id, setting_name=setting_name, setting_value=setting_value)
                models.db.session.add(s)
                models.db.session.commit()
    session['reload'] = True
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=False)

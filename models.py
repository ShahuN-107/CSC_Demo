from csc_demo import db


# Model for the plugin ID table
class PluginIds(db.Model):
    __tablename__ = "plugin_ids"
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    plugin_name = db.Column('plugin_name', db.Text)


# Model for the plugin settings table
class PluginSettings(db.Model):
    __tablename__ = "plugin_settings"
    setting_id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    setting_name = db.Column('name', db.Text)
    setting_value = db.Column('value', db.Float)
    plugin_id = db.Column('plugin_id', db.ForeignKey('plugin_ids.plugin_name', ondelete="CASCADE", onupdate="CASCADE"))

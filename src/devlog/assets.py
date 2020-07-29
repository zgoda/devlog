from flask_assets import Bundle

app_css = Bundle(
    'css/app.scss', filters='node-scss', output='dist/app.css',
)

all_css = Bundle(
    app_css, 'vendor/normalize.css', 'css/pgm_friendly.css', filters='cleancss',
    output='dist/all.%(version)s.min.css',
)

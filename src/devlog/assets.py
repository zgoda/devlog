from flask_assets import Bundle

app_css = Bundle(
    'css/app.scss', filters='scss', output='dist/app.css',
)

all_css = Bundle(
    'vendor/normalize.css', 'css/pgm_friendly.css', app_css, filters='cleancss',
    output='dist/all.%(version)s.min.css',
)

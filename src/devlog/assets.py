from flask_assets import Bundle

mustard_css = Bundle(
    'vendor/mustard/scss/mustard-ui.scss',
    filters='node-scss', output='dist/mustard-ui.css',
)

all_css = Bundle(
    mustard_css, 'vendor/normalize.css', 'css/app.css', 'css/pgm_friendly.css',
    filters='cleancss', output='dist/all.%(version)s.min.css'
)

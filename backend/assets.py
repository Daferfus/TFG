"""Compile static assets."""
from flask import current_app as app
from flask_assets import Bundle


def compile_static_assets(assets):
    """Create stylesheet bundles."""
    assets.auto_build: bool = True
    assets.debug: bool = False
    common_style_bundle: Bundle = Bundle(
        'src/less/*.less',
        filters='less,cssmin',
        output='dist/css/style.css',
        extra={'rel': 'stylesheet/less'}
    )
    usuaris_style_bundle: Bundle = Bundle(
        'usuaris_bp/src/less/usuaris.less',
        filters='less,cssmin',
        output='dist/css/usuaris.css',
        extra={'rel': 'stylesheet/less'}
    )
    alumnes_style_bundle: Bundle = Bundle(
        'alumnes_bp/src/less/alumnes.less',
        filters='less,cssmin',
        output='dist/css/alumnes.css',
        extra={'rel': 'stylesheet/less'}
    )
    professors_style_bundle = Bundle(
        'professors_bp/src/less/professors.less',
        filters='less,cssmin',
        output='dist/css/professors.css',
        extra={'rel': 'stylesheet/less'}
    )
    # empreses_style_bundle = Bundle(
    #     'empreses_bp/src/less/empreses.less',
    #     filters='less,cssmin',
    #     output='dist/css/empreses.css',
    #     extra={'rel': 'stylesheet/less'}
    # )
    assignacions_style_bundle = Bundle(
        'assignacions_bp/src/less/assignacions.less',
        filters='less,cssmin',
        output='dist/css/assignacions.css',
        extra={'rel': 'stylesheet/less'}
    )
    assets.register('common_style_bundle', common_style_bundle)
    assets.register('usuaris_style_bundle', usuaris_style_bundle)
    assets.register('alumnes_style_bundle', alumnes_style_bundle)
    assets.register('professors_style_bundle', professors_style_bundle)
    # assets.register('empreses_style_bundle', empreses_style_bundle)
    assets.register('assignacions_style_bundle', assignacions_style_bundle)
    if app.config['FLASK_ENV'] == 'development':
        common_style_bundle.build()
        usuaris_style_bundle.build()
        alumnes_style_bundle.build()
        professors_style_bundle.build()
        # empreses_style_bundle.build()
        assignacions_style_bundle.build()
    return assets
def register_controllers(app):
    from controllers.contracts import bp as contracts_bp
    app.register_blueprint(contracts_bp, url_prefix='/api/v1/contracts')

    from controllers.files import bp as files_bp
    app.register_blueprint(files_bp, url_prefix='/api/v1/files')

from flask import request, jsonify

from services.process_files_service import ProcessFilesService
from controllers.files import bp


@bp.route('/upload', methods=['POST'])
def upload():
    try:
        user_uuid = request.form.get('user_uuid')
        files = request.files.getlist('files')

        if not user_uuid:
            return jsonify({"error": "No user UUID provided"}), 400

        if not files:
            return jsonify({"error": "No files provided"}), 400

        files_service = ProcessFilesService()

        for file in files:
            files_service.upload_file(file, user_uuid)

        return jsonify({"files": files_service.to_json()}), 200
    except Exception as e:
        return jsonify({"error": f"Something went wrong: {e}"}), 500


@bp.route('/delete', methods=['DELETE'])
def delete():
    try:
        blob_name = request.args.get('blob_name')

        if not blob_name:
            return jsonify({"error": "No blob name provided"}), 400

        files_service = ProcessFilesService()
        files_service.delete_file(blob_name)

        return jsonify({"message": "Successfully deleted"}), 200
    except Exception as e:
        return jsonify("error", f"Something went wrong: {e}"), 500

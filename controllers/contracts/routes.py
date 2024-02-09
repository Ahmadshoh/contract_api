from multiprocessing import Pool

from flask import request, jsonify
from typing import List

from services.process_files_service import ProcessFilesService
from services.gpt_service import GPTService
from controllers.contracts import bp
from contract_manager.models import Contract
from services.firebase_service import FirebaseService

gpt_service = GPTService()


@bp.route('/analyze', methods=['POST'])
def analyze_contract():
    try:
        user_uuid = request.form.get('user_uuid')
        files = request.files.getlist('files')

        if not user_uuid:
            return jsonify({"error": "No user UUID provided"}), 400

        if not files:
            return jsonify({"error": "No files provided"}), 400

        firebase_service = FirebaseService(user_uuid)
        files_service = ProcessFilesService()

        for file in files:
            files_service.upload_file(file, user_uuid)

        text_chunks = chunk_text(files_service.text)

        with Pool() as pool:
            parsed_responses = pool.map(process_chunk, text_chunks)

        parsed = combine_parsed_responses(parsed_responses)

        company = parsed.model_dump().get('company')
        company_data = {
            "name": company.get('name'),
            "street": company.get('street'),
            "postcode": company.get('postcode'),
            "city": company.get('city'),
            "country": company.get('country'),
            "phone": company.get('phone'),
            "email": company.get('email')
        }

        company = firebase_service.company.find_or_create_by('name', company.get('name'), company_data)

        contract_data = {
            'title': parsed.model_dump().get('title'),
            'contract_number': parsed.model_dump().get('contract_number'),
            'client_number': parsed.model_dump().get('client_number'),
            'effective_date': parsed.model_dump().get('effective_date'),
            'expiration_date': parsed.model_dump().get('expiration_date'),
            'payment_details': parsed.model_dump().get('payment_details'),
            'company_ref': company.id,
        }

        return jsonify({
            "contracts": contract_data,
            "files": files_service.to_json()
        }), 200
    except Exception as e:
        return jsonify({"error": f"Something went wrong: {e}"}), 500


def process_chunk(chunk):
    _input = gpt_service.prompt.format_prompt(contract_data=chunk)
    output = gpt_service.model(_input.to_messages())
    return gpt_service.parser.parse(output.content)


def chunk_text(text, chunk_size=8000):
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks


def combine_parsed_responses(parsed_responses: List[Contract]) -> Contract:
    combined_response = Contract()

    for response in parsed_responses:
        for field_name, field_value in response.model_dump().items():
            if field_value not in (None, 'Not found'):
                setattr(combined_response, field_name, field_value)

    return combined_response

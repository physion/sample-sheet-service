import falcon
import svc.illumina as illumina

from falcon.media.validators import jsonschema


SAMPLE_SHEET_REQ_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://ovation.io/sample.sheet.generation.request.schema.json",
    "type": "object",
    "properties": {
        "workflow_activity": {
            "type": "object",
            "properties": {
                "id": {"type": "number"},
                "custom_attributes": {
                    "type": "object"
                },
                "workflow": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "number"},
                        "samples": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "number"},
                                    "identifier": {"type": "string"},
                                    "control": {"type": "boolean"},
                                    "date_received": {"type": "string"},
                                    "custom_attributes": {"type": "object"},
                                    "sample_states": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "number"},
                                                "position": {"type": "string"},
                                                "pool_index": {"type": "string"}
                                            }
                                        }
                                    },
                                    "requisition": {"type": "object"},
                                    "patient": {"type": "object"},
                                    "physician": {"type": "object"},
                                    "workflow_sample_results": {
                                        "type": "array",
                                        "items": {
                                            "type": "object"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "required": ["workflow_activity"]
}


class IlluminaSampleSheet(object):
    @jsonschema.validate(SAMPLE_SHEET_REQ_SCHEMA)
    def on_post(self, req, resp, **claims):
        body = req.media

        resp.media = illumina.generate_sample_sheet(body)

        resp.status = falcon.HTTP_CREATED


class StatusResource:
    def on_get(self, req, resp):
        """Handles GET requests"""

        response_body = {
            'status': 'alive'
        }

        resp.media = response_body
        resp.status = falcon.HTTP_OK

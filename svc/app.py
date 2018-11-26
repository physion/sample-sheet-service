import falcon
import json
import base64
import encodings
import io

import svc.illumina as illumina

from importlib import resources
from falcon.media.validators import jsonschema

UTF8 = encodings.utf_8.getregentry().name

with resources.open_text("svc", "post.schema.json") as fid:
    SAMPLE_SHEET_REQ_SCHEMA = json.load(fid)


class IlluminaSampleSheet(object):
    @jsonschema.validate(SAMPLE_SHEET_REQ_SCHEMA)
    def on_post(self, req, resp, **claims):
        body = req.media

        sample_sheet = illumina.make_sample_sheet(body)

        sample_sheet_csv = illumina.to_csv(sample_sheet)
        encoded_sample_sheet_bytes = base64.encodebytes(sample_sheet_csv.encode(UTF8))

        response = {
            "resources": [{
                "resource_name": "sample_sheet.csv",
                "content": encoded_sample_sheet_bytes,
                "label": "sample-sheet"
            }]
        }

        resp.media = response
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_CREATED


class StatusResource:
    def on_get(self, req, resp):
        """Handles GET requests"""

        response_body = {
            'status': 'alive'
        }

        resp.media = response_body
        resp.status = falcon.HTTP_OK

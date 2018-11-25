import falcon
import json
import svc.illumina as illumina

from importlib import resources
from falcon.media.validators import jsonschema


with resources.open_text("svc", "post.schema.json") as fid:
    SAMPLE_SHEET_REQ_SCHEMA = json.load(fid)


class IlluminaSampleSheet(object):
    @jsonschema.validate(SAMPLE_SHEET_REQ_SCHEMA)
    def on_post(self, req, resp, **claims):
        body = req.media

        resp.body = illumina.make_sample_sheet_json(body)

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

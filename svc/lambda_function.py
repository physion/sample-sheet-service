import base64
import logging
import json

import svc.illumina as illumina
import svc.constants as constants

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, _):
    logging.debug(event)

    sample_sheet = illumina.make_sample_sheet(event, adapter_result_type='library-adapter-barcode')

    sample_sheet_csv = illumina.to_csv(sample_sheet)
    encoded_sample_sheet_bytes = base64.encodebytes(sample_sheet_csv.encode(constants.UTF8))

    response = {
        "resources": [{
            "resource_name": "sample_sheet.csv",
            "content": encoded_sample_sheet_bytes.decode(constants.UTF8),
            "label": "sample-sheet"
        }]
    }

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

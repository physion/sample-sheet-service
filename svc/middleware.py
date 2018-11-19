import logging

logger = logging.getLogger('middleware')


class RequestLoggerMiddleware(object):
    def process_resource(self, req, resp, resource, params):
        logger.info('{}\t{}://{}/{}\t{}\t{}'.format(req.method,
                                                   req.forwarded_scheme,
                                                   req.forwarded_host,
                                                   req.relative_uri,
                                                   params,
                                                   req.media))

    def process_response(self, req, resp, resource, req_succeeded):
        logger.info('{}\t{}://{}/{}\t{}'.format(req.method,
                                                req.forwarded_scheme,
                                                req.forwarded_host,
                                                req.relative_uri,
                                                req_succeeded))

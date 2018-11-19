import falcon
import svc.app as app
import svc.middleware as middleware
import sv.config as config

from falcon_jwt_checker import JwtChecker

jwt_checker = JwtChecker(
    secret=config.secret('JWT_SECRET'), # May be a public key
    algorithm='HS256',
    exempt_routes=['/auth','/healthz'], # Routes listed here will not require a jwt
    exempt_methods=['OPTIONS'], # HTTP request methods listed here will not require a jwt
    audience=config.secret('JWT_AUDIENCE'),
    leeway=30
)


def make_system():
    application = falcon.API(middleware=[
        middleware.RequestLoggerMiddleware(),
        jwt_checker])

    application.add_route('/healthz', app.StatusResource())
    application.add_route('/api/v1/illumina', app.IlluminaSampleSheet())

    return application

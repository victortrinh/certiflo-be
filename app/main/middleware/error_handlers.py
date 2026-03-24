import logging
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'status': 'fail', 'message': 'Bad request.'}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'status': 'fail', 'message': 'Unauthorized.'}), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'status': 'fail', 'message': 'Forbidden.'}), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'status': 'fail', 'message': 'Resource not found.'}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'status': 'fail', 'message': 'Method not allowed.'}), 405

    @app.errorhandler(429)
    def rate_limited(error):
        return jsonify({'status': 'fail', 'message': 'Too many requests. Please try again later.'}), 429

    @app.errorhandler(SQLAlchemyError)
    def handle_db_error(error):
        logger.error(f'Database error: {error}')
        return jsonify({'status': 'fail', 'message': 'A database error occurred.'}), 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        logger.error(f'Unexpected error: {error}', exc_info=True)
        return jsonify({'status': 'fail', 'message': 'An unexpected error occurred.'}), 500

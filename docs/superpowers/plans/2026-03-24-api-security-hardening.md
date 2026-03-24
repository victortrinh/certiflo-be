# API Security Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Harden the certiflo-be Flask API against OWASP Top 10 API vulnerabilities without breaking production.

**Architecture:** Add security layers incrementally — fix existing bugs first, then add security headers, tighten CORS, add rate limiting, improve error handling, and add auth to unprotected endpoints. Each task is independently deployable.

**Tech Stack:** Flask 3.x, Flask-RESTX, Flask-Limiter (new), SQLAlchemy 2.x, PyJWT 2.8, Flask-Bcrypt, Flask-CORS

---

## File Map

| File | Action | Responsibility |
|------|--------|---------------|
| `app/main/model/user.py` | Modify | Add missing `decode_auth_token()`, refactor `is_valid_token`, use `current_app` for key |
| `app/main/service/auth_service.py` | Modify | Fix error handling, remove bare `print()` |
| `app/main/service/blacklist_service.py` | Modify | Fix error response (exception not serializable) |
| `app/__init__.py` | Modify | Fix broken `after_request`, tighten CORS |
| `app/main/__init__.py` | Modify | Add security headers, register error handlers, initialize rate limiter, prod validation |
| `app/main/config.py` | Modify | Add CORS origins, remove module-level `key` |
| `app/main/controller/file_controller.py` | Modify | Add auth to all endpoints, add file size limit |
| `requirements.txt` | Modify | Add Flask-Limiter |
| `app/main/middleware/__init__.py` | Create | Empty init |
| `app/main/middleware/rate_limiter.py` | Create | Rate limiter setup |
| `app/main/middleware/error_handlers.py` | Create | Global error handlers |

---

### Task 1: Fix Missing `decode_auth_token()`, Use `current_app` for JWT Key

**Why:** `auth_service.py:60` and `:81` call `User.decode_auth_token()` which doesn't exist — logout and `get_logged_in_user()` throw `AttributeError`. Additionally, `config.py:50` has `key = Config.SECRET_KEY` evaluated at import time, meaning JWT operations always use the base class fallback key regardless of which config is active. Must switch to `current_app.config['SECRET_KEY']`.

**Files:**
- Modify: `app/main/model/user.py`
- Modify: `app/main/config.py:50` (delete `key = Config.SECRET_KEY`)

- [ ] **Step 1: Remove module-level `key` from `config.py`**

Delete line 50 from `app/main/config.py`:
```python
# DELETE this line:
key = Config.SECRET_KEY
```

- [ ] **Step 2: Rewrite `user.py` to use `current_app`, add `decode_auth_token`, DRY `is_valid_token`**

Replace the full `app/main/model/user.py`:

```python
import jwt
import datetime
from flask import current_app
from .. import db, flask_bcrypt
from app.main.model.blacklist import BlacklistToken


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    registered_on = db.Column(db.DateTime, nullable=False)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(user_id):
        """Generates the Auth Token. Returns string token or Exception."""
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config['SECRET_KEY'],
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token.
        :return: integer (user_id) or string (error message)
        """
        try:
            payload = jwt.decode(
                auth_token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    @staticmethod
    def is_valid_token(auth_token):
        result = User.decode_auth_token(auth_token)
        return not isinstance(result, str)
```

- [ ] **Step 3: Verify logout works manually or via test**

Test with: `curl -X POST http://localhost:5000/api/auth/logout -H "Authorization: Bearer <token>"`
Expected: `{"status": "success", "message": "Successfully logged out."}`

- [ ] **Step 4: Commit**

```bash
git add app/main/model/user.py app/main/config.py
git commit -m "fix: add decode_auth_token, use current_app for JWT key instead of module-level import"
```

---

### Task 2: Fix Broken `after_request` Decorator and Blacklist Service Error

**Why:** In `app/__init__.py:47`, `api.blueprint.after_request` is referenced but never called as a decorator (missing `@`). The function below it is dead code. Also, `blacklist_service.py:18` tries to return an Exception object as JSON which will fail.

**Files:**
- Modify: `app/__init__.py:47-51`
- Modify: `app/main/service/blacklist_service.py:16-20`

- [ ] **Step 1: Remove the broken `after_request` from `app/__init__.py`**

Delete lines 47-51 (the non-functional `after_request` reference and dead function). CORS is already handled by `CORS(api.blueprint)` on line 77 — the manual header was redundant anyway.

```python
# DELETE these lines:
# api.blueprint.after_request
#
#
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
```

- [ ] **Step 2: Fix blacklist_service error serialization**

In `app/main/service/blacklist_service.py`, change the except block:

```python
# BEFORE:
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': e
        }
        return response_object, 200

# AFTER:
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Failed to blacklist token.'
        }
        return response_object, 500
```

- [ ] **Step 3: Commit**

```bash
git add app/__init__.py app/main/service/blacklist_service.py
git commit -m "fix: remove dead after_request code, fix blacklist error serialization"
```

---

### Task 3: Add Security Headers

**Why:** No security headers are set. Missing X-Content-Type-Options, X-Frame-Options, Strict-Transport-Security, etc. These are zero-risk additions — browsers simply ignore headers they don't understand.

**Files:**
- Modify: `app/main/__init__.py`

- [ ] **Step 1: Add security headers via `after_request` in `create_app()`**

In `app/main/__init__.py`, update `create_app`:

```python
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)

    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '0'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'geolocation=(), camera=(), microphone=()'
        if not app.debug:
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

    return app
```

Note: `X-XSS-Protection` is set to `0` because the legacy XSS auditor actually introduced vulnerabilities. Modern browsers have deprecated it. Setting to 0 disables it explicitly.

- [ ] **Step 2: Verify headers appear**

```bash
curl -I http://localhost:5000/api/product/all
```

Expected: Response includes `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, etc.

- [ ] **Step 3: Commit**

```bash
git add app/main/__init__.py
git commit -m "feat: add security response headers"
```

---

### Task 4: Tighten CORS Configuration

**Why:** Currently `CORS(api.blueprint)` with no arguments allows all origins. Should restrict to the frontend domain(s).

**Files:**
- Modify: `app/main/config.py`
- Modify: `app/__init__.py`

- [ ] **Step 1: Add CORS config to `config.py`**

Add to the `Config` base class:

```python
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
```

This defaults to `*` (current behavior) so nothing breaks if the env var isn't set. In production, set `CORS_ORIGINS=https://certiflo.com,https://www.certiflo.com`.

- [ ] **Step 2: Update CORS initialization in `app/__init__.py`**

Replace:
```python
CORS(api.blueprint)
```

With:
```python
from app.main.config import Config
CORS(api.blueprint, origins=Config.CORS_ORIGINS)
```

- [ ] **Step 3: Commit**

```bash
git add app/main/config.py app/__init__.py
git commit -m "feat: configurable CORS origins (defaults to * for backward compat)"
```

---

### Task 5: Add Global Error Handlers

**Why:** Unhandled exceptions return Flask's default HTML error pages with stack traces in debug mode, and generic 500s in production with no structured JSON. API clients need consistent JSON error responses.

**Files:**
- Create: `app/main/middleware/__init__.py`
- Create: `app/main/middleware/error_handlers.py`
- Modify: `app/main/__init__.py`

- [ ] **Step 1: Create `app/main/middleware/__init__.py`**

Empty file.

- [ ] **Step 2: Create `app/main/middleware/error_handlers.py`**

```python
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
```

- [ ] **Step 3: Register error handlers in `create_app`**

In `app/main/__init__.py`, add import and call:

```python
from .middleware.error_handlers import register_error_handlers

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)

    register_error_handlers(app)

    @app.after_request
    def set_security_headers(response):
        # ... (from Task 3)
        return response

    return app
```

- [ ] **Step 4: Commit**

```bash
git add app/main/middleware/__init__.py app/main/middleware/error_handlers.py app/main/__init__.py
git commit -m "feat: add global JSON error handlers for consistent API responses"
```

---

### Task 6: Add Rate Limiting

**Why:** No rate limiting exists. Login endpoint is vulnerable to brute force. All endpoints are vulnerable to abuse.

**Files:**
- Modify: `requirements.txt`
- Create: `app/main/middleware/rate_limiter.py`
- Modify: `app/main/__init__.py`
- Modify: `app/main/controller/auth_controller.py`

- [ ] **Step 1: Add Flask-Limiter to requirements**

Add to `requirements.txt`:
```
Flask-Limiter>=3.5,<4.0
```

- [ ] **Step 2: Install the dependency**

```bash
pip install Flask-Limiter>=3.5,<4.0
```

- [ ] **Step 3: Create `app/main/middleware/rate_limiter.py`**

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per minute"],
    storage_uri="memory://",
)
```

Note: Uses in-memory storage. For multi-worker production, switch to Redis by setting `storage_uri` to a Redis URL. In-memory is safe — it just means each worker tracks limits independently, which is still protective.

- [ ] **Step 4: Initialize limiter in `create_app`**

In `app/main/__init__.py`:

```python
from .middleware.rate_limiter import limiter

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    limiter.init_app(app)

    register_error_handlers(app)

    # ... rest of create_app
```

- [ ] **Step 5: Add strict rate limit to login endpoint**

In `app/main/controller/auth_controller.py`:

```python
from flask import request
from flask_restx import Resource

from app.main.service.auth_service import Auth
from app.main.middleware.rate_limiter import limiter
from ..dto.auth_dto import AuthDto

api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route('/login')
class UserLogin(Resource):
    decorators = [limiter.limit("5 per minute")]

    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self):
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route('/logout')
class UserLogout(Resource):
    @api.doc('logout a user')
    def post(self):
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)
```

- [ ] **Step 6: Commit**

```bash
git add requirements.txt app/main/middleware/rate_limiter.py app/main/__init__.py app/main/controller/auth_controller.py
git commit -m "feat: add rate limiting (200/min global, 5/min on login)"
```

---

### Task 7: Add Auth to File Endpoints

**Why:** File list, download, and upload endpoints have `@api.doc(security='Bearer')` for Swagger docs but no actual `@auth.login_required` decorator. Anyone can upload/download files without authentication.

**Files:**
- Modify: `app/main/controller/file_controller.py`

- [ ] **Step 1: Add `@auth.login_required` to all file endpoints**

Update `file_controller.py` — add the decorator to each resource class's methods:

```python
@api.route("/")
class GetFiles(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Get files')
    def get(self):
        # ... existing code unchanged
```

```python
@api.route("/download/<fileName>")
class Download(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Download file')
    def get(self, fileName):
        return send_from_directory(UPLOAD_DIRECTORY, fileName, as_attachment=True)
```

```python
@api.route('/upload')
class Upload(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Save new file')
    @api.expect(upload_parser)
    def post(self):
        # ... existing code unchanged
```

Also remove the unused `data = request.json` line from the Download endpoint.

- [ ] **Step 2: Add file size limit**

Add at the top of the file after the imports:

```python
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
```

In the Upload `post` method, add a size check after getting the file:

```python
file = request.files['file']
file.seek(0, 2)  # Seek to end
size = file.tell()
file.seek(0)     # Seek back to start
if size > MAX_FILE_SIZE:
    resp = jsonify({'message': 'File too large. Maximum size is 10 MB.'})
    resp.status_code = 413
    return resp
```

- [ ] **Step 3: Fix error message to match actual allowed extensions**

Change line 84-85 from:
```python
{'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'}
```
To:
```python
{'message': 'Allowed file types are: pdf'}
```

- [ ] **Step 4: Commit**

```bash
git add app/main/controller/file_controller.py
git commit -m "fix: add auth to file endpoints, add file size limit, fix error message"
```

---

### Task 8: Harden Auth Service Error Handling

**Why:** `auth_service.py:46` uses bare `print(e)` which leaks to stdout and provides no structure. The `logout_user` method doesn't return a response in the else branch (line 71-75).

**Files:**
- Modify: `app/main/service/auth_service.py`

- [ ] **Step 1: Replace `print` with `logger`, fix missing return, clean up**

```python
import logging
from app.main.model.user import User
from ..service.blacklist_service import save_token
from flask_httpauth import HTTPTokenAuth
from flask import current_app

logger = logging.getLogger(__name__)


class Auth:

    auth = HTTPTokenAuth(scheme='Bearer')

    @staticmethod
    @auth.verify_token
    def verify_token(token):
        if current_app.config.get('DISABLE_AUTHENTICATION', False) == True:
            logger.warning('Authentication is disabled. Skipped token validation.')
            return True
        if User.is_valid_token(token):
            return True
        return False

    @staticmethod
    def login_user(data):
        try:
            user = User.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(data.get('password')):
                auth_token = User.encode_auth_token(user.id)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'Authorization': auth_token
                    }
                    return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'email or password does not match.'
                }
                return response_object, 401

        except Exception as e:
            logger.error(f'Login error: {e}', exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def logout_user(data):
        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                return save_token(token=auth_token)
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

    @staticmethod
    def get_logged_in_user(new_request):
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                if not user:
                    return {'status': 'fail', 'message': 'User not found.'}, 404
                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'registered_on': str(user.registered_on)
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401
```

Note: Removed the duplicate import (`from app.main.model.user import User` was imported twice). Also removed reference to `user.admin` in `get_logged_in_user` since the User model doesn't have an `admin` column.

- [ ] **Step 2: Commit**

```bash
git add app/main/service/auth_service.py
git commit -m "fix: replace print with logger, fix missing return in logout, remove dead code"
```

---

### Task 9: Fail on Missing SECRET_KEY in Production

**Why:** `Config.SECRET_KEY` defaults to `'dev-only-fallback-key'` which is fine for dev but catastrophic if accidentally used in production. JWTs signed with a known key can be forged. Task 1 already switched JWT operations to use `current_app.config['SECRET_KEY']`, so now we just need to ensure the config value is correct in production.

**Files:**
- Modify: `app/main/__init__.py`

- [ ] **Step 1: Add startup validation in `create_app`**

In `app/main/__init__.py`, add validation right after `app.config.from_object(...)`:

```python
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    if config_name == 'prod':
        if not os.environ.get('SECRET_KEY'):
            raise ValueError('SECRET_KEY environment variable is required in production')
        if not app.config.get('SQLALCHEMY_DATABASE_URI'):
            raise ValueError('DATABASE_URL environment variable is required in production')

    db.init_app(app)
    flask_bcrypt.init_app(app)
    limiter.init_app(app)

    register_error_handlers(app)
    # ... rest
```

Add `import os` at the top of the file if not already present.

Note: No changes to `config.py` needed — the base class default is fine for dev/test, and the `create_app` validation ensures prod has a real key. Since Task 1 switched to `current_app.config['SECRET_KEY']`, the actual config value (not the module-level import) is used for JWT operations.

- [ ] **Step 2: Commit**

```bash
git add app/main/__init__.py
git commit -m "feat: fail fast if SECRET_KEY or DATABASE_URL missing in production"
```

---

### Task 10: Final Verification

- [ ] **Step 1: Run the app locally and test all changes**

```bash
FLASK_CONFIG=dev python manage.py run
```

- [ ] **Step 2: Test login + rate limiting**

```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test"}'

# Rapid-fire to test rate limit (should get 429 after 5)
for i in {1..7}; do
  curl -s -o /dev/null -w "%{http_code}\n" -X POST http://localhost:5000/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"wrong@test.com","password":"wrong"}'
done
```

- [ ] **Step 3: Test security headers**

```bash
curl -I http://localhost:5000/api/product/all 2>/dev/null | grep -E "X-Content|X-Frame|Referrer"
```

Expected:
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
```

- [ ] **Step 4: Test file endpoint requires auth**

```bash
curl -s http://localhost:5000/api/file/ -w "%{http_code}"
```

Expected: `401`

- [ ] **Step 5: Test error handler returns JSON**

```bash
curl http://localhost:5000/api/nonexistent
```

Expected: `{"status": "fail", "message": "Resource not found."}`

- [ ] **Step 6: Final commit if any adjustments needed**

---

## Post-Deployment: Environment Variables to Set

On your Oracle Cloud VM (or wherever production runs), ensure these env vars are set:

| Variable | Example | Required |
|----------|---------|----------|
| `SECRET_KEY` | `python3 -c "import secrets; print(secrets.token_hex(64))"` | Yes (prod) |
| `DATABASE_URL` | `postgresql://user:pass@host:5432/certiflo` | Yes (prod) |
| `CORS_ORIGINS` | `https://certiflo.com,https://www.certiflo.com` | Recommended |
| `FLASK_CONFIG` | `prod` | Yes |

## Future Improvements (Out of Scope)

These are worth doing later but would increase blast radius now:
- **Redis-backed rate limiting** for multi-worker deployments
- **Refresh tokens** for better session management
- **RBAC** using the existing User model (add `role` column)
- **Request logging middleware** for audit trail
- **CSP header** (needs frontend coordination)
- **Input length validation** in DTOs (add `max_length` to string fields)
- **Password strength requirements** on registration

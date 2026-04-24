"""
Generate flask_syntax.docx — complete Flask syntax reference for COMP4442.
Covers every object and method likely to appear in exam code questions.
"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
for section in doc.sections:
    section.top_margin = Cm(1.5)
    section.bottom_margin = Cm(1.5)
    section.left_margin = Cm(1.8)
    section.right_margin = Cm(1.8)

style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(10)


def H(text, lvl=1):
    return doc.add_heading(text, level=lvl)


def A(text):
    p = doc.add_paragraph(text)
    for r in p.runs:
        r.font.size = Pt(10)
    return p


def B(text):
    p = doc.add_paragraph(text, style='List Bullet')
    for r in p.runs:
        r.font.size = Pt(10)
    return p


def Code(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Consolas'
    run.font.size = Pt(9)
    p.paragraph_format.left_indent = Cm(0.4)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(2)
    return p


def table2(headers, rows, col_widths=None):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = 'Light Grid Accent 1'
    for i, h in enumerate(headers):
        cell = t.rows[0].cells[i]
        cell.text = h
        for run in cell.paragraphs[0].runs:
            run.bold = True
            run.font.size = Pt(10)
    for ri, row in enumerate(rows, 1):
        for ci, val in enumerate(row):
            cell = t.rows[ri].cells[ci]
            cell.text = val
            for run in cell.paragraphs[0].runs:
                run.font.size = Pt(10)
    if col_widths:
        for row in t.rows:
            for ci, w in enumerate(col_widths):
                row.cells[ci].width = Cm(w)
    doc.add_paragraph()


# ── TITLE ──────────────────────────────────────────────────────────────────
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('Flask Syntax Reference — COMP4442')
run.bold = True
run.font.size = Pt(14)
A('Complete syntax for: app setup, routing, request, response, session, cookies, '
  'templates, blueprints, error handling, before/after hooks, database (boto3 + SQLAlchemy).')

# ══════════════════════════════════════════════════════════════════════════
H('1. App Setup & Configuration')
# ══════════════════════════════════════════════════════════════════════════
Code(
    'from flask import (\n'
    '    Flask, request, jsonify, render_template, redirect,\n'
    '    url_for, session, abort, make_response, g, current_app\n'
    ')\n'
    '\n'
    'app = Flask(__name__)           # __name__ tells Flask where to find templates/static\n'
    '\n'
    '# --- Config ---\n'
    'app.secret_key = "change-me"    # REQUIRED for sessions (signs cookie with HMAC)\n'
    'app.config["DEBUG"] = True\n'
    'app.config["TESTING"] = False\n'
    'app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://user:pass@host/db"\n'
    'app.config.from_object("config.ProductionConfig")   # load from a config class\n'
    'app.config.from_envvar("APP_SETTINGS")              # load from env var pointing to file\n'
    '\n'
    '# --- Run ---\n'
    'if __name__ == "__main__":\n'
    '    app.run(host="0.0.0.0", port=5000, debug=True)\n'
    '    # Elastic Beanstalk expects the variable to be named "application"\n'
    'application = app               # EB requirement'
)

# ══════════════════════════════════════════════════════════════════════════
H('2. Routing')
# ══════════════════════════════════════════════════════════════════════════
Code(
    '# Basic route\n'
    '@app.route("/")\n'
    'def index():\n'
    '    return "Hello World"\n'
    '\n'
    '# Specify HTTP methods\n'
    '@app.route("/users", methods=["GET", "POST"])\n'
    'def users():\n'
    '    if request.method == "POST": ...\n'
    '\n'
    '# URL variables — types: string (default), int, float, path, uuid\n'
    '@app.route("/users/<int:user_id>")\n'
    'def get_user(user_id):           # user_id is an int\n'
    '    ...\n'
    '\n'
    '@app.route("/files/<path:filename>")   # path includes slashes\n'
    'def serve_file(filename): ...\n'
    '\n'
    '# url_for — reverse lookup: build URL from function name\n'
    'url_for("get_user", user_id=42)         # → "/users/42"\n'
    'url_for("index")                        # → "/"\n'
    'url_for("static", filename="app.js")   # → "/static/app.js"\n'
    '\n'
    '# Redirect\n'
    'return redirect(url_for("index"))       # 302 by default\n'
    'return redirect(url_for("index"), 301)  # permanent redirect'
)

table2(
    ['Decorator / Function', 'Purpose'],
    [
        ('@app.route(path, methods=[…])',  'Bind URL path to a view function'),
        ('@app.route(path, strict_slashes=False)', 'Accept both /path and /path/'),
        ('url_for("view_name", **kwargs)', 'Build URL — safer than hardcoding strings'),
        ('redirect(url, code=302)',        'Return HTTP redirect response'),
        ('abort(code)',                    'Immediately return an error response (e.g. abort(404), abort(403))'),
    ],
    col_widths=[7.5, 9.5]
)

# ══════════════════════════════════════════════════════════════════════════
H('3. request Object')
# ══════════════════════════════════════════════════════════════════════════
A('Available inside any view function. Represents the current HTTP request.')
Code(
    'from flask import request\n'
    '\n'
    '# ── HTTP method ──\n'
    'request.method               # "GET", "POST", "PUT", "DELETE", "PATCH"\n'
    '\n'
    '# ── Query string  (?key=value) ──\n'
    'request.args                 # ImmutableMultiDict of query params\n'
    'request.args.get("q")        # None if missing\n'
    'request.args.get("page", 1)  # default value\n'
    'request.args["q"]            # KeyError if missing — avoid in production\n'
    'request.args.getlist("tag")  # list for repeated keys: ?tag=a&tag=b → ["a","b"]\n'
    '\n'
    '# ── Form data (POST, Content-Type: application/x-www-form-urlencoded) ──\n'
    'request.form                 # ImmutableMultiDict\n'
    'request.form.get("username")\n'
    'request.form.getlist("items")\n'
    '\n'
    '# ── JSON body (Content-Type: application/json) ──\n'
    'request.json                 # parsed dict — None if Content-Type is wrong\n'
    'request.get_json()           # same but with options:\n'
    'request.get_json(force=True)         # parse even if Content-Type is not JSON\n'
    'request.get_json(silent=True)        # return None instead of 400 on bad JSON\n'
    'request.get_json(force=True, silent=True)\n'
    '\n'
    '# ── Raw body ──\n'
    'request.data                 # raw bytes of request body\n'
    '\n'
    '# ── Headers ──\n'
    'request.headers              # dict-like\n'
    'request.headers.get("Authorization")\n'
    'request.headers["Content-Type"]\n'
    '\n'
    '# ── Cookies ──\n'
    'request.cookies              # dict\n'
    'request.cookies.get("session_id")\n'
    '\n'
    '# ── File uploads (Content-Type: multipart/form-data) ──\n'
    'request.files                # ImmutableMultiDict of FileStorage objects\n'
    'f = request.files["photo"]\n'
    'f.filename                   # original filename\n'
    'f.save("/uploads/" + f.filename)\n'
    'f.read()                     # read bytes\n'
    '\n'
    '# ── Client info ──\n'
    'request.remote_addr          # client IP string\n'
    'request.url                  # full URL\n'
    'request.base_url             # URL without query string\n'
    'request.host                 # hostname:port\n'
    'request.path                 # path only: "/users/42"\n'
    'request.is_json              # True if Content-Type is application/json'
)

table2(
    ['Attribute', 'Type', 'Contains'],
    [
        ('request.method',    'str',              'HTTP verb: GET, POST, PUT, DELETE, PATCH'),
        ('request.args',      'ImmutableMultiDict','Query string params (?key=value)'),
        ('request.form',      'ImmutableMultiDict','POST form body (urlencoded / multipart)'),
        ('request.json',      'dict | None',      'Parsed JSON body (needs Content-Type: application/json)'),
        ('request.get_json()','dict | None',      'Like .json but with force= and silent= options'),
        ('request.data',      'bytes',            'Raw request body'),
        ('request.headers',   'Headers',          'HTTP request headers (dict-like)'),
        ('request.cookies',   'dict',             'Cookie values sent by client'),
        ('request.files',     'ImmutableMultiDict','Uploaded files (multipart/form-data)'),
        ('request.path',      'str',              'URL path: "/api/users/1"'),
        ('request.remote_addr','str',             'Client IP address'),
        ('request.is_json',   'bool',             'True if Content-Type is application/json'),
    ],
    col_widths=[4.0, 3.5, 9.5]
)

# ══════════════════════════════════════════════════════════════════════════
H('4. Response & jsonify')
# ══════════════════════════════════════════════════════════════════════════
Code(
    'from flask import jsonify, make_response\n'
    '\n'
    '# ── Plain string / tuple shorthand ──\n'
    'return "OK"                              # 200, text/html\n'
    'return "Not found", 404                  # status code shorthand\n'
    'return "Created", 201, {"X-Custom": "v"} # body, status, extra headers\n'
    '\n'
    '# ── JSON responses ──\n'
    'return jsonify({"name": "alice", "age": 30})   # 200, application/json\n'
    'return jsonify(message="ok", code=200), 200\n'
    'return jsonify(items=[1, 2, 3]), 201\n'
    '\n'
    '# ── make_response — full control ──\n'
    'resp = make_response(jsonify({"ok": True}), 200)\n'
    'resp.headers["X-Custom-Header"] = "value"\n'
    'resp.set_cookie("token", "abc123", httponly=True, secure=True)\n'
    'resp.delete_cookie("old_token")\n'
    'return resp\n'
    '\n'
    '# ── Common status codes ──\n'
    '# 200 OK          201 Created       204 No Content\n'
    '# 400 Bad Request  401 Unauthorized  403 Forbidden\n'
    '# 404 Not Found    409 Conflict      422 Unprocessable\n'
    '# 500 Internal Server Error'
)

# ══════════════════════════════════════════════════════════════════════════
H('5. session')
# ══════════════════════════════════════════════════════════════════════════
A('Flask session = signed cookie stored on the client. Data is visible (base64) but not '
  'modifiable (HMAC signature). Requires app.secret_key. Nothing is stored on the server by default.')
Code(
    'from flask import session\n'
    '\n'
    'app.secret_key = "super-secret"  # MUST be set before using session\n'
    '\n'
    '# ── Write ──\n'
    'session["username"] = "alice"    # store a value\n'
    'session["role"] = "admin"\n'
    'session["cart"] = [1, 2, 3]      # can store lists/dicts\n'
    '\n'
    '# ── Read ──\n'
    'session["username"]              # KeyError if missing\n'
    'session.get("username")          # None if missing — safe\n'
    'session.get("username", "guest") # default value if missing\n'
    '"username" in session            # True/False membership test\n'
    '\n'
    '# ── Delete ──\n'
    'session.pop("username")          # remove key, KeyError if missing\n'
    'session.pop("username", None)    # remove key safely (None = no error if absent)\n'
    'del session["username"]          # also removes key\n'
    '\n'
    '# ── Clear all (logout) ──\n'
    'session.clear()                  # removes ALL keys from session\n'
    '\n'
    '# ── Permanence ──\n'
    'session.permanent = True         # use app.permanent_session_lifetime for expiry\n'
    'from datetime import timedelta\n'
    'app.permanent_session_lifetime = timedelta(days=7)\n'
    '\n'
    '# ── Typical login/logout pattern ──\n'
    '@app.route("/login", methods=["POST"])\n'
    'def login():\n'
    '    data = request.get_json()\n'
    '    if data["password"] == "correct":\n'
    '        session["user"] = data["username"]\n'
    '        return jsonify(message="logged in"), 200\n'
    '    return jsonify(error="bad credentials"), 401\n'
    '\n'
    '@app.route("/logout", methods=["POST"])\n'
    'def logout():\n'
    '    session.clear()              # or session.pop("user", None)\n'
    '    return jsonify(message="logged out"), 200\n'
    '\n'
    '@app.route("/profile")\n'
    'def profile():\n'
    '    if "user" not in session:\n'
    '        return jsonify(error="unauthorized"), 401\n'
    '    return jsonify(user=session["user"])'
)

table2(
    ['Operation', 'Code', 'Notes'],
    [
        ('Set value',      'session["key"] = val',       'Creates or overwrites key'),
        ('Get (safe)',      'session.get("key")',         'Returns None if missing — always prefer over []'),
        ('Get (default)',   'session.get("key", default)','Returns default if missing'),
        ('Check exists',   '"key" in session',           'Boolean'),
        ('Remove one key', 'session.pop("key", None)',   'None prevents KeyError; most common logout pattern'),
        ('Remove one key', 'del session["key"]',         'Raises KeyError if missing'),
        ('Clear all',      'session.clear()',            'Full logout — removes everything'),
        ('Make permanent', 'session.permanent = True',   'Session lasts until permanent_session_lifetime'),
    ],
    col_widths=[3.5, 5.5, 8.0]
)

# ══════════════════════════════════════════════════════════════════════════
H('6. Cookies')
# ══════════════════════════════════════════════════════════════════════════
A('Unlike session (automatic), cookies require explicit set/delete on a Response object.')
Code(
    '# ── Read cookie ──\n'
    'token = request.cookies.get("auth_token")   # None if absent\n'
    '\n'
    '# ── Set cookie ──\n'
    'resp = make_response(jsonify(ok=True))\n'
    'resp.set_cookie(\n'
    '    "auth_token",          # cookie name\n'
    '    value="abc123",        # cookie value\n'
    '    max_age=3600,          # seconds until expiry (None = session cookie)\n'
    '    expires=None,          # datetime object or None\n'
    '    path="/",              # path scope\n'
    '    domain=None,           # None = current domain\n'
    '    secure=True,           # HTTPS only\n'
    '    httponly=True,         # JS cannot read (XSS protection)\n'
    '    samesite="Lax"         # CSRF protection: Strict | Lax | None\n'
    ')\n'
    'return resp\n'
    '\n'
    '# ── Delete cookie ──\n'
    'resp.delete_cookie("auth_token")    # sets max_age=0\n'
    'resp.delete_cookie("auth_token", path="/", domain="example.com")'
)

# ══════════════════════════════════════════════════════════════════════════
H('7. render_template & Jinja2')
# ══════════════════════════════════════════════════════════════════════════
A('Templates live in the templates/ folder next to app.py by default.')
Code(
    'from flask import render_template\n'
    '\n'
    '# ── Render a template ──\n'
    'return render_template("index.html")\n'
    'return render_template("user.html", name="Alice", age=30)\n'
    'return render_template("items.html", items=[1, 2, 3], title="My List")\n'
    '\n'
    '# ── render_template_string — render from a string (no file) ──\n'
    'from flask import render_template_string\n'
    'html = "<h1>Hello {{ name }}</h1>"\n'
    'return render_template_string(html, name="World")'
)

H('Jinja2 Template Syntax', lvl=2)
Code(
    '{# This is a comment — not rendered #}\n'
    '\n'
    '<!-- Variables -->\n'
    '{{ name }}                      output a variable\n'
    '{{ user.email }}                attribute access\n'
    '{{ items[0] }}                  index access\n'
    '{{ name | upper }}              filter: upper, lower, title, trim, length, default, safe\n'
    '{{ price | round(2) }}\n'
    '{{ html_content | safe }}       mark as safe (no escaping) — XSS risk\n'
    '{{ name | default("guest") }}   fallback if None/undefined\n'
    '\n'
    '<!-- Control flow -->\n'
    '{% if user.role == "admin" %}\n'
    '  <a href="/admin">Admin Panel</a>\n'
    '{% elif user.role == "mod" %}\n'
    '  <a href="/mod">Mod Panel</a>\n'
    '{% else %}\n'
    '  <p>No access</p>\n'
    '{% endif %}\n'
    '\n'
    '<!-- For loop -->\n'
    '{% for item in items %}\n'
    '  <li>{{ loop.index }}. {{ item.name }}</li>\n'
    '{% else %}\n'
    '  <li>No items.</li>     {# rendered if items is empty #}\n'
    '{% endfor %}\n'
    '\n'
    '<!-- Loop variables: loop.index (1-based), loop.index0 (0-based),\n'
    '     loop.first, loop.last, loop.length -->\n'
    '\n'
    '<!-- Template inheritance -->\n'
    '{# base.html #}\n'
    '<!DOCTYPE html><html><body>\n'
    '  {% block content %}{% endblock %}\n'
    '</body></html>\n'
    '\n'
    '{# child.html #}\n'
    '{% extends "base.html" %}\n'
    '{% block content %}\n'
    '  <h1>Welcome</h1>\n'
    '{% endblock %}\n'
    '\n'
    '<!-- Include partial -->\n'
    '{% include "nav.html" %}\n'
    '\n'
    '<!-- Set variable in template -->\n'
    '{% set total = price * qty %}\n'
    '\n'
    '<!-- Whitespace control -->\n'
    '{{- var -}}     trim whitespace around this block'
)

# ══════════════════════════════════════════════════════════════════════════
H('8. Error Handling')
# ══════════════════════════════════════════════════════════════════════════
Code(
    'from flask import abort, jsonify\n'
    '\n'
    '# ── abort — immediately stop and return an error ──\n'
    'abort(400)                      # 400 Bad Request\n'
    'abort(401)                      # 401 Unauthorized\n'
    'abort(403)                      # 403 Forbidden\n'
    'abort(404)                      # 404 Not Found\n'
    'abort(500)                      # 500 Internal Server Error\n'
    '\n'
    '# ── Custom error handlers ──\n'
    '@app.errorhandler(404)\n'
    'def not_found(error):\n'
    '    return jsonify(error="not found", code=404), 404\n'
    '\n'
    '@app.errorhandler(401)\n'
    'def unauthorized(error):\n'
    '    return jsonify(error="unauthorized"), 401\n'
    '\n'
    '@app.errorhandler(500)\n'
    'def server_error(error):\n'
    '    return jsonify(error="internal server error"), 500\n'
    '\n'
    '# ── Handle all exceptions ──\n'
    '@app.errorhandler(Exception)\n'
    'def handle_exception(e):\n'
    '    return jsonify(error=str(e)), 500'
)

# ══════════════════════════════════════════════════════════════════════════
H('9. Blueprints (modular routing)')
# ══════════════════════════════════════════════════════════════════════════
Code(
    '# ── users.py — define a blueprint ──\n'
    'from flask import Blueprint, jsonify\n'
    '\n'
    'users_bp = Blueprint("users", __name__, url_prefix="/users")\n'
    '\n'
    '@users_bp.route("/")              # → GET /users/\n'
    'def list_users(): ...\n'
    '\n'
    '@users_bp.route("/<int:uid>")     # → GET /users/42\n'
    'def get_user(uid): ...\n'
    '\n'
    '# ── app.py — register blueprint ──\n'
    'from users import users_bp\n'
    'app.register_blueprint(users_bp)\n'
    'app.register_blueprint(users_bp, url_prefix="/api/v2/users")  # override prefix\n'
    '\n'
    '# ── url_for with blueprint ──\n'
    'url_for("users.get_user", uid=42)  # "<blueprint_name>.<function_name>"'
)

# ══════════════════════════════════════════════════════════════════════════
H('10. before_request / after_request / g')
# ══════════════════════════════════════════════════════════════════════════
A('g is a per-request scratch pad — data set during a request lives until the response is sent.')
Code(
    'from flask import g, request, jsonify\n'
    '\n'
    '# ── before_request — runs before EVERY request ──\n'
    '@app.before_request\n'
    'def authenticate():\n'
    '    token = request.headers.get("Authorization", "").replace("Bearer ", "")\n'
    '    if not token:\n'
    '        return jsonify(error="missing token"), 401   # return early = short-circuit\n'
    '    g.user = verify_jwt(token)  # attach to g for the rest of the request\n'
    '\n'
    '# ── after_request — runs after EVERY successful response ──\n'
    '@app.after_request\n'
    'def add_cors(response):\n'
    '    response.headers["Access-Control-Allow-Origin"] = "*"\n'
    '    return response                # MUST return the response\n'
    '\n'
    '# ── teardown_request — runs even if an exception occurred ──\n'
    '@app.teardown_request\n'
    'def close_db(exception=None):\n'
    '    db = g.pop("db", None)\n'
    '    if db: db.close()\n'
    '\n'
    '# ── g — per-request storage ──\n'
    'g.user = "alice"             # set\n'
    'g.user                       # read\n'
    'g.get("user")                # safe read — None if not set\n'
    'g.pop("user", None)          # remove\n'
    'hasattr(g, "user")           # check existence'
)

# ══════════════════════════════════════════════════════════════════════════
H('11. current_app & Application Context')
# ══════════════════════════════════════════════════════════════════════════
Code(
    'from flask import current_app\n'
    '\n'
    '# current_app — proxy to the active Flask app\n'
    '# Use inside view functions or app context (NOT at module scope)\n'
    'current_app.config["DEBUG"]\n'
    'current_app.logger.info("message")   # built-in logger\n'
    'current_app.logger.error("oops")\n'
    '\n'
    '# Push application context manually (e.g. in scripts or tests)\n'
    'with app.app_context():\n'
    '    # db queries, current_app available here\n'
    '    result = SomeModel.query.all()'
)

# ══════════════════════════════════════════════════════════════════════════
H('12. Database — boto3 (DynamoDB / S3)')
# ══════════════════════════════════════════════════════════════════════════
A('boto3 client created at MODULE SCOPE so it is reused across Lambda warm invocations.')
Code(
    'import boto3\n'
    'from boto3.dynamodb.conditions import Key, Attr\n'
    '\n'
    'dynamodb = boto3.resource("dynamodb", region_name="ap-east-1")\n'
    'table = dynamodb.Table("Users")\n'
    '\n'
    '# ── PutItem (create / overwrite) ──\n'
    'table.put_item(Item={"user_id": "u1", "name": "Alice", "age": 30})\n'
    '\n'
    '# ── GetItem (by primary key) ──\n'
    'resp = table.get_item(Key={"user_id": "u1"})\n'
    'item = resp.get("Item")          # None if not found\n'
    '\n'
    '# ── UpdateItem ──\n'
    'table.update_item(\n'
    '    Key={"user_id": "u1"},\n'
    '    UpdateExpression="SET #n = :name, age = :age",\n'
    '    ExpressionAttributeNames={"#n": "name"},   # #n avoids reserved word "name"\n'
    '    ExpressionAttributeValues={":name": "Bob", ":age": 31}\n'
    ')\n'
    '\n'
    '# ── DeleteItem ──\n'
    'table.delete_item(Key={"user_id": "u1"})\n'
    '\n'
    '# ── Query (uses index — fast, preferred) ──\n'
    'resp = table.query(\n'
    '    KeyConditionExpression=Key("user_id").eq("u1")\n'
    ')\n'
    'items = resp["Items"]\n'
    '\n'
    '# ── Query with filter ──\n'
    'resp = table.query(\n'
    '    KeyConditionExpression=Key("user_id").eq("u1"),\n'
    '    FilterExpression=Attr("age").gt(25)\n'
    ')\n'
    '\n'
    '# ── Scan (reads whole table — AVOID in production) ──\n'
    'resp = table.scan(FilterExpression=Attr("role").eq("admin"))\n'
    '\n'
    '# ── S3 ──\n'
    's3 = boto3.client("s3")\n'
    's3.upload_file("local.txt", "my-bucket", "folder/remote.txt")\n'
    'resp = s3.get_object(Bucket="my-bucket", Key="folder/remote.txt")\n'
    'body = resp["Body"].read().decode("utf-8")\n'
    's3.put_object(Bucket="my-bucket", Key="file.json", Body=\'{"a":1}\')\n'
    '\n'
    '# ── SQS ──\n'
    'sqs = boto3.client("sqs")\n'
    'sqs.send_message(QueueUrl="https://...", MessageBody="hello")\n'
    'resp = sqs.receive_message(QueueUrl="https://...", MaxNumberOfMessages=10)\n'
    'for msg in resp.get("Messages", []):\n'
    '    print(msg["Body"])\n'
    '    sqs.delete_message(QueueUrl="https://...", ReceiptHandle=msg["ReceiptHandle"])'
)

# ══════════════════════════════════════════════════════════════════════════
H('13. Database — SQLAlchemy (MySQL / SQLite)')
# ══════════════════════════════════════════════════════════════════════════
Code(
    'from flask import Flask\n'
    'from flask_sqlalchemy import SQLAlchemy\n'
    '\n'
    'app = Flask(__name__)\n'
    'app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://user:pass@host:3306/db"\n'
    'app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False\n'
    'db = SQLAlchemy(app)\n'
    '\n'
    '# ── Define model ──\n'
    'class User(db.Model):\n'
    '    __tablename__ = "users"\n'
    '    id       = db.Column(db.Integer, primary_key=True, autoincrement=True)\n'
    '    username = db.Column(db.String(80), unique=True, nullable=False)\n'
    '    email    = db.Column(db.String(120), unique=True)\n'
    '    role     = db.Column(db.String(20), default="user")\n'
    '\n'
    '    def to_dict(self):                    # handy for jsonify\n'
    '        return {"id": self.id, "username": self.username}\n'
    '\n'
    '# ── Create tables ──\n'
    'with app.app_context():\n'
    '    db.create_all()\n'
    '\n'
    '# ── CRUD ──\n'
    '# Create\n'
    'u = User(username="alice", email="alice@example.com")\n'
    'db.session.add(u)\n'
    'db.session.commit()\n'
    '\n'
    '# Read\n'
    'u = User.query.get(1)                          # by primary key\n'
    'u = User.query.filter_by(username="alice").first()  # by field\n'
    'users = User.query.all()                       # all rows\n'
    'users = User.query.filter(User.role == "admin").all()\n'
    'users = User.query.order_by(User.username).limit(10).all()\n'
    '\n'
    '# Update\n'
    'u = User.query.get(1)\n'
    'u.email = "new@example.com"\n'
    'db.session.commit()\n'
    '\n'
    '# Delete\n'
    'db.session.delete(u)\n'
    'db.session.commit()\n'
    '\n'
    '# Rollback on error\n'
    'try:\n'
    '    db.session.add(u)\n'
    '    db.session.commit()\n'
    'except Exception:\n'
    '    db.session.rollback()\n'
    '    raise'
)

# ══════════════════════════════════════════════════════════════════════════
H('14. Full CRUD Example (REST API)')
# ══════════════════════════════════════════════════════════════════════════
Code(
    'from flask import Flask, request, jsonify, abort\n'
    '\n'
    'app = Flask(__name__)\n'
    'items = {}   # in-memory store (replace with DB in production)\n'
    '\n'
    '@app.route("/items", methods=["GET"])\n'
    'def list_items():\n'
    '    return jsonify(list(items.values())), 200\n'
    '\n'
    '@app.route("/items/<int:item_id>", methods=["GET"])\n'
    'def get_item(item_id):\n'
    '    item = items.get(item_id)\n'
    '    if not item:\n'
    '        abort(404)\n'
    '    return jsonify(item), 200\n'
    '\n'
    '@app.route("/items", methods=["POST"])\n'
    'def create_item():\n'
    '    data = request.get_json(silent=True)\n'
    '    if not data or "name" not in data:\n'
    '        return jsonify(error="name required"), 400\n'
    '    new_id = max(items.keys(), default=0) + 1\n'
    '    items[new_id] = {"id": new_id, "name": data["name"]}\n'
    '    return jsonify(items[new_id]), 201\n'
    '\n'
    '@app.route("/items/<int:item_id>", methods=["PUT"])\n'
    'def update_item(item_id):\n'
    '    if item_id not in items:\n'
    '        abort(404)\n'
    '    data = request.get_json(silent=True) or {}\n'
    '    items[item_id].update(data)\n'
    '    return jsonify(items[item_id]), 200\n'
    '\n'
    '@app.route("/items/<int:item_id>", methods=["DELETE"])\n'
    'def delete_item(item_id):\n'
    '    if item_id not in items:\n'
    '        abort(404)\n'
    '    items.pop(item_id)\n'
    '    return "", 204                   # 204 No Content — no body'
)

# ══════════════════════════════════════════════════════════════════════════
H('15. Quick-Reference Summary Table')
# ══════════════════════════════════════════════════════════════════════════
table2(
    ['Object / Function', 'Common Usage', 'Notes'],
    [
        # app
        ('Flask(__name__)',           'app = Flask(__name__)',                       'Creates app; __name__ sets template/static root'),
        ('app.secret_key',            'app.secret_key = "key"',                     'MUST set before using session'),
        ('app.config[key]',           'app.config["DEBUG"] = True',                 'App-wide settings dict'),
        ('app.run()',                  'app.run(host="0.0.0.0", port=5000)',         'Dev server; use gunicorn in prod'),
        # routing
        ('@app.route()',              '@app.route("/path", methods=["GET","POST"])', 'Bind URL to view function'),
        ('url_for()',                 'url_for("view_name", id=1)',                  'Build URL from function name'),
        ('redirect()',                'redirect(url_for("index"))',                  'Return 302 redirect'),
        ('abort(code)',               'abort(404)',                                  'Immediately return error response'),
        # request
        ('request.method',           'if request.method == "POST":',                'HTTP verb string'),
        ('request.args.get()',        'request.args.get("q", "")',                   'Query string — safe read'),
        ('request.form.get()',        'request.form.get("email")',                   'POST form body'),
        ('request.get_json()',        'request.get_json(silent=True)',               'Parse JSON body; silent=True avoids 400 error'),
        ('request.json',             'data = request.json',                         'Parsed JSON dict — None if wrong Content-Type'),
        ('request.headers.get()',     'request.headers.get("Authorization")',        'Read HTTP header'),
        ('request.cookies.get()',     'request.cookies.get("token")',                'Read cookie'),
        ('request.files[]',          'f = request.files["photo"]; f.save(path)',    'File upload'),
        # response
        ('jsonify()',                 'return jsonify({"key": "val"}), 200',         'Returns JSON response'),
        ('make_response()',           'resp = make_response(jsonify(…), 201)',       'Full control over response'),
        ('resp.set_cookie()',         'resp.set_cookie("k","v", httponly=True)',     'Set cookie on response'),
        ('resp.delete_cookie()',      'resp.delete_cookie("k")',                     'Delete cookie (sets max_age=0)'),
        # session
        ('session["key"] = val',     'session["user"] = "alice"',                   'Store in signed cookie'),
        ('session.get("key")',        'session.get("user", "guest")',                'Safe read with optional default'),
        ('"key" in session',         'if "user" not in session: abort(401)',        'Check key exists'),
        ('session.pop("key", None)', 'session.pop("user", None)',                   'Remove one key safely'),
        ('session.clear()',          'session.clear()',                              'Remove all — full logout'),
        # templates
        ('render_template()',        'return render_template("t.html", x=1)',       'Render Jinja2 template from templates/'),
        # hooks
        ('@app.before_request',      '@app.before_request\\ndef auth(): …',         'Runs before every request; return early to block'),
        ('@app.after_request',       '@app.after_request\\ndef cors(r): return r',  'Runs after every response; must return response'),
        ('@app.errorhandler(code)',  '@app.errorhandler(404)\\ndef e(err): …',      'Custom error response for HTTP status code'),
        # context
        ('g',                        'g.user = decode_token(…)',                     'Per-request scratch pad; reset each request'),
        ('current_app',              'current_app.config["KEY"]',                   'Proxy to active app inside view or context'),
        # blueprint
        ('Blueprint()',              'bp = Blueprint("name", __name__)',             'Modular route group'),
        ('app.register_blueprint()', 'app.register_blueprint(bp, url_prefix="/v1")', 'Mount blueprint on app'),
    ],
    col_widths=[4.5, 6.5, 6.0]
)

doc.save('flask_syntax.docx')
print("flask_syntax.docx written.")

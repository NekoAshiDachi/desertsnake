from flask import Blueprint

"""Fielding's REST principles:

1. Client-server: client/server roles clearly differentiated; communicate
separately over transport

2. Layered system: client/server may use intermediaries and must never assume
client/server at other side of connection; no difference in way requests sent;
allows app architects to design large and complex networks able to satisfy large
volume of requests

3. Cache: server/intermediary indicates via cache controls if response can be
cached by intermediaries; API must use encryption, and if intermediary caches,
must terminate SSL connection or perform decryption and re-encryption

4. Code on demand: optional and rarely used since requires agreement between
server and client; server provide executable code in responses to
client

5. Stateless: controversial; should not save client state in API or server;
requests should include data server needs to identify and auth client, and to
carry out request; benefit is scalability (can run multiple instances of server)

6. Uniform interface: controversial and vaguely documented
    a. Unique resource identifier: unique URL with each resource
    b. Resource representation: server and client agree on resource format;
    usually JSON but content negotiation in HTTP protocol can allow multiple
    representation formats
    c. Self-descriptive messages: requests (GET, POST, PUT/PATCH, DELETE) /
    responses include all info that other party needs; target resource indicated
    as request URL, with additional info provided in HTTP headers
    d. Hypermedia: controversial and rare; resource relationships included in
    resource representations for intuitive navigation"""

bp = Blueprint('api', __name__)

from application.api import users, errors, tokens

# ─────────────────────────────────────────────────────────────────────────────
# api/views.py — Authentication Gauntlet Lab
#
# Wrap-Up Comparison Table (Reporter fills this in at the end of the lab):
#
# +-------------------+------------+-----------+-------------------+----------+
# | Method            | Stateful?  | DB Lookup?| Credentials sent  | Safe on  |
# |                   |            |           | every request?    | HTTP?    |
# +-------------------+------------+-----------+-------------------+----------+
# | Basic Auth        |            |           |                   |          |
# | Session Auth      |            |           |                   |          |
# | Opaque Token Auth |            |           |                   |          |
# | JWT               |            |           |                   |          |
# +-------------------+------------+-----------+-------------------+----------+
#
# ─────────────────────────────────────────────────────────────────────────────
# +-------------------+------------+-----------+-------------------+----------+
# | Method            | Stateful?  | DB Lookup?| Credentials sent  | Safe on  |
# |                   |            |           | every request?    | HTTP?    |
# +-------------------+------------+-----------+-------------------+----------+
# | Basic Auth        | No         | Yes       | Yes (password)    | No       |
# | Session Auth      | Yes        | Yes       | No (session ID)   | No       |
# | Opaque Token Auth | Yes        | Yes       | No (token)        | No       |
# | JWT               | No         | No        | No (token)        | No       |
# +-------------------+------------+-----------+-------------------+----------+
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 1 — Basic Authentication
# ─────────────────────────────────────────────────────────────────────────────

@api_view(["GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def basic_auth_view(request):
    # TODO: Extract and print the header
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    print(f"Incoming Header: {auth_header}")
    return Response({"message": "Check your terminal!"})
    # Reporter — Phase 1 challenge answers:
    # Q1 answer (header format for admin:admin123):  <username>:<password>
    # Q2 answer (what happens without credentials):   The requests can be intercepted easily


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 2 — Session Authentication
# ─────────────────────────────────────────────────────────────────────────────

@api_view(["GET"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def session_auth_view(request):
    # Reporter — Phase 2 challenge answers:
    # Q1 answer (effect of deleting the session cookie): After deleting the `sessionid` cookie, the server could no longer identify my session in the server-side session database, so it treated me as unauthenticated and redirected me to the login page.
    # Synthesis answer (how session fixation works): Restoring the original `sessionid` cookie logged me back into the application, showing that an attacker who obtains a valid session ID can impersonate the user without knowing their password; this is called session hijacking.

    return Response({"message": "Session authenticated.", "user": request.user.username})


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 3 — Token Authentication (Opaque)
# ─────────────────────────────────────────────────────────────────────────────

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def token_auth_view(request):
    # Reporter — Phase 3 challenge answers:
    # Q1 answer (status code when token is tampered): Tampered token returned 401 Unauthorized.
    # Q2 answer (algorithm used to hash admin's password in the DB): pbkdf2_sha256$ . Passwords are stored as salted, iterated
    # Synthesis answer (how to revoke a token):  one-way hashes so a database leak doesn't expose the actual passwords.

    return Response({"message": "Token authenticated.", "user": request.user.username})


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 4 — JSON Web Tokens (JWT)
# ─────────────────────────────────────────────────────────────────────────────

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def jwt_protected_view(request):
    # Reporter — Phase 4 challenge answers:
                                           
    # Q1 answer (fields found in the decoded payload): # Payload also contains: user_id (plus token_type and jti).
    # Q2 answer (what happens when the signature is tampered):# The server validates the token by recomputing the signature with its secret
                                                              
    # Synthesis answer (JWT revocation challenge and workaround): # The server returned 401. The payload is just Base64-encoded JSON that anyone
                                                                # can edit, but changing it invalidates the signature. Without the server's
                                                                # secret key, the attacker can't produce a signature that matches, so the token is rejected.

    return Response({"message": "JWT authenticated.", "user": request.user.username})

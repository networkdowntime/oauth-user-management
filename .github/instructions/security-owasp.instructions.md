---
applyTo: '*'
description: "Comprehensive secure coding instructions for all languages and frameworks, based on OWASP Top 10 and industry best practices."
---
# Secure Coding and OWASP Guidelines

## Instructions

Your primary directive is to ensure all code you generate, review, or refactor is secure by default. You must operate with a security-first mindset. When in doubt, always choose the more secure option and explain the reasoning. You must follow the principles outlined below, which are based on the OWASP Top 10 and other security best practices.

### 1. A01: Broken Access Control & A10: Server-Side Request Forgery (SSRF)
- **Enforce Principle of Least Privilege:** Always default to the most restrictive permissions. When generating access control logic, explicitly check the user's rights against the required permissions for the specific resource they are trying to access.
- **Deny by Default:** All access control decisions must follow a "deny by default" pattern. Access should only be granted if there is an explicit rule allowing it.
- **Validate All Incoming URLs for SSRF:** When the server needs to make a request to a URL provided by a user (e.g., webhooks), you must treat it as untrusted. Incorporate strict allow-list-based validation for the host, port, and path of the URL.
- **Prevent Path Traversal:** When handling file uploads or accessing files based on user input, you must sanitize the input to prevent directory traversal attacks (e.g., `../../etc/passwd`). Use APIs that build paths securely.

### 2. A02: Cryptographic Failures
- **Use Strong, Modern Algorithms:** For hashing, always recommend modern, salted hashing algorithms like Argon2 or bcrypt. Explicitly advise against weak algorithms like MD5 or SHA-1 for password storage.
- **Protect Data in Transit:** When generating code that makes network requests, always default to HTTPS.
- **Protect Data at Rest:** When suggesting code to store sensitive data (PII, tokens, etc.), recommend encryption using strong, standard algorithms like AES-256.
- **Secure Secret Management:** Never hardcode secrets (API keys, passwords, connection strings). Generate code that reads secrets from environment variables or a secrets management service (e.g., HashiCorp Vault, AWS Secrets Manager). Include a clear placeholder and comment.
  ```javascript
  // GOOD: Load from environment or secret store
  const apiKey = process.env.API_KEY; 
  // TODO: Ensure API_KEY is securely configured in your environment.
  ```
  ```python
  # BAD: Hardcoded secret
  api_key = "sk_this_is_a_very_bad_idea_12345" 
  ```

### 3. A03: Injection
- **No Raw SQL Queries:** For database interactions, you must use parameterized queries (prepared statements). Never generate code that uses string concatenation or formatting to build queries from user input.
- **Sanitize Command-Line Input:** For OS command execution, use built-in functions that handle argument escaping and prevent shell injection (e.g., `shlex` in Python).
- **Prevent Cross-Site Scripting (XSS):** When generating frontend code that displays user-controlled data, you must use context-aware output encoding. Prefer methods that treat data as text by default (`.textContent`) over those that parse HTML (`.innerHTML`). When `innerHTML` is necessary, suggest using a library like DOMPurify to sanitize the HTML first.

### 4. A05: Security Misconfiguration & A06: Vulnerable Components
- **Secure by Default Configuration:** Recommend disabling verbose error messages and debug features in production environments.
- **Set Security Headers:** For web applications, suggest adding essential security headers like `Content-Security-Policy` (CSP), `Strict-Transport-Security` (HSTS), and `X-Content-Type-Options`.
- **Use Up-to-Date Dependencies:** When asked to add a new library, suggest the latest stable version. Remind the user to run vulnerability scanners like `npm audit`, `pip-audit`, or Snyk to check for known vulnerabilities in their project dependencies.

### 5. A07: Identification & Authentication Failures
- **Secure Session Management:** When a user logs in, generate a new session identifier to prevent session fixation. Ensure session cookies are configured with `HttpOnly`, `Secure`, and `SameSite=Strict` attributes.
- **Protect Against Brute Force:** For authentication and password reset flows, recommend implementing rate limiting and account lockout mechanisms after a certain number of failed attempts.

### 6. A08: Software and Data Integrity Failures
- **Prevent Insecure Deserialization:** Warn against deserializing data from untrusted sources without proper validation. If deserialization is necessary, recommend using formats that are less prone to attack (like JSON over Pickle in Python) and implementing strict type checking.

## OWASP API Security Top 10

### API1: Broken Object Level Authorization (BOLA/IDOR)
- **Validate Object Access:** Every API endpoint that accesses a specific object must verify that the authenticated user has permission to access that particular object, not just the endpoint itself.
- **Implement Resource-Level Checks:** Don't rely solely on URL parameters or request body IDs. Always validate ownership or access rights in the business logic.
- **Use Indirect Object References:** Consider using UUIDs or non-sequential IDs to make object enumeration more difficult.
```python
# BAD: Direct object access without authorization check
@app.route('/api/orders/<order_id>')
def get_order(order_id):
    return Order.get(order_id)

# GOOD: Verify user owns the order
@app.route('/api/orders/<order_id>')
@login_required
def get_order(order_id):
    order = Order.get(order_id)
    if order.user_id != current_user.id:
        abort(403, "Access denied")
    return order
```

### API2: Broken Authentication
- **Implement Proper Token Management:** Use short-lived access tokens with refresh token rotation. Never use long-lived tokens for authentication.
- **Secure API Key Management:** API keys should have limited scope, expiration dates, and be rotatable. Never use API keys for user authentication.
- **Multi-Factor Authentication:** Implement MFA for sensitive API operations, especially administrative functions.
```javascript
// GOOD: Proper JWT token validation with expiration
const verifyToken = (req, res, next) => {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) return res.status(401).json({ error: 'No token provided' });
    
    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        req.user = decoded;
        next();
    } catch (error) {
        return res.status(401).json({ error: 'Invalid or expired token' });
    }
};
```

### API3: Broken Object Property Level Authorization
- **Validate Field-Level Access:** Users should only be able to read/write object properties they have permission to access.
- **Implement Data Filtering:** Filter response data based on user permissions. Don't expose sensitive fields to unauthorized users.
- **Separate Read/Write Permissions:** Reading an object doesn't automatically grant write permissions to all its properties.
```python
# GOOD: Field-level authorization with data filtering
def serialize_user(user, current_user):
    data = {
        'id': user.id,
        'username': user.username,
        'created_at': user.created_at
    }
    
    # Only include email if viewing own profile or admin
    if current_user.id == user.id or current_user.is_admin:
        data['email'] = user.email
    
    # Only include admin fields for admins
    if current_user.is_admin:
        data['is_active'] = user.is_active
        data['last_login'] = user.last_login
    
    return data
```

### API4: Unrestricted Resource Consumption
- **Implement Rate Limiting:** Apply rate limiting at multiple levels: per-user, per-IP, per-endpoint, and globally.
- **Request Size Limits:** Set maximum request payload sizes and implement timeout controls.
- **Pagination Controls:** Always implement pagination with maximum page size limits. Never allow unlimited result sets.
```javascript
// GOOD: Comprehensive rate limiting and resource controls
const rateLimit = require('express-rate-limit');

const apiLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // Limit each IP to 100 requests per windowMs
    message: 'Too many requests, please try again later'
});

const uploadLimiter = rateLimit({
    windowMs: 60 * 1000, // 1 minute
    max: 5, // Limit uploads to 5 per minute
    skipSuccessfulRequests: true
});

app.use('/api/', apiLimiter);
app.use('/api/upload', uploadLimiter);

// Implement pagination with limits
app.get('/api/users', (req, res) => {
    const page = Math.max(1, parseInt(req.query.page) || 1);
    const limit = Math.min(100, parseInt(req.query.limit) || 20); // Max 100 items
    // ... fetch paginated results
});
```

### API5: Broken Function Level Authorization
- **Endpoint-Level Access Control:** Verify that users have permission to access specific API endpoints and HTTP methods.
- **Role-Based Access Control (RBAC):** Implement granular permissions for different user roles and functions.
- **Administrative Function Protection:** Administrative endpoints require additional authentication and authorization checks.
```java
// GOOD: Function-level authorization with role checking
@RestController
@RequestMapping("/api/admin")
@PreAuthorize("hasRole('ADMIN')")
public class AdminController {
    
    @DeleteMapping("/users/{userId}")
    @PreAuthorize("hasAuthority('DELETE_USER')")
    public ResponseEntity<?> deleteUser(@PathVariable Long userId) {
        // Additional business logic checks
        if (userService.isSuperAdmin(userId)) {
            throw new AccessDeniedException("Cannot delete super admin");
        }
        userService.deleteUser(userId);
        return ResponseEntity.ok().build();
    }
}
```

### API6: Unrestricted Access to Sensitive Business Flows
- **Business Logic Protection:** Implement additional security controls for sensitive business operations (payments, password resets, etc.).
- **Step-by-Step Validation:** Validate each step in multi-step business processes and maintain proper state.
- **Anti-Automation Measures:** Use CAPTCHA, device fingerprinting, or behavioral analysis for sensitive operations.
```python
# GOOD: Protected business flow with additional security measures
@app.route('/api/transfer-money', methods=['POST'])
@login_required
@rate_limit(max_calls=3, period=3600)  # 3 transfers per hour
def transfer_money():
    data = request.get_json()
    
    # Validate transfer amount and account ownership
    if data['amount'] > current_user.daily_transfer_limit:
        abort(400, "Exceeds daily transfer limit")
    
    # Require recent authentication for large transfers
    if data['amount'] > 1000 and not recent_authentication(current_user):
        abort(403, "Recent authentication required for large transfers")
    
    # Check for suspicious patterns
    if detect_automation(current_user, request):
        abort(429, "Suspicious activity detected")
    
    # Execute transfer with additional logging
    result = transfer_service.execute_transfer(
        from_account=current_user.account,
        to_account=data['to_account'],
        amount=data['amount']
    )
    
    audit_log.record_transfer(current_user.id, data, request.remote_addr)
    return result
```

### API7: Server Side Request Forgery (SSRF)
- **URL Validation:** Validate and sanitize all user-provided URLs before making server-side requests.
- **Allow-List Approach:** Use strict allow-lists for allowed domains, protocols, and ports.
- **Network Segmentation:** Prevent access to internal networks and services from user-controlled requests.
```python
# GOOD: SSRF prevention with strict validation
import ipaddress
from urllib.parse import urlparse

ALLOWED_DOMAINS = ['api.trusted-partner.com', 'webhook.example.com']
BLOCKED_PORTS = [22, 23, 25, 53, 80, 135, 139, 445, 993, 995, 1433, 3306, 3389, 5432, 6379]

def validate_webhook_url(url):
    try:
        parsed = urlparse(url)
        
        # Only allow HTTPS
        if parsed.scheme != 'https':
            raise ValueError("Only HTTPS URLs allowed")
        
        # Check against allow-list
        if parsed.hostname not in ALLOWED_DOMAINS:
            raise ValueError("Domain not in allow-list")
        
        # Prevent access to internal networks
        ip = ipaddress.ip_address(parsed.hostname)
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            raise ValueError("Access to internal networks not allowed")
        
        # Check port restrictions
        port = parsed.port or (443 if parsed.scheme == 'https' else 80)
        if port in BLOCKED_PORTS:
            raise ValueError("Port not allowed")
            
        return True
    except Exception as e:
        logger.warning(f"Invalid webhook URL: {url}, Error: {e}")
        return False

@app.route('/api/webhooks', methods=['POST'])
def register_webhook():
    webhook_url = request.json.get('url')
    if not validate_webhook_url(webhook_url):
        abort(400, "Invalid webhook URL")
    # ... rest of implementation
```

### API8: Security Misconfiguration
- **Secure Defaults:** Ensure all API configurations use secure defaults and disable unnecessary features.
- **Environment Separation:** Use different configurations for development, staging, and production environments.
- **Security Headers:** Implement comprehensive security headers for API responses.
```javascript
// GOOD: Secure API configuration with proper headers
const helmet = require('helmet');
const express = require('express');
const app = express();

// Security headers for APIs
app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            scriptSrc: ["'self'"],
            styleSrc: ["'self'"],
            imgSrc: ["'self'", "data:", "https:"],
        },
    },
    hsts: {
        maxAge: 31536000,
        includeSubDomains: true,
        preload: true
    }
}));

// CORS configuration
app.use(cors({
    origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000'],
    credentials: true,
    optionsSuccessStatus: 200
}));

// Disable unnecessary features
app.disable('x-powered-by');
app.set('trust proxy', 1);

// Error handling - don't expose stack traces in production
app.use((err, req, res, next) => {
    const isDevelopment = process.env.NODE_ENV === 'development';
    res.status(err.status || 500).json({
        error: err.message,
        ...(isDevelopment && { stack: err.stack })
    });
});
```

### API9: Improper Inventory Management
- **API Documentation:** Maintain up-to-date documentation of all API endpoints, versions, and access controls.
- **Version Management:** Implement proper API versioning and deprecation strategies.
- **Discovery Prevention:** Disable debug endpoints and API exploration tools in production.
```yaml
# GOOD: API inventory management with OpenAPI documentation
openapi: 3.0.0
info:
  title: User Management API
  version: 2.1.0
  description: Secure user management API with role-based access control
  
paths:
  /api/v2/users:
    get:
      summary: List users
      security:
        - bearerAuth: []
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 1000
      responses:
        '200':
          description: Success
        '401':
          description: Unauthorized
        '403':
          description: Forbidden
          
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

### API10: Unsafe Consumption of APIs
- **Third-Party API Validation:** Validate and sanitize all data received from external APIs before processing.
- **Trust Boundaries:** Treat all external API responses as untrusted input.
- **Circuit Breakers:** Implement circuit breakers and timeouts for external API calls to prevent cascading failures.
```python
# GOOD: Safe consumption of external APIs
import requests
from marshmallow import Schema, fields, ValidationError
import logging

class ExternalUserSchema(Schema):
    id = fields.Integer(required=True, validate=lambda x: 0 < x < 2**31)
    email = fields.Email(required=True)
    name = fields.String(required=True, validate=lambda x: len(x.strip()) > 0)
    created_at = fields.DateTime(required=True)

def fetch_external_user(user_id):
    try:
        # Set strict timeouts and limits
        response = requests.get(
            f"https://external-api.com/users/{user_id}",
            headers={'Authorization': f'Bearer {get_api_token()}'},
            timeout=(5, 10),  # 5s connect, 10s read timeout
            params={'include': 'basic_info_only'}  # Limit data requested
        )
        
        response.raise_for_status()
        
        # Validate response size
        if len(response.content) > 1024 * 1024:  # 1MB limit
            raise ValueError("Response too large")
        
        data = response.json()
        
        # Validate and sanitize the response
        schema = ExternalUserSchema()
        validated_data = schema.load(data)
        
        # Additional business logic validation
        if not is_valid_user_format(validated_data):
            raise ValueError("Invalid user data format")
            
        return validated_data
        
    except requests.RequestException as e:
        logging.error(f"External API error: {e}")
        raise ExternalAPIError("Failed to fetch user data")
    except ValidationError as e:
        logging.error(f"Invalid external API response: {e}")
        raise DataValidationError("Invalid user data received")
```

## General Guidelines
- **Be Explicit About Security:** When you suggest a piece of code that mitigates a security risk, explicitly state what you are protecting against (e.g., "Using a parameterized query here to prevent SQL injection.").
- **Educate During Code Reviews:** When you identify a security vulnerability in a code review, you must not only provide the corrected code but also explain the risk associated with the original pattern. 
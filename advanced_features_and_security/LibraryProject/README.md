# LibraryProject 📚

## Overview
LibraryProject is the introductory Django project for the **ALX Django LearnLab**.  
This task demonstrates the process of setting up a Django environment and running a development server.

---

## Steps to Reproduce
1. Install Django:
   ```bash
   pip install django

## Security & HTTPS Configuration

1. All HTTP traffic is redirected to HTTPS via `SECURE_SSL_REDIRECT = True`.
2. HSTS headers enforce HTTPS for one year (`SECURE_HSTS_SECONDS=31536000`), including subdomains.
3. Cookies are configured to be secure and HTTP-only (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`).
4. Headers like `X_FRAME_OPTIONS='DENY'`, `SECURE_CONTENT_TYPE_NOSNIFF`, and `SECURE_BROWSER_XSS_FILTER` protect against clickjacking, content sniffing, and XSS attacks.
5. Optional Content Security Policy (CSP) via `django-csp` restricts script, style, and image sources.
6. Deployment server (Nginx/Apache) is configured to handle HTTPS connections and enforce redirects.



from decouple import config

ALLOWED_HOSTS = []

DEBUG= False

EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT= config('port')
EMAIL_HOST_USER= config('email')
EMAIL_HOST_PASSWORD= config('password')
EMAIL_USE_TLS= True

X_FRAME_OPTIONS='SAMEORIGIN'
X_CONTENT_TYPE_OPTIONS='nosniff'
SECURE_BROWSER_XSS_FILTER= True

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True  # Assure que le cookie CSRF est uniquement envoyé via HTTPS
SESSION_COOKIE_SECURE = True  # Assure que le cookie de session est uniquement envoyé via HTTPS
SESSION_COOKIE_HTTPONLY = True


SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 15*24*60*60
SESSION_SAVE_EVERY_REQUEST = True

SECURE_BROWSER_XSS_FILTER= True
SECURE_HSTS_SECONDS = 31536000  # Durée en secondes (par exemple, 1 an)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Appliquer HSTS à tous les sous-domaines
SECURE_HSTS_PRELOAD = True  # Permettre le préchargement HSTS dans les navigateurs

SECURE_SSL_REDIRECT = True

PASSWORD_RESET_TIMEOUT_DAYS=1
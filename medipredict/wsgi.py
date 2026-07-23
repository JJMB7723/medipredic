import os
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medipredict.settings')
application = get_wsgi_application()

try:
    print("[*] Running automatic database migrations on startup...")
    call_command('migrate', interactive=False)
    print("[*] Database migrations completed successfully.")
    
    # Auto-create superuser
    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        print("[*] Creating default admin superuser...")
        User.objects.create_superuser('admin', 'admin@medipredict.com', 'AdminPass123!')
        print("[*] Default admin superuser created.")
except Exception as e:
    print(f"[!] Database migrations / superuser creation failed: {e}")

try:
    print("[*] Running automatic collectstatic on startup...")
    call_command('collectstatic', interactive=False, clear=False)
    print("[*] Static files collection completed successfully.")
except Exception as e:
    print(f"[!] Static files collection failed: {e}")


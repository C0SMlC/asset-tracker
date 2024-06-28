from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))  # Default to 8000 for compatibility with Gunicorn
    if os.name == 'nt':  # Windows
        from waitress import serve
        serve(app, host='0.0.0.0', port=port)
    else:  # Unix-like (Linux, macOS)
        app.run(host='0.0.0.0', port=port)

from app import app


__all__ = ('index',)


@app.route('/')
def index():
    return 'Forum!'

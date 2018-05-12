from flask import render_template

from app import app
from db import get_connector
from models import Section


__all__ = ('section_view',)


@app.route('/section/<section_id>', methods=('GET',))
def section_view(section_id):
    section = Section.get(section_id)
    subsections = Section.filter(parent=section.id)
    return render_template('section.html', section=section, subsections=subsections)

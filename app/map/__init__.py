import csv
import json
import logging
import os

from flask import Blueprint, render_template, abort, url_for, flash, current_app, jsonify
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

from app.auth.decorators import admin_required
from app.auth.forms import csv_upload
from app.db import db
from app.db.models import Location
from werkzeug.utils import secure_filename, redirect
from flask import Response

from app.map.forms import location_edit_form, create_location_form

map = Blueprint('map', __name__,
                template_folder='templates')


@map.route('/locations', methods=['GET'], defaults={"page": 1})
@map.route('/locations/<int:page>', methods=['GET'])
def browse_locations(page):
    page = page
    per_page = 10
    pagination = Location.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    new_url = ('map.new_location', [('loc_id', ':id')])
    edit_url = ('map.edit_location', [('loc_id', ':id')])
    delete_url = ('map.delete_location', [('loc_id', ':id')])
    try:
        return render_template('browse_locations.html',
                               data=data,
                               pagination=pagination,
                               Location=Location,
                               new_url=new_url,
                               edit_url=edit_url,
                               delete_url=delete_url)
    except TemplateNotFound:
        abort(404)


@map.route('/locations_datatables/', methods=['GET'])
def browse_locations_datatables():
    data = Location.query.all()
    add_url = url_for('map.new_location')
    edit_url = ('map.edit_location', [('loc_id', ':id')])
    delete_url = ('map.delete_location', [('loc_id', ':id')])
    try:
        return render_template('browse_locations_datatables.html',
                               data=data,
                               Location=Location,
                               new_url=add_url,
                               edit_url=edit_url,
                               delete_url=delete_url)
    except TemplateNotFound:
        abort(404)


@map.route('/locations/new', methods=['POST', 'GET'])
@login_required
def new_location():
    form = create_location_form()
    if form.validate_on_submit():
        location_title = Location.query.filter_by(title=form.title.data).first()
        if location_title is None:
            location = Location(title=form.title.data, longitude=form. longitude.data, latitude=form.latitude.data, population=form.population.data)
            db.session.add(location)
            db.session.commit()
            flash('Congratulations, you added a new location', 'success')
            return redirect(url_for('map.browse_locations_datatables'))
        else:
            flash('Location Already Exists')
            return redirect(url_for('map.browse_locations_datatables'))
    return render_template('location_add.html', form=form)


@map.route('/locations/<int:loc_id>/edit', methods=['POST', 'GET'])
@login_required
@admin_required
def edit_location(loc_id):
    loc = Location.query.get(loc_id)
    form = location_edit_form(obj=loc)
    if form.validate_on_submit():
        loc.title = form.title.data
        loc.population = form.population.data
        db.session.add(loc)
        db.session.commit()
        flash('Location Edited Successfully', 'success')
        current_app.logger.info("edited a location")
        return redirect(url_for('map.browse_locations_datatables'))
    return render_template("location_edit.html", form=form)


@map.route('/locations/<int:loc_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_location(loc_id):
    loc = Location.query.get(loc_id)
    db.session.delete(loc)
    db.session.commit()
    flash('Location Deleted', 'success')
    return redirect(url_for('map.browse_locations_datatables'))

@map.route('/api/locations/', methods=['GET'])
def api_locations():
    data = Location.query.all()
    try:
        return jsonify(data=[location.serialize() for location in data])
    except TemplateNotFound:
        abort(404)


@map.route('/locations/map', methods=['GET'])
def map_locations():
    google_api_key = current_app.config.get('GOOGLE_API_KEY')
    try:
        return render_template('map_locations.html', google_api_key=google_api_key)
    except TemplateNotFound:
        abort(404)


@map.route('/locations/upload', methods=['POST', 'GET'])
@login_required
def location_upload():
    form = csv_upload()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(filepath)
        list_of_locations = []
        with open(filepath) as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                location = Location.query.filter_by(title=row['location']).first()
                if location is None:
                    current_user.locations.append(
                        Location(row['location'], row['longitude'], row['latitude'], row['population']))
                    db.session.commit()
                else:
                    current_user.locations.append(location)
                    db.session.commit()
        return redirect(url_for('map.browse_locations'))

    try:
        return render_template('upload_locations.html', form=form)
    except TemplateNotFound:
        abort(404)

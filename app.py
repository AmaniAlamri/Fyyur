#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from sqlalchemy import func
import sys

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migarte = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
#oneVenueHasManyShows
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String()))#db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website=db.Column(db.String(500))
    seeking_talent=db.Column(db.Boolean, default=False)
    seeking_description=db.Column(db.String)
    facebook_link = db.Column(db.String(120))
    shows=db.relationship('Show', backref='Venue', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website=db.Column(db.String())
    seeking_venue=db.Column(db.Boolean, default=False)
    seeking_description=db.Column(db.String)
    shows=db.relationship('Show', backref='Artist', lazy=True)
    

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


class Show(db.Model):
    __tablename__ = 'Show'  
    
    id=db.Column(db.Integer, primary_key=True)
    venue_id=db.Column(db.Integer,db.ForeignKey(Venue.id),nullable=False)
    venue_name=db.Column(db.String(120))
    artist_id=db.Column(db.Integer,db.ForeignKey(Artist.id),nullable=False)
    artist_name=db.Column(db.String())
    artist_image_link=db.Column(db.String(500))
    start_time=db.Column(db.DateTime)  
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  areas = Venue.query.distinct('city', 'state').order_by('state').all()
  for area in areas:
      area.venues = Venue.query.filter_by(state=area.state, city=area.city)
      
  return render_template('pages/venues.html', areas=areas);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search =request.form.get('search_term','')
  venue=Venue.query.filter(Venue.name.ilike("%" + search + "%")).all()
  data=[]
  
  for v in venue:
    data.append({
    "id": v.id,
    "name":v.name,
    "num_upcoming_shows":len(db.session.query(Show).filter(Show.venue_id == v.id).filter(Show.start_time > datetime.now()).all())
  })
  
  response={}
  
  response={
    "count": len(venue),
    "data": data
  }

  #len() function returns the number of items in an object
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue=Venue.query.get(venue_id)
  data=[]
  past_shows_data=db.session.query(Show).filter(Show.venue_id == venue_id).filter(Show.start_time < datetime.now()).all()
  upcoming_shows_data=db.session.query(Show).filter(Show.venue_id == venue_id).filter(Show.start_time > datetime.now()).all()
  
  past_shows_count=0
  upcoming_shows_count=0
  
  past_shows=[]
  upcoming_shows=[]
  
  for show in past_shows_data:
   past_shows.append({
    "artist_id": show.artist_id,
    "artist_name":show.artist_name,
    "artist_image_link":show.artist_image_link,
    "start_time":str(show.start_time)
  })
  
  for show in upcoming_shows_data:
   upcoming_shows.append({
    "artist_id": show.artist_id,
    "artist_name":show.artist_name,
    "artist_image_link":show.artist_image_link,
    "start_time":str(show.start_time)
  })
  
  data={  
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)}
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form=VenueForm()
  ven=Venue()
  if form.validate_on_submit():
    try:
     ven.name=form.name.data
     ven.genres=request.form.getlist('genres')
     ven.address=form.address.data
     ven.city=form.city.data
     ven.state=form.state.data
     ven.phone=form.phone.data
     ven.website=form.website.data
     ven.facebook_link=form.facebook_link.data
     ven.image_link=form.image_link.data
     ven.seeking_talent=form.seeking_talent.data
     ven.seeking_description=form.seeking_description.data
    
     db.session.add(ven)
     db.session.commit()
   # on successful db insert, flash success
     flash('Venue ' + request.form['name'] +' was successfully listed!')
     return render_template('pages/home.html')
    except:
     flash('An error occurred. Venue ' + form.name.data +' could not be listed.')
     db.session.rollback()
     print(sys.exc_info())
     return render_template('pages/home.html')
     # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    finally:
     db.session.close()  
  flash('Invalid Input')
  return render_template('pages/home.html')
  # TODO: on unsuccessful db insert, flash an error instead.
  
  @app.route('/venues/<int:venue_id>/edit', methods=['GET'])
  def edit_venue(venue_id):
   form = VenueForm()
   venue=Venue.query.get(venue_id)
   
   form.name.data=venue.name
   form.genres.data=venue.genres
   form.city.data=venue.city
   form.address.data= venue.address
   form.state.data=venue.state
   form.phone.data=venue.phone
   form.website.data=venue.website
   form.facebook_link.data=venue.facebook_link
   form.seeking_talent.data=venue.seeking_talent
   form.seeking_description.data=venue.seeking_description
   form.image_link.data=venue.image_link
   
  
   # TODO: populate form with values from venue with ID <venue_id>
   return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue=Venue.query.get(venue_id)
  
  venue.name = request.form['name']
  venue.city = request.form['city']
  venue.address= request.form['address']
  venue.state = request.form['state']
  venue.phone = request.form['phone']
  venue.genres = request.form.getlist('genres')
  venue.image_link = request.form['image_link']
  venue.facebook_link = request.form['facebook_link']
  venue.website = request.form['website']
  venue.seeking_talent = True if 'seeking_talent' in request.form else False 
  venue.seeking_description = request.form['seeking_description']
  db.session.commit()
  
  flash('Venue ' + request.form['name'] + ' was successfully updated!')  
  return redirect(url_for('show_venue', venue_id=venue_id))

@app.route('/venues/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
  venue_name=Venue.query.with_entities(Venue.name).filter_by(id=venue_id).first()
  try:
    venue=Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    flash('Venue ' + venue_name + ' was successfully deleted!')
    return render_template('pages/home.html')
  except:
    db.session.rollback()
    flash('Venue ' + venue_name + ' was not deleted!')
    return render_template('pages/home.html')
  finally:
    db.session.close()  
    
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  #return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=Artist.query.all()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search =request.form.get('search_term','')
  artist=Artist.query.filter(Artist.name.ilike("%" + search + "%")).all()
  data=[]
  
  for a in artist:
    data.append({
    "id": a.id,
    "name":a.name,
    "num_upcoming_shows":len(db.session.query(Show).filter(Show.artist_id == a.id).filter(Show.start_time > datetime.now()).all()),
  })
  
  response={}
  
  response={
    "data": data
  }
  
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist=Artist.query.filter_by(id=artist_id).first()
  data=[]

  past_shows_data=db.session.query(Show).filter(Show.artist_id == artist_id).filter(Show.start_time < datetime.now()).all()
  upcoming_shows_data=db.session.query(Show).filter(Show.artist_id == artist_id).filter(Show.start_time > datetime.now()).all()
  
  past_shows_count=0
  upcoming_shows_count=0
  
  past_shows=[]
  upcoming_shows=[]
  
  for show in past_shows_data:
   past_shows.append({
    "venue_id": show.venue_id,
    "venue_name":show.venue_name,
    "venue_image_link":Venue.query.with_entities(Venue.name).filter_by(id=Show.venue_id).first()[0],#show.venue_image_link,
    "start_time":str(show.start_time)
   })
  
  for show in upcoming_shows_data:
   upcoming_shows.append({
    "venue_id": show.venue_id,
    "venue_name":show.venue_name,
    "venue_image_link":Venue.query.with_entities(Venue.name).filter_by(id=Show.venue_id).first()[0],#show.venue_image_link,
    "start_time":str(show.start_time)
  })
   
 # artist.append({
 #    "past_shows":past_shows,
  #   "upcoming_shows":upcoming_shows,
  #   "past_shows_count":len(past_shows),
   #  "upcoming_shows_count":len(upcoming_shows),
  # })
  data={  
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)}
    
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  art=Artist.query.filter_by(id=artist_id).first()
  form.name.data=art.name,
  form.genres.data=art.genres
  form.city.data=art.city
  form.state.data=art.state
  form.phone.data=art.phone
  form.website.data=art.website
  form.facebook_link.data=art.facebook_link
  form.seeking_venue.data=art.seeking_venue
  form.seeking_description.data=art.seeking_description
  form.image_link.data=art.image_link
  
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=art)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form=ArtistForm()
  artist=Artist.query.filter_by(id=artist_id).first()
  artist.name = request.form['name']
  artist.city = request.form['city']
  artist.state = request.form['state']
  artist.phone = request.form['phone']
  artist.genres = request.form.getlist('genres')
  artist.image_link = request.form['image_link']
  artist.facebook_link = request.form['facebook_link']
  artist.website = request.form['website']
  artist.seeking_venue = True if 'seeking_venue' in request.form else False 
  artist.seeking_description = request.form['seeking_description']
  db.session.commit()
  flash('Artist ' + request.form['name'] + ' was successfully updated!')
  return redirect(url_for('show_artist', artist_id=artist_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  artist=Artist()
  form=ArtistForm()
  if form.validate_on_submit():

   try:
     artist.name=form.name.data
     artist.city=form.city.data
     artist.state=form.state.data
     artist.phone=form.phone.data
     artist.genres=request.form.getlist('genres')
     artist.website=form.website.data
     artist.image_link=form.image_link.data
     artist.seeking_venue=form.seeking_venue.data
     artist.seeking_description=form.seeking_description.data
     artist.facebook_link=form.facebook_link.data
    
     db.session.add(artist)
     db.session.commit()
    # on successful db insert, flash success
     flash('Artist ' + request.form['name'] + ' was successfully listed!')
     return render_template('pages/home.html')
   except: 
    # TODO: on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
      db.session.rollback()
      return render_template('pages/home.html')
   finally:
    db.session.close()
    
  flash('Invalid Input')
  return render_template('pages/home.html')
 
    

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows = Show.query.all()
  data = []
  for show in shows:
      show = {
          "venue_id": show.venue_id,
          "venue_name": show.venue_name,#Venue.query.with_entities(Venue.name).filter_by(id=Show.venue_id).first(),
          "artist_id": show.artist_id,
          "artist_name":show.artist_name,#Artist.query.with_entities(Artist.name).filter_by(id=Show.artist_id).first(),
          "artist_image_link":Artist.query.with_entities(Artist.image_link).filter_by(id=show.artist_id).first()[0],
          "start_time": str(show.start_time)
      }
      data.append(show)
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  show=Show()
  form=ShowForm()
  
  try:
    show.artist_id=form.artist_id.data
    show.venue_id=form.venue_id.data
    show.start_time=form.start_time.data
    #ven_name=Show.query.filter_by(show.venue_id)
    #art_name=Show.query.filter_by(show.artist_id)
    
    db.session.add(show)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')
    return render_template('pages/home.html')
  
  except:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
    return render_template('pages/home.html')

  finally:
    db.session.close()
    
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#


# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

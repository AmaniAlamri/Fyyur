class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.String(120))
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
    
    
    class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website=db.Column(db.String())
    seeking_venue=db.Column(db.Boolean, default=False)
    seeking_description=db.Column(db.String)
    shows=db.relationship('Show', backref='Artist', lazy=True)
    
    
    lass Show(db.Model):
    __tablename__ = 'Show'  
    
    id=db.Column(db.Integer, primary_key=True)
    venue_id=db.Column(db.Integer,db.ForeignKey(Venue.id),nullable=False)#tablename.id
    venue_name=db.Column(db.String(120))
    artist_id=db.Column(db.Integer,db.ForeignKey(Artist.id),nullable=False)#tablename.id
    artist_name=db.Column(db.String())
    artist_image_link=db.Column(db.String(500))
    start_time=db.Column(db.DateTime)
artist4=Artist(name="Guns N Petals",genres="Rock n Roll",city="San Francisco",state= "CA",phone="326-123-5000",website="https://www.gunsnpetalsband.com",facebook_link="https://www.facebook.com/GunsNPetals",seeking_venue=True,seeking_description="Looking for shows to perform at in the San Francisco Bay Area!",image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80");
INSERT INTO "Artist"(name,genres,city,state,phone,website,facebook_link,seeking_venue,seeking_description,image_link) VALUES ('Guns N Petals','Rock n Roll','San Francisco','CA','326-123-5000','https://www.gunsnpetalsband.com','https://www.facebook.com/GunsNPetals',True,'Looking for shows to perform at in the San Francisco Bay Area!','https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80');
INSERT INTO "Artist"(name,genres,city,state,phone,facebook_link,seeking_venue,image_link) VALUES ('Matt Quevedo','Jazz','New York','NY','300-400-5000','https://www.facebook.com/mattquevedo923251523',False,'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80');
INSERT INTO "Artist"(name,genres,city,state,phone,seeking_venue,image_link) VALUES ('The Wild Sax Band',ARRAY['Jazz,Classical'],'San Francisco','CA','432-325-5432',False,'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80');
INSERT INTO "Venue"(name,genres,address,city,state,phone,website,facebook_link,seeking_talent,seeking_description,image_link) VALUES ('he Musical Hop',ARRAY['Jazz','Reggae'],'1015 Folsom Street','San Francisco','CA','3123-123-1234','https://www.themusicalhop.com','https://www.facebook.com/TheMusicalHop',True,'We are on the lookout for a local artist to play every two weeks. Please call us.','https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60');
INSERT INTO "Venue"(name,genres,address,city,state,phone,website,facebook_link,seeking_talent,image_link) VALUES ('The Dueling Pianos Bar',ARRAY['Classical','R&B','Hip-Hop'],'335 Delancey Street','New York','NY','914-003-1132','https://www.theduelingpianos.com','https://www.facebook.com/theduelingpianos',False,'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80');
INSERT INTO "Venue"(name,genres,address,city,state,phone,website,facebook_link,seeking_talent,image_link) VALUES ('Park Square',ARRAY['Rock n Roll','Jazz','Classical','Folk'],'34 Whiskey Moore Ave','San Francisco','CA','415-000-1234','https://www.parksquarelivemusicandcoffee.com','https://www.facebook.com/ParkSquareLiveMusicAndCoffee',False,'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80');
UPDATE "Venue" SET "address"='1015 Folsom Street' where id=1; 
INSERT INTO "Show"(venue_id,venue_name,artist_id,artist_name,artist_image_link,start_time) VALUES (1,'The Musical Hop',4,'Guns N Petals','https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80','2019-05-21T21:30:00.000Z');
INSERT INTO "Show"(venue_id,venue_name,artist_id,artist_name,artist_image_link,start_time) VALUES (3,'Park Square Live Music & Coffee',5,'Matt Quevedo','https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80','2019-06-15T23:00:00.000Z');
INSERT INTO "Show"(venue_id,venue_name,artist_id,artist_name,artist_image_link,start_time) VALUES (3,'Park Square Live Music & Coffee',6,'The Wild Sax Band','https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80','2035-04-01T20:00:00.000Z');
INSERT INTO "Show"(venue_id,venue_name,artist_id,artist_name,artist_image_link,start_time) VALUES (3,'Park Square Live Music & Coffee',6,'The Wild Sax Band','https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80','2035-04-08T20:00:00.000Z');
INSERT INTO "Show"(venue_id,venue_name,artist_id,artist_name,artist_image_link,start_time) VALUES (3,'Park Square Live Music & Coffee',6,'The Wild Sax Band','https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80','2035-04-15T20:00:00.000Z');


for show in shows:
    show = {
      "venue_id":show.venue_id,
      "venue_name":db.session.query(Venue.name).filter_by(id=show.venue_id).first()[0],
      "artist_id":show.artist_id,
      "artist_name":d.artist_name,
      "artist_image_link":show.artist_image_link,
      "start_time":show.start_time 
    }
    # artist
    #.............
   data1={
   "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "past_shows": [{
      "venue_id": 1,
      "venue_name": "The Musical Hop",
      "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 5,
    "name": "Matt Quevedo",
    "genres": ["Jazz"],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "past_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 6,
    "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "past_shows": [],
    "upcoming_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 0,
    "upcoming_shows_count": 3,
  }
    #..........
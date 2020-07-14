from flask import jsonify, request
from application import app, db, ma, jwt, mail
from application import models
from flask_jwt_extended import jwt_required, create_access_token
from flask_mail import Message


@app.route('/planets', methods=['GET'])
def planets():
    planets_list = models.Planet.query.all()
    results = models.planets_schema.dump(planets_list)
    return jsonify(results)


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']

    test = models.User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='email already used'), 409

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    password = request.form['password']

    user = models.User(first_name=first_name,
                       last_name=last_name, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify(message='user created!'), 201


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = models.User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message='Login Granted!', access_token=access_token)
    else:
        return jsonify(message='Bad email/password'), 401


@app.route('/retrieve_password/<string:email>', methods=['GET'])
def retrieve_password(email: str):
    user = models.User.query.filter_by(email=email).first()
    if user:
        msg = Message('your planetary API password is ' + user.password,
                      sender='admin@planetary-api.com', recipients=[email])
        mail.send(msg)
        return jsonify(message='Password send to ' + email)
    else:
        return jsonify(message="The email doesn't exist..."), 401


@app.route('/planet_details/<int:planet_id>', methods=['GET'])
def planet_details(planet_id: int):
    planet = models.Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        result = models.planet_schema.dump(planet)
        return jsonify(result)
    else:
        return jsonify(message="That planet doesn't exist"), 404


@app.route('/add_planet', methods=['POST'])
@jwt_required
def add_planet():
    planet_name = request.form['planet_name']
    planet = models.Planet.query.filter_by(planet_name=planet_name).first()
    if planet:
        return jsonify(message='That planet already exist!'), 409
    else:
        planet_type = request.form['planet_type']
        home_star = request.form['home_star']
        mass = float(request.form['mass'])
        radius = float(request.form['radius'])
        distance = float(request.form['distance'])

        new_planet = models.Planet(planet_name=planet_name,
                                   planet_type=planet_type,
                                   home_star=home_star,
                                   mass=mass,
                                   radius=radius,
                                   distance=distance)

        db.session.add(new_planet)
        db.session.commit()
        return jsonify(message='Planet added!'), 201


@app.route('/update_planet', methods=['PUT'])
@jwt_required
def update_planet():
    planet_id = int(request.form['planet_id'])
    planet = models.Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        planet.planet_name = request.form['planet_name']
        planet.planet_type = request.form['planet_type']
        planet.home_star = request.form['home_star']
        planet.mass = float(request.form['mass'])
        planet.radius = float(request.form['radius'])
        planet.distance = float(request.form['distance'])
        db.session.commit()
        return jsonify(message='Planet updated!'), 202
    else:
        return jsonify(message='Planet does not exist!'), 404


@app.route('/remove_planet/<int:planet_id>', methods=['DELETE'])
@jwt_required
def remove_planet(planet_id: int):
    planet = models.Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify(message='Planet removed!'), 202
    else:
        return jsonify(message='Planet does not exist!'), 404


# flask cli functions
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database Created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database Dropped!')


@app.cli.command('db_seed')
def db_seed():
    mercury = models.Planet(planet_name='Mercury',
                            planet_type='Class D',
                            home_star='Sol',
                            mass=2.258e23,
                            radius=1516,
                            distance=35.98e6)

    venus = models.Planet(planet_name='Venus',
                          planet_type='Class K',
                          home_star='Sol',
                          mass=4.867e24,
                          radius=3760,
                          distance=67.24e6)

    earth = models.Planet(planet_name='Earth',
                          planet_type='Class M',
                          home_star='Sol',
                          mass=5.972e24,
                          radius=3959,
                          distance=92.96e6)

    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)

    test_user = models.User(first_name='William',
                            last_name='Herschel',
                            email='test@test.com',
                            password='P@ssw0rd')

    db.session.add(test_user)
    db.session.commit()
    print('Database Seeded!')

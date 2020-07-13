from flask import jsonify
from application import app, db, ma
from application import models


@app.route('/planets', methods=['GET'])
def planets():
    planets_list = models.Planet.query.all()
    results = models.planets_schema.dump(planets_list)
    return jsonify(results)


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

# Author:  DINDIN Meryll
# Date:    20 July 2019
# Project: RoadBuddy

from flask import Flask
from flask import request
from flask import Response

try: from interaction.jokes import *
except: from jokes import *
try: from interaction.places import *
except: from places import *
try: from interaction.vehicle import *
except: from vehicle import *

with open('credentials/key_BEANSTALK.json') as raw: crd = json.load(raw)
application = Flask(__name__)
application.secret_key = crd['key']

# Defines the request objects
car = CarStatus()
car.set_access(code=crd['token'])
pos = car.get()

# pos = {'latitude': 37.78742599487305, 
#        'longitude': -122.39665222167969, 
#        'range': 195.28, 
#        'percentRemaining': 0.64}

plc = PlacesOfInterest()
jks = DadJoke()
fct = FunFact()

@application.route('/exchange', methods=['POST'])
def exchange():

    bdy, arg = '', dict(request.args)
    # try: pos = car.get()
    # except: pass

    if arg['objective'] == 'enumerate':
        msg = plc.get(pos)
        cor = ' ,'.join([e['title'] for e in msg])
        bdy = 'Do you wanna know more about your surroundings? ' 
        bdy += 'Here are five places I picked for you: {}'.format(cor)
    if arg['objective'] == 'joke':
        bdy = 'Okay, here is a good one for you! '
        bdy += jks.get()
    if arg['objective'] == 'funfact':
        bdy = 'Have been scratching my head on this one. '
        bdy += 'Did you know that ' + fct.get()

    if pos['percentRemaining'] < 0.70:
        bdy += ' By the way, you should consider taking a small break, '
        bdy += 'and charge your car which is {} percent loaded.'.format(int(pos['percentRemaining']*100))

    arg = {'status': 200, 'mimetype': 'application/json'}
    return Response(response=json.dumps({'success': True, 'body': bdy}), **arg)

@application.route('/refresh', methods=['POST'])
def refresh():

    car.set_access(code=None)

    arg = {'status': 200, 'mimetype': 'application/json'}
    return Response(response=json.dumps({'success': True}), **arg)

# if __name__ == '__main__':

    # application.run(host='127.0.0.1', port=8080)

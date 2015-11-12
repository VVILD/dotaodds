from django.core.management.base import BaseCommand
from myapp.models import Match,Links
import json
import time
import dateutil.parser
import datetime
import urllib
import requests
from datetime import date,timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from bs4 import BeautifulSoup
import urllib2
import json
import re



# linktype = models.CharField(max_length=10, choices=(,),null=True, blank=True)

class Command(BaseCommand):
    args = 'Arguments is not needed'
    help = 'Django admin custom command poc.'

    def handle(self, *args, **options):

        def d2l_parser(url):
            
            soup = BeautifulSoup(urllib2.urlopen(url).read(),"lxml")     
            data  = soup.find_all("script")
            count=0
            z=data[4].string
            split=z.split(';')
            teama=float(split[0][11:])
            teamb=float(split[1][13:])
            d2l_max=max([teama/teamb,teamb/teama])
            d2l_min=min([teama/teamb,teamb/teama])

            data  = soup.find_all("div", class_="half")

            time=data[0].string
            return [d2l_max,d2l_min,time]


        def vpg_parser(url):
            
            soup = BeautifulSoup(urllib2.urlopen(url).read(),"lxml")     
            data  = soup.find_all("span", class_="vp-item-odds")
            vp_list=[]

        #   print "vpgame normal odds"
            for x in data:
        #       print x.string
                vp_list.append(float(x.string))

            vp_max=max(vp_list)
            vp_min=min(vp_list)
            data  = soup.find_all("span", class_="vp-gold-odds hides")
            vpp_list=[]
            for x in data:
                vpp_list.append(float(x.string))

            vpp_max=max(vpp_list)
            vpp_min=min(vpp_list)

            time="live"
            data  = soup.find_all("span", class_="timewill")
            for x in data:
                time=x.string


            return [vp_max,vp_min,vpp_max,vpp_min,time]



        def d2b_parser(url):
            
            soup = BeautifulSoup(urllib2.urlopen(url).read(),"lxml")     
            data  = soup.find_all("script")
            count=0
            z=data[10].string
            split=z.split(';')
            #print split
            # print "d2b dota odds"
            # print split[0][17:]
            # print split[1][17:]


            d2b_max= max([float(split[0][17:]),float(split[1][17:])])
            d2b_min= min([float(split[0][17:]),float(split[1][17:])])
            

            d2bc_max= max([float(split[2][21:]),float(split[3][21:])])
            d2bc_min= min([float(split[2][21:]),float(split[3][21:])])

            # print split[2][21:]
            # print split[3][21:]

            data  = soup.find_all("div", class_="time")
            time = data[0].string


            # teama=float(split[0][11:])
            # teamb=float(split[1][13:])

            # print "d2b odds"
            # print teama/teamb
            # print teamb/teama

            # data  = soup.find_all("div", class_="half")

            # print "d2b time"  
            # print data[0].string

            return [d2b_max,d2b_min,d2bc_max,d2bc_min,time]


#('d2l', 'dota2lounge'), ('d2byd', 'vpgame dota'), ('vpp', 'vpgame p coins'), ('d2byd', 'dota 2 bestyolo dota'), ('d2byc', 'dota 2 bestyolo csgo')

        active_match=Match.objects.filter(is_active=True).prefetch_related('links_set')
        d2l_links=Links.objects.filter(match__in=active_match,linktype='d2l')
        for link in d2l_links:
            result=d2l_parser(link.link)
            link.team1odd=result[0]
            link.team2odd=result[1]
            link.time_left=result[2]
            link.save()

        vpd_links=Links.objects.filter(match__in=active_match,linktype='vpd')
        for link in vpd_links:
            result=vpg_parser(link.link)
            link.team1odd=result[0]
            link.team2odd=result[1]
            link.time_left=result[4]
            link.save()

        vpp_links=Links.objects.filter(match__in=active_match,linktype='vpp')
        for link in vpp_links:
            result=vpg_parser(link.link)
            link.team1odd=result[2]
            link.team2odd=result[3]
            link.time_left=result[4]
            link.save()

        d2byd_links=Links.objects.filter(match__in=active_match,linktype='d2byd')
        for link in d2byd_links:
            result=d2b_parser(link.link)
            link.team1odd=result[0]
            link.team2odd=result[1]
            link.time_left=result[4]
            link.save()

        d2byc_links=Links.objects.filter(match__in=active_match,linktype='d2byc')
        for link in d2byc_links:
            result=d2b_parser(link.link)
            link.team1odd=result[2]
            link.team2odd=result[3]
            link.time_left=result[4]
            link.save()
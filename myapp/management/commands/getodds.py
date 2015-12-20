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
from concurrent import futures



# linktype = models.CharField(max_length=10, choices=(,),null=True, blank=True)

class Command(BaseCommand):
    args = 'Arguments is not needed'
    help = 'Django admin custom command poc.'

    def handle(self, *args, **options):


        def nxt_parser(url):
            
            soup = BeautifulSoup(urllib2.urlopen(url).read(),"html.parser")     
            
            data  = soup.find_all("span", class_="potential_reward")

            data1  = soup.find_all("span", class_="potential_reward1")

            # z=data[4].string
            # split=z.split(';')
            teama=float(data[0].string)
            teamb=float(data1[0].string)

            # print "d2l odds"
            # print teama/teamb
            # print teamb/teama

            d2l_max=max([teamb,teama])
            d2l_min=min([teamb,teama])

            # data  = soup.find_all("div", class_="half")

            return [d2l_max,d2l_min,""]

    # print "d2l time"  
    # print data[0].string

#d2t_parser(d2t_url)


        def d2t_parser(url):
            
            soup = BeautifulSoup(urllib2.urlopen(url).read(),"html.parser")     
            
            data  = soup.find_all("div", class_=None)


            a=data[3].string
            b=data[5].string

            c="".join(a.split())
            d="".join(b.split())

            teama=float(c[2:])
            teamb=float(d[2:])



            data  = soup.find_all("span", class_=None)

            time=data[0].string
            

            d2l_max=max([teamb,teama])
            d2l_min=min([teamb,teama])

            return [d2l_max,d2l_min,time]

        def d2l_parser(url):
            
            soup = BeautifulSoup(urllib2.urlopen(url).read(), 'html.parser')     
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
            
            soup = BeautifulSoup(urllib2.urlopen(url).read(), 'html.parser')     
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
            
            soup = BeautifulSoup(urllib2.urlopen(url).read(), 'html.parser')     
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
        # d2l_links=Links.objects.filter(match__in=active_match,linktype='d2l')
        def fun_d2l(link):
        # for link in d2l_links:
            result=d2l_parser(link.link)
            link.team1odd=result[0]
            link.team2odd=result[1]
            link.time_left=result[2].encode("utf-8")
            link.save()
            # msg1=str(link.match.pk)+str('.teama.d2l,')+str(result[0])
            # msg2=str(link.match.pk)+str('.teamb.d2l,')+str(result[1])
            # msg3=str(link.match.pk)+str('.time.d2l,')+str(result[2])
            # r.publish("b2c", msg1)
            # r.publish("b2c", msg2)
            # r.publish("b2c", msg3)
            


        def fun_vpd(link):
        # vpd_links=Links.objects.filter(match__in=active_match,linktype='vpd')
        # for link in vpd_links:
            result=vpg_parser(link.link)
            link.team1odd=result[0]
            link.team2odd=result[1]
            link.time_left=result[4].encode("utf-8")
            link.save()

            # msg1=str(link.match.pk)+str('.teama.vpd,')+str(result[0])
            # msg2=str(link.match.pk)+str('.teamb.vpd,')+str(result[1])
            # msg3=str(link.match.pk)+str('.time.vpd,')+str(result[4])
            # r.publish("b2c", msg1)
            # r.publish("b2c", msg2)
            # r.publish("b2c", msg3)


        # vpp_links=Links.objects.filter(match__in=active_match,linktype='vpp')
        # for link in vpp_links:
        def fun_vpp(link):
            result=vpg_parser(link.link)
            link.team1odd=result[2]
            link.team2odd=result[3]
            link.time_left=result[4].encode("utf-8")
            link.save()
            # msg1=str(link.match.pk)+str('.teama.vpp,')+str(result[2])
            # msg2=str(link.match.pk)+str('.teamb.vpp,')+str(result[3])
            # msg3=str(link.match.pk)+str('.time.vpp,')+str(result[4])
            # r.publish("b2c", msg1)
            # r.publish("b2c", msg2)
            # r.publish("b2c", msg3)



        # d2byd_links=Links.objects.filter(match__in=active_match,linktype='d2byd')
        # for link in d2byd_links:
        def fun_d2byd(link):
            result=d2b_parser(link.link)
            link.team1odd=result[0]
            link.team2odd=result[1]
            try:
                link.time_left=result[4].encode("utf-8")
            except:
                link.time_left='live'
                result[4]='live'
            link.save()

            # msg1=str(link.match.pk)+str('.teama.d2byd,')+str(result[0])
            # msg2=str(link.match.pk)+str('.teamb.d2byd,')+str(result[1])
            # msg3=str(link.match.pk)+str('.time.d2byd,')+str(result[4].encode("utf-8"))
            # r.publish("b2c", msg1)
            # r.publish("b2c", msg2)
            # r.publish("b2c", msg3)



        # d2byc_links=Links.objects.filter(match__in=active_match,linktype='d2byc')
        # for link in d2byc_links:
        def fun_d2byc(link):
            result=d2b_parser(link.link)
            link.team1odd=result[2]
            link.team2odd=result[3]
            try:
                link.time_left=result[4].encode("utf-8")
            except:
                link.time_left='live'
                result[4]='live'
            link.save()

            # msg1=str(link.match.pk)+str('.teama.d2byc,')+str(result[2])
            # msg2=str(link.match.pk)+str('.teamb.d2byc,')+str(result[3])
            # msg3=str(link.match.pk)+str('.time.d2byc,')+str(result[4].encode("utf-8"))

            # r.publish("b2c", msg1)
            # r.publish("b2c", msg2)
            # r.publish("b2c", msg3)

        # d2t_links=Links.objects.filter(match__in=active_match,linktype='d2t')
        # for link in d2t_links:
        def fun_d2t(link):
            result=d2t_parser(link.link)
            link.team1odd=result[0]
            link.team2odd=result[1]
            try:
                link.time_left=result[2].encode("utf-8")
            except:
                link.time_left='live'
                result[4]='live'
            link.save()

            # msg1=str(link.match.pk)+str('.teama.d2byc,')+str(result[2])
            # msg2=str(link.match.pk)+str('.teamb.d2byc,')+str(result[3])
            # msg3=str(link.match.pk)+str('.time.d2byc,')+str(result[4].encode("utf-8"))

            # r.publish("b2c", msg1)
            # r.publish("b2c", msg2)
            # r.publish("b2c", msg3)


        # nxt_links=Links.objects.filter(match__in=active_match,linktype='nxt')
        # for link in nxt_links:
        def fun_nxt(link):
            result=nxt_parser(link.link)
            link.team1odd=result[0]
            link.team2odd=result[1]
            try:
                link.time_left=result[2].encode("utf-8")
            except:
                link.time_left='live'
                result[4]='live'
            link.save()


        def main_function(link):
            result=[]
            try:
                print "started"
                # distributor

                if link.linktype == 'nxt':
                    fun_nxt(link)
                elif link.linktype == 'd2t':
                    fun_d2t(link)
                elif link.linktype == 'd2byc':
                    fun_d2byc(link)
                elif link.linktype == 'd2byd':
                    fun_d2byd(link)
                elif link.linktype == 'vpp':
                    fun_vpp(link)
                elif link.linktype == 'vpd':
                    fun_vpd(link)
                elif link.linktype == 'd2l':
                    fun_d2t(d2l)


                result = {
                    "real_tracking_no": link.link,
                    "company": link.linktype,
                    "updated": True,
                    "error": None
                }


            except Exception,e:

                result = {
                    "real_tracking_no": link.link,
                    "company": link.linktype,
                    "updated": False,
                    "error": str(e)
                }

            return result


        aftership_track_queue = []
        # Track Bluedart shipments for businesses and customers
        aftership_business_shipments = Links.objects.filter(match__in=active_match)

        for aftership_business_shipment in aftership_business_shipments:
            aftership_track_queue.append(aftership_business_shipment)


        if len(aftership_track_queue) > 0:
            with futures.ThreadPoolExecutor(max_workers=15) as executor:
                futures_track = (executor.submit(main_function, item) for item in aftership_track_queue)
                for result in futures.as_completed(futures_track):
                    if result.exception() is not None:
                        print('%s' % result.exception())
                    else:
                        print(result.result())


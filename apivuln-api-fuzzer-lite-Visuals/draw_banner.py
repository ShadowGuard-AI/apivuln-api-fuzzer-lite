#!/usr/bin/env python3
"""Veranda banner: big frog on post, small frog under beam, station table, title painted on collecting crate only.
v1: title on a veranda sign board (wrong carrier). v2: jar labels and notebook also readable (flaw)."""
import sys, random
from PIL import Image, ImageDraw, ImageFont
random.seed(9); mode=sys.argv[1] if len(sys.argv)>1 else "ship"; out=sys.argv[2]
F="fonts/BacasimeAntique.ttf"; W,H=1600,900
img=Image.new("RGB",(W,H),(96,116,92)); d=ImageDraw.Draw(img,"RGBA")
for i,xx in enumerate(range(0,W,92)):
    d.rectangle([xx,0,xx+52,620],fill=(52+i%3*8,74,50))
    for k in range(4):
        x=xx+random.randint(-26,44); y=random.randint(30,400); d.ellipse([x,y,x+104,y+42],fill=(66,110,58))
d.rectangle([0,580,W,640],fill=(205,212,200,90))
d.rectangle([0,640,W,900],fill=(112,88,64))
for y in range(664,900,44): d.line([(0,y),(W,y)],fill=(88,66,46),width=3)
d.rectangle([0,84,W,116],fill=(74,56,40))  # roof beam
d.rectangle([0,540,W,570],fill=(88,66,46))
# small frog under beam above hanging lamp, out of focus (soft, larger pale)
d.ellipse([1052,116,1172,176],fill=(150,120,96)); d.ellipse([1140,124,1196,168],fill=(156,126,100)); d.ellipse([1172,132,1192,152],fill=(240,236,214))
d.line([(1240,116),(1240,196)],fill=(50,44,36),width=4); d.polygon([(1216,196),(1264,196),(1254,246),(1230,246)],fill=(250,230,170)); d.ellipse([1224,204,1260,242],fill=(255,244,190))
# nearest post with large frog at eye level
d.rectangle([120,0,330,900],fill=(106,82,58))
for x in range(140,320,34): d.line([(x,0),(x-12,900)],fill=(88,66,44),width=3)
fx,fy=150,300
d.ellipse([fx,fy,fx+250,fy+160],fill=(168,104,62)); d.ellipse([fx+34,fy+76,fx+236,fy+176],fill=(94,102,112))
d.ellipse([fx+158,fy-60,fx+268,fy+48],fill=(172,110,66)); d.ellipse([fx+208,fy-38,fx+252,fy+6],fill=(250,244,220)); d.ellipse([fx+222,fy-26,fx+242,fy-6],fill=(24,22,18))
d.arc([fx+156,fy+22,fx+246,fy+76],20,150,fill=(128,84,180),width=7)
d.line([(fx+30,fy+128),(fx-24,fy+188)],fill=(150,92,54),width=20)
for k in range(4): d.ellipse([fx-52+k*18,fy+196,fx-34+k*18,fy+214],fill=(228,198,152),outline=(118,86,48),width=2)
# station table with day laid out
d.rectangle([430,590,1180,628],fill=(96,74,52))
for i,x in enumerate((470,575,680)):
    d.rounded_rectangle([x,522,x+84,592],radius=11,fill=(228,230,224),outline=(170,172,166),width=3); d.rectangle([x+10,510,x+74,524],fill=(150,90,50))
    if mode=="v2":
        try: fs=ImageFont.truetype(F,22)
        except: fs=ImageFont.load_default()
        d.text((x+42,556),"specimen",font=fs,fill=(40,44,60),anchor="mm")
d.polygon([(830,592),(862,592),(876,540),(818,540)],fill=(200,220,226)); d.rectangle([806,586,1010,620],fill=(206,198,168),outline=(150,140,110),width=2)
if mode=="v2":
    try: fs=ImageFont.truetype(F,24)
    except: fs=ImageFont.load_default()
    d.text((908,602),"field notes",font=fs,fill=(40,44,60),anchor="mm")
d.ellipse([1040,548,1104,580],outline=(60,56,48),width=5); d.line([(1094,572),(1150,606)],fill=(60,56,48),width=6)
# sketch of a frog foot for toe pads alone
d.rectangle([560,628,760,716],fill=(232,228,206))
for k in range(4): d.ellipse([592+k*36,668,592+k*36+24,690],outline=(90,80,60),width=3)
d.line([(610,640),(700,690)],fill=(90,80,60),width=3)
# collecting crate beside table: slate, one line of lab white paint (ship) ; v1 uses a sign board instead
try: fb=ImageFont.truetype(F,64)
except: fb=ImageFont.load_default()
if mode=="v1":
    d.rectangle([430,150,1090,232],fill=(84,92,104),outline=(240,242,238),width=4)
    d.text((760,190),"apivuln-api-fuzzer-lite",font=fb,fill=(240,242,238),anchor="mm")
    d.rectangle([1200,600,1520,760],fill=(84,92,104))
else:
    d.rectangle([1170,590,1560,780],fill=(84,92,104),outline=(60,66,76),width=5)
    for y in (640,700): d.line([(1170,y),(1560,y)],fill=(64,70,82),width=4)
    d.text((1365,618),"apivuln-api-fuzzer-lite",font=ImageFont.truetype(F,29),fill=(240,242,238),anchor="mm")
img.save(out); print(out,mode)

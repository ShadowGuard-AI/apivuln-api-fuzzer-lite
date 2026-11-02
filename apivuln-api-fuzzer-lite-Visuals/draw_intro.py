#!/usr/bin/env python3
"""Rain tree frog veranda intro, no writing. v1: frog mid-call with pouch inflated (prose: still, deflated).
v2: jar labels facing viewer with marks (flaw). Ship: pouch smooth, labels turned away."""
import sys, random, math
from PIL import Image, ImageDraw
random.seed(23); mode=sys.argv[1] if len(sys.argv)>1 else "ship"; out=sys.argv[2]
W,H=1600,900
img=Image.new("RGB",(W,H),(96,116,92)); d=ImageDraw.Draw(img,"RGBA")
# layered wet forest background
for i,xx in enumerate(range(0,W,90)):
    d.rectangle([xx,0,xx+54,640],fill=(52+i%3*8,74,50))
    for k in range(5):
        x=xx+random.randint(-30,50); y=random.randint(30,420)
        d.ellipse([x,y,x+110,y+44],fill=(66,110,58))
for x in range(0,W,26):
    yy=560+random.randint(0,30); d.ellipse([x,yy,x+15,yy+18],fill=(140,120,180))  # violet shadow leaves
d.rectangle([0,600,W,660],fill=(70,80,66))  # mist band low
for x in range(0,W,60): d.ellipse([x,606,x+90,646],fill=(210,215,205,70))
# veranda floor + rail
d.rectangle([0,660,W,900],fill=(110,86,62))
for y in range(680,900,44): d.line([(0,y),(W,y)],fill=(88,66,46),width=3)
d.rectangle([0,560,W,592],fill=(88,66,46))
for x in range(60,W,180): d.rectangle([x,592,x+18,664],fill=(88,66,46))
# station table midground, seen from behind working side
d.rectangle([180,600,980,640],fill=(96,74,52)); d.rectangle([210,640,246,780],fill=(80,60,42)); d.rectangle([900,640,936,780],fill=(80,60,42))
for i,(x,y) in enumerate([(280,540),(390,528),(500,548)]):  # jars, labels turned fully away (blank backs)
    d.rounded_rectangle([x,y,x+86,y+72],radius=12,fill=(228,230,224),outline=(170,172,166),width=3)
    d.rectangle([x+10,y-12,x+76,y],fill=(150,90,50))
    if mode=="v2": d.line([(x+16,y+24),(x+70,y+24)],fill=(40,44,60),width=4); d.line([(x+16,y+40),(x+60,y+40)],fill=(40,44,60),width=4)
d.polygon([(640,612),(676,612),(692,556),(628,556)],fill=(200,220,226))  # flask of stream water
d.rectangle([740,566,920,606],fill=(206,198,168),outline=(150,140,110),width=2)  # closed damp notebook
d.ellipse([1060,560,1130,596],outline=(60,56,48),width=5); d.line([(1118,584),(1180,624)],fill=(60,56,48),width=6)  # hand lens
d.ellipse([1078,570,1092,584],fill=(255,255,240))  # one point of light
# wet post right foreground
d.rectangle([1250,0,1600,900],fill=(104,80,56))
for x in range(1270,1590,36): d.line([(x,0),(x-14,900)],fill=(86,64,42),width=3)
for _ in range(160):
    x=random.randint(1260,1590); y=random.randint(0,890); d.ellipse([x,y,x+5,y+8],fill=(215,228,232,170))
# copper backed frog clinging at eye level, side grip, toe discs
fx,fy=1330,330
d.ellipse([fx,fy,fx+230,fy+150],fill=(168,104,62))  # copper back body hunched
d.ellipse([fx+30,fy+70,fx+220,fy+168],fill=(94,102,112))  # slate belly
d.ellipse([fx+150,fy-58,fx+252,fy+44],fill=(172,110,66))  # head
d.ellipse([fx+196,fy-38,fx+238,fy+4],fill=(250,244,220)); d.ellipse([fx+208,fy-27,fx+228,fy-7],fill=(26,24,20)); d.ellipse([fx+214,fy-24,fx+221,fy-17],fill=(255,255,255))
if mode=="v1":
    d.ellipse([fx+150,fy+30,fx+226,fy+96],fill=(128,84,180))  # inflated violet pouch (flaw)
else:
    d.arc([fx+148,fy+18,fx+224,fy+72],20,150,fill=(128,84,180),width=7)  # smooth deflated throat line
# legs gripping post edge, toe discs clear circles
for (lx,ly) in [(fx+18,fy+120),(fx+60,fy+150)]:
    d.line([(lx,ly),(lx-58,ly+58)],fill=(150,92,54),width=20)
    for k in range(4): d.ellipse([lx-84+k*17,ly+66,lx-66+k*17,ly+84],fill=(226,196,150),outline=(120,88,50),width=2)
d.line([(fx+120,fy+140),(fx+96,fy+226)],fill=(150,92,54),width=18)
for k in range(4): d.ellipse([fx+70+k*17,fy+224,fx+88+k*17,fy+242],fill=(226,196,150),outline=(120,88,50),width=2)
# slow irregular drip line from roof edge
d.rectangle([0,0,W,26],fill=(70,54,38))
for x in [140,430,760,1010,1210]:
    d.line([(x,26),(x,44)],fill=(200,220,228),width=3); d.ellipse([x-5,44,x+5,58],fill=(200,220,228))
img.save(out); print(out,mode)

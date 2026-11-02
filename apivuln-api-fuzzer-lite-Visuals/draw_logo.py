#!/usr/bin/env python3
"""Frog on a broad leaf, side view, grip as the point. v1: front view cartoon frog (flaw).
v2: toe pads drawn as points, not discs (flaw). Ship: discs, hunched, eye high."""
import sys
from PIL import Image, ImageDraw, ImageFont
mode=sys.argv[1] if len(sys.argv)>1 else "ship"; out=sys.argv[2]
F="fonts/BacasimeAntique.ttf"; W,H=1200,1000
img=Image.new("RGB",(W,H),(238,240,236)); d=ImageDraw.Draw(img,"RGBA")
# broad leaf, lab white central vein fading to pale green torn edge
d.ellipse([90,120,1110,700],fill=(168,205,160)); d.polygon([(90,410),(600,180),(1110,410),(600,640)],fill=(178,212,168))
d.line([(110,410),(1090,410)],fill=(240,242,238),width=16)
for k in range(-4,5):
    if k: d.line([(600,410),(600+k*110,410-150 if k%2 else 300)],fill=(215,232,208),width=5)
for (x,y) in [(980,250),(1040,330),(90,470)]: d.ellipse([x,y,x+52,y+30],fill=(238,240,236))  # insect fed tears
COP=(168,104,62); SLA=(84,92,104); VIO=(128,84,180)
if mode=="v1":
    d.ellipse([420,220,780,560],fill=COP); d.ellipse([470,470,730,600],fill=SLA)
    for ex in (500,660): d.ellipse([ex,250,ex+60,310],fill=(250,244,220)); d.ellipse([ex+18,268,ex+42,292],fill=(20,20,20))
    d.arc([520,380,680,470],20,160,fill=(40,36,30),width=6)
else:
    fx,fy=380,300
    d.ellipse([fx,fy,fx+430,fy+230],fill=COP)          # hunched copper back
    d.ellipse([fx+50,fy+120,fx+410,fy+258],fill=SLA)    # slate belly
    d.ellipse([fx+290,fy-84,fx+470,fy+66],fill=(172,110,66))  # head, eye high
    d.ellipse([fx+372,fy-56,fx+432,fy+4],fill=(250,244,220)); d.ellipse([fx+390,fy-38,fx+416,fy-12],fill=(24,22,18)); d.ellipse([fx+398,fy-33,fx+407,fy-24],fill=(255,255,255))
    d.arc([fx+286,fy+40,fx+430,fy+118],20,150,fill=VIO,width=8)  # deflated violet throat, smooth
    # front foot pressing leaf with four toe discs (points in v2 flaw)
    d.line([(fx+330,fy+190),(fx+392,fy+268)],fill=(150,92,54),width=26)
    for k in range(4):
        x=fx+352+k*30; y=fy+282
        if mode=="v2": d.ellipse([x+10,y+8,x+16,y+14],fill=(60,50,30))
        else: d.ellipse([x,y,x+26,y+22],fill=(228,198,152),outline=(118,86,48),width=3)
    d.line([(fx+70,fy+200),(fx+30,fy+300)],fill=(150,92,54),width=24)
    for k in range(3): d.ellipse([fx-2+k*28,fy+306,fx+24+k*28,fy+326],fill=(228,198,152),outline=(118,86,48),width=3)
try: f=ImageFont.truetype(F,58)
except: f=ImageFont.load_default()
d.text((600,790),"apivuln-api-fuzzer-lite",font=f,fill=SLA,anchor="ma")
d.text((600,880),"The Field Station's Rain Tree Frogs",font=ImageFont.truetype(F,36),fill=(110,116,126),anchor="ma")
img.save(out)
if mode=="ship": img.resize((76,64)).save("scratch/logo64-ship.png")
print(out,mode)

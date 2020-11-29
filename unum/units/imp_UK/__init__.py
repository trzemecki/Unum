"""
UK Imperial units.
Author: L Selter, 2020
Maintainer: L Selter
https://github.com/Tirpitz93
"""

from unum import Unum
unit = Unum.unit
# << uncomment this import if you want to derive your units from SI >>
from unum.units.si import *

# << define your units hereafter, e.g.
#    M  = unit(  'm' , 0          , 'meter'     )
#    KM = unit( 'km' , 1000. * M  , 'kilometer' ) >>

## Length
inch                    = unit('inch' ,          0.0254 * M,         'Inch')
th      = thou          = unit('th' ,           inch/1000,          'Thousandth Inch')
ft      = foot          = unit("ft"   ,         12*inch,            "Foot")
yd      = yard          = unit("yd"   ,         3 * ft,             "Yard")
ch      = chain         = unit("ch"   ,         22 * yd,            "Chain")
fur     = furlong       = unit("fur"  ,         10 * ch,            "Furlong")
mi      = mile          = unit("mi",            8* fur,             "Mile (statute")
lea     = league        = unit("lea",           3*mi,               "League")
ftm     = fathom        = unit("ftm",           6.08*ft,            "Fathom")
cable                   = unit("cable",         100*ftm,            "Cable")
link                    = unit("link",          chain/100,          "Link")
rod     = pole          = unit("rod",           25*link,            "Rod")
namile  = british_nautical_mile = admirality_mile = unit("namile",   10*cable,   "British Nautical Mile")
line                    = unit("line",          inch/12,            "Line")
point                   = unit("point",         6*line,             "Point")
twip                    = unit("twip",          20*point,           "Twip")
pica                    = unit("pica",          12*point,           "Pica")
poppyseed               = unit("poppyseed",     line,               "Poppyseed")
barleycorn              = unit("barleycorn",    4*poppyseed,        "Barley Corn")
palm                    = unit("palm",          3*inch,             "Palm")
digit                   = unit("digit",         palm/4,             "Digit")
nail                    = unit("nail",          3*digit,            "Nail")
finger                  = unit("finger",        7/8*inch,           "Finger")
stick                   = unit("stick",         2*inch,             "Stick")
hand                    = unit("hand",          2*stick,            "Hand")
span                    = unit("span",          4*nail,             "Span")
cubit                   = unit("cubit",         2*span,             "Cubit")
shaftment               = unit("shaftment",     2*palm,             "Shaftment")
pace                    = unit("pace",          5*shaftment,        "Pace")
ell                     = unit("ell",           5*span,             "Ell")
grade = step            = unit("grade",         2*pace,             "Grade")
rope                    = unit("rope",          4* step,            "Rope")
shackle                 = unit("shackle",       15* fathom,         "Shackle")
gunters_chain           = unit("gunters_chain", 11 * fathom,        "Gunter's Chain")
ramsdens_chain          = unit("ramsdens_chain",5*rope,             "Ramsden's Chain")
skein                   = unit("skein",         96*ell,             "Skein")
roman_mile              = unit("roman_mile",    50 *ramsdens_chain, "Roman Mile")
spindle                 = unit("spindle",       120*skein,          "Spindle")
naleague                = unit("naleague",      3*namile,           "Nautical League")

## Area
perch                   = unit("perch",         rod**2,             "Perch")
rood                    = unit("rood",          fur*rod,            "Rood")
acre                    = unit("acre",          fur*ch,             "Acre")


## Volume
fl_oz = fluid_ounce     = unit("fl_oz",         2.84131e-5*m**3,    "Fluid Ounce")
gi = gill               = unit("gi",            5*fl_oz,            "Gill")
pt = pint               = unit("pt",            20*fl_oz,           "Pint")
qt = quart              = unit("qt",            40*fl_oz,           "Quart")
gal = gallon            = unit("gal",           160*fl_oz,          "Gallon")

## Legal
peck                    = unit("peck",      2*gal,              "Peck")
bushel                  = unit("bushel",    4*gal,              "Bushel")


## Apothecary
fluidram = fluid_drachm = unit("fl_drachm",     pint/8,             "Fluid Drachm")
fl_scruple              = unit("fl_scruple",    fluidram/3,         "Fluid Scruple")
minim                   = unit("minim",         fl_scruple/20,      "Minim")

## Mass & weight
lb = pound              = unit("lb",            453.59237*g,        "Pound")
gr = grain              = unit("gr",            0.06479891	* mg,   "Grain")
dr = drachm             = unit("dr",            lb/256,             "Drachm")
oz = ounce              = unit("oz",            lb/16,              "Ounce")
st = stone              = unit("st",            14*lb,              "Stone")
qr = qtr=quarter        = unit("qtr",           28*lb,              "Quarter")
cwt= hundredweight      = unit("cwt",           112*lb,             "Hundredweight")
t = ton                 = unit("ton",             2240* lb,           "Ton")
slug                    = unit("slug",          32.17404856,        "Slug")

# cleaning
del Unum
del unit

"""
UK Imperial units.
Author: L Selter, 2020
Maintainer: L Selter
https://github.com/Tirpitz93

Much of these units are based off: https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/English_Length_Units_Graph.svg/348px-English_Length_Units_Graph.svg.png
and its parent page: https://www.wikiwand.com/en/Imperial_units
as well as: https://www.britannica.com/topic/Imperial-unit


"""
from unum import new_unit
from unum.units import m, mg, g,s
from unum.units.others import g0

# << define your units hereafter, e.g.
#    M  = new_unit(  'm' , 0          , 'meter'     )
#    KM = new_unit( 'km' , 1000. * M  , 'kilometer' ) >>

## Length



###length


inch                    = new_unit('inch' ,          0.0254 * m,         'Inch')
th      = thou          = new_unit('th' ,           inch/1000,          'Thousandth Inch')
ft      = foot          = new_unit("ft"   ,         12*inch,            "Foot")
yd      = yard          = new_unit("yd"   ,         3 * ft,             "Yard")
ch      = chain         = new_unit("ch"   ,         22 * yd,            "Chain")
fur     = furlong       = new_unit("fur"  ,         10 * ch,            "Furlong")
mi      = mile          = new_unit("mi",            8* fur,             "Mile (statute")
lea     = league        = new_unit("lea",           3*mi,               "League")
ftm     = fathom        = new_unit("ftm",           6.08*ft,            "Fathom")
cable                   = new_unit("cable",         100*ftm,            "Cable")
link                    = new_unit("link",          chain/100,          "Link")
rod     = pole          = new_unit("rod",           25*link,            "Rod")
namile  = british_nautical_mile = admirality_mile = new_unit("namile",   10*cable,   "British Nautical Mile")
line                    = new_unit("line",          inch/12,            "Line")
point                   = new_unit("point",         6*line,             "Point")
twip                    = new_unit("twip",          20*point,           "Twip")
pica                    = new_unit("pica",          12*point,           "Pica")
poppyseed               = new_unit("poppyseed",     line,               "Poppyseed")
barleycorn              = new_unit("barleycorn",    4*poppyseed,        "Barley Corn")
palm                    = new_unit("palm",          3*inch,             "Palm")
digit                   = new_unit("digit",         palm/4,             "Digit")
nail                    = new_unit("nail",          3*digit,            "Nail")
finger                  = new_unit("finger",        7/8*inch,           "Finger")
stick                   = new_unit("stick",         2*inch,             "Stick")
hand                    = new_unit("hand",          2*stick,            "Hand")
span                    = new_unit("span",          4*nail,             "Span")
cubit                   = new_unit("cubit",         2*span,             "Cubit")
shaftment               = new_unit("shaftment",     2*palm,             "Shaftment")
pace                    = new_unit("pace",          5*shaftment,        "Pace")
ell                     = new_unit("ell",           5*span,             "Ell")
grade = step            = new_unit("grade",         2*pace,             "Grade")
rope                    = new_unit("rope",          4* step,            "Rope")
shackle                 = new_unit("shackle",       15* fathom,         "Shackle")
chain_g = gunters_chain           = new_unit("gunters chain", 11 * fathom,        "Gunter's Chain")
chain_r = ramsdens_chain          = new_unit("ramsdens chain",5*rope,             "Ramsden's Chain")
skein                   = new_unit("skein",         96*ell,             "Skein")
roman_mile              = new_unit("roman mile",    50 *ramsdens_chain, "Roman Mile")
spindle                 = new_unit("spindle",       120*skein,          "Spindle")
naleague                = new_unit("naleague",      3*namile,           "Nautical League")

## Area
perch                   = new_unit("perch",         rod**2,             "Perch")
rood                    = new_unit("rood",          fur*rod,            "Rood")
acre                    = new_unit("acre",          fur*ch,             "Acre")


## Volume
#https://www.britannica.com/topic/Imperial-unit

fl_oz = fluid_ounce     = new_unit("fl oz",         2.84131e-5*m**3,    "Fluid Ounce")
gi = gill               = new_unit("gi",            5*fl_oz,            "Gill")
pt = pint               = new_unit("pt",            20*fl_oz,           "Pint")
qt = quart              = new_unit("qt",            40*fl_oz,           "Quart")
gal = gallon            = new_unit("gal",           160*fl_oz,          "Gallon")
fluid_dram = fl_d       = new_unit("fl d",           fl_oz/8,          "Fluid Dram")
minim                   = new_unit("minim",           fl_d/60,          "Minim")
peck     = pk           = new_unit("peck",      2*gal,              "Peck")
bushel   = bu           = new_unit("bushel",    4*gal,              "Bushel")




## Mass & weight
#Avoirdupois as default
from unum.units.imp_UK.avoirdupois import *


#force
lbf = pound_force =  new_unit("lb f", lb * g0,"Pound force")

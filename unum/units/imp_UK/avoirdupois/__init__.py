from unum import new_unit
from unum.units import g

lb = pound              = new_unit("lb",            453.59237*g,        "Pound")
gr = grain              = new_unit("gr",            0.06479891	* g,   "Grain")
dr = drachm             = new_unit("dr",            lb/256,             "Drachm")
oz = ounce              = new_unit("oz",            lb/16,              "Ounce")
st = stone              = new_unit("st",            14*lb,              "Stone")
qr = qtr=quarter        = new_unit("qtr",           28*lb,              "Quarter")
cwt= hundredweight      = new_unit("cwt",           112*lb,             "Long Hundredweight")
cwt_s= short_hundredweight      = new_unit("s cwt",           100*lb,             "Short Hundredweight")
t = ton                 = new_unit("ton",             2240* lb,           "Long Ton")
t_s = short_ton                 = new_unit("short ton",             2000* lb,           "Short Ton")
slug                    = new_unit("slug",          32.17404856*lb,        "Slug")

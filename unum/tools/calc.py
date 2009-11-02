#!python
'''
--------------------------------------------------------------------
file : unum/calc/calc.py
ver  : 04.00
role : interactive unit-aware calculator 
--------------------------------------------------------------------

Copyright (C) 2000-2004 Pierre Denis

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
--------------------------------------------------------------------
'''

from unum import Unum, __version__
from unum.units import *
from sys import exc_info

# ---- Unum Calculator parameters ----------------------------------
PROMPT   = ">>> "
S_BANNER = "-- Welcome in Unum Calculator (ver %s) --" % __version__
E_BANNER = "-- end of Unum Calculator session --"


# ---- public functions --------------------------------------------

unit = Unum.unit

def udict():
    ''' returns a dictionary with all defined unums
        (present in the global dictionary)
        with their names as keys
    '''
    unumDict = {}
    globDict = globals()
    for name in list(globDict.keys()):
        value = globDict[name]
        if isinstance(value,Unum):
           unumDict[name] = value
    return unumDict       

def ucat(unum=None):
    ''' displays all the defined units (if unum is None)
        or the selected unum, in the following format :
        "variable name : [symbol] = converted (if any) : name"
        sorted by variable name
    ''' 
    unumDict = udict()
    unumNames = list(unumDict.keys())
    unumNames.sort()
    unitTable = Unum.getUnitTable()
    res = ''
    for unumName in unumNames:
        foundUnum = unumDict[unumName]
        if unum is None or unum is foundUnum:
           if len(foundUnum._unit) == 1:
              symbol = list(foundUnum._unit.keys())[0]
              conv,level,name = unitTable.get(symbol)
              res += "%-10s : %-10s" % (unumName,'[%s]'%symbol)
              if conv is None:
                 res += "   %-21s" % ''
              else:
                 res += " = %-21s" % conv
              res += " : %s\n" % (name)                 
    return res[:-1]

if __name__ == '__main__':

# ---- internal functions ------------------------------------------
          
   def _interpret(s):
       ''' evaluate s and print result if string s is a valid expression
           execute  s                  if string s is a valid statement
           print error message if any standard or Unum exception caught
       '''
       try: 
          try:
             print(eval(s,_globalDict))
          except (Unum.DimensionError,Unum.UnumError) as err:
             print("%s: %s" % (err.__class__,err)) 
       except:
          try:
             exec(s, _globalDict)
          except (Unum.DimensionError,Unum.UnumError) as err:
             print("%s: %s" % (err.__class__,err)) 
          except:
             print("%s: %s" % exc_info()[:2])

# ---- main program ------------------------------------------------

   _globalDict = globals()
   print(S_BANNER)
   while True:
      try:
         _interpret(input(PROMPT))
      except EOFError:
         break
   print(E_BANNER)

# == End of main program ===========================================
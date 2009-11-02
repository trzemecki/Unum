'''
--------------------------------------------------------------------
file : unum/__init__.py
ver  : 04.00
role : define the Unum class
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
import sys

__version__ = '04.01'


# == Unum class =====================================================

class Unum(object):
   ''' Unum instances ('unum') represent numbers with units;
       the class implements the basic arithmetic operators,
       the unit consistency checking and string representation
   '''

   # == Unum class attributes =======================================
   
   # -- parameters --------------------------------------------------
   
   # 1. Unum string representation
   
   UNIT_SEP     = "."
   ''' separator between units
   '''
   
   UNIT_DIV_SEP = "/"
   ''' separator between numerator and denominator;
       if set to None then negative exponents are used
   '''
   
   UNIT_FORMAT  = "[%s]"
   ''' output format string for unit group
   '''
   
   UNIT_INDENT  = " "
   ''' separator between value and units 
   '''
   
   UNIT_HIDE_EMPTY = False
   ''' boolean indicating that unit-less unums must be displayed as
       raw numbers, i.e. without the string UNIT_FORMAT
   '''
   
   UNIT_SORTING    = True
   ''' boolean indicating that units must be sorted alphabetically
       when displayed; if False, then the order is unspecified and
       platform-dependant
   '''
   
   VALUE_FORMAT    = "%s"
   ''' output format string for value
   '''
   
   # 2. Error messages
   
   ERR_UNIT      = "%s incompatible with %s"
   ''' message associated to DimensionError exception, for any units
       inconsistency in addition, subtraction, comparison or conversion
   '''
   
   ERR_EXP       = "unit %s unexpected"
   ''' message associated to DimensionError exception, indicating the
       presence of unit(s) in exponents or mathematical functions
   '''
   
   ERR_BASIC     = "%s not a basic unit"
   ''' message associated to UnumError exception, indicating that a unum
       refers to a non-basic units
   '''
   
   ERR_NOCONVERT = "%s has no conversion"
   ''' message associated to UnumError exception, indicating the absence
       of a conversion unum
   '''
   
   ERR_DUPLICATE = "'%s' is already defined"
   ''' message associated to UnumError exception, indicating that the same
       unit symbol is defined twice
   '''

   # 3. auto-normalization of units

   AUTO_NORM     = True
   ''' boolean indicating whether normalization should be applied
       when displaying unums
   '''

   # == exception classes ===========================================

   class DimensionError(TypeError):
     ''' exception raised for any dimension inconsistency
         (see ERR_UNIT and ERR_EXP message strings above)
     '''
     def __init__(self,unit1,unit2=None):     
         TypeError.__init__(self)
         self.unit1 = unit1
         self.unit2 = unit2
     def __str__(self):    
         if self.unit2 is None:
            res = Unum.ERR_EXP % self.unit1.strUnit()
         else:
            res = Unum.ERR_UNIT % (self.unit1.strUnit(),self.unit2.strUnit())
         return res
       
   class UnumError(Exception):
     ''' exception raised for any inconsistency, except dimension's
         (see ERR_BASIC, ERR_NOCONVERT and ERR_DUPLICATE message strings above)
     '''
     pass          


   # == internal definitions ========================================
   
   # -- internal constants ------------------------------------------
   _NO_UNIT = {}
  
   # -- internal working storage ------------------------------------
   # unit dictionary :
   #  the key is the unit string
   #  the value is a tuple (conversion unum, level, name)
   _unitTable = {}

   # -- definition of instance's attributes -------------------------
   __slots__ = ('_value','_unit','_normal')

        
   # == Unum methods ================================================

   # -- Constructors ------------------------------------------------

   def __init__(self,unit,value=1.0,conv=None,name=''):
       ''' overloaded Unum constructor;
            unit  is a dictionary with pairs (unit symbol : exponent)
            value is a number,
            conv  is None if self does not represent a unit
                  or 0 if self represents a basic unit
                  or a unum equivalent to self, expressed in other unit(s)
                       if self represents a derived unit
            name  is the unit full name if self represents a basic unit
           raises UnumError exception if conv is a unum
                  although unit and value do not represent a basic unit
       '''
       object.__init__(self)
       self._value = value
       self._unit = unit
       if conv is None:
          self._normal = False
       else:
          unit_key = list(unit.keys())[0]
          if unit_key in Unum._unitTable:
             raise Unum.UnumError(Unum.ERR_DUPLICATE % unit_key)
          self._normal = True
          if conv is 0:
             conv_unum = None
             level = 0
          else:
             if (value == 0) or len(unit) != 1 or list(unit.values())[0] != 1:
                raise Unum.UnumError(Unum.ERR_BASIC % self)
             conv_unum = Unum.coerceToUnum(conv)/value
             level = conv_unum.maxLevel() + 1
             conv_unum._normal = True
          Unum._unitTable[unit_key] = conv_unum, level, name

   def copy(self,normalized=False):
       ''' returns a copy of self             if normalized is false
                   a normalized copy of self  otherwise  
       '''
       res = Unum(self._unit.copy(),self._value)
       if normalized:
          res.normalize()
       return res
       
   def as_unit(self,other):
       ''' other is the unum with target unit;
           returns a new unum representing self in converted units;
           raises DimensionError exception if self and other have incompatible units
           raises UnumError exception if other is null or is not a basic unit
       '''
       other = Unum.coerceToUnum(other)
       if (other._value == 0) or (other != Unum(other._unit,1)):
          raise Unum.UnumError(Unum.ERR_BIC % other)
       s, o = self.matchUnits(other)
       res = Unum(other._unit,s._value/o._value)
       res._normal = True
       return res
   
   def replaced(self,u,conv_unum):
       ''' returns a new unum with unit u (string) 
           replaced by conv_unum (unum) in self;
           if u is absent from self then a copy of self is returned
       '''
       res = self.copy() * conv_unum**self._unit[u]
       del res._unit[u]
       return res

   # -- Persistence methods (required by the definition of __slots__)
   
   def __getstate__(self):
       return (self._value,self._unit,self._normal)

   def __setstate__(self,state):
       self._value, self._unit, self._normal = state

   # -- Normalization methods ---------------------------------------
   
   def normalize(self,forDisplay=False):
       ''' changes self to an equivalent unum and returns self;
           the units may be simplified through substitutions 
           ruled by the '_unitTable' class attribute
           rule 1 : least different units
           rule 2 : least substitutions
           if forDisplay is true
             then rule 1 has the following exception :
                  one single unit is preferred to no unit
       '''
       best_l = len(self._unit)
       new_subst_unums = [({},+self)]
       while new_subst_unums:
             subst_unums, new_subst_unums = new_subst_unums, []
             for subst_dict, subst_unum in subst_unums:
                 for u, exp in list(subst_unum._unit.items()):
                     conv_unum = Unum._unitTable[u][0]
                     if conv_unum is not None:
                        new_subst_dict = subst_dict.copy()
                        new_subst_dict[u] = exp + new_subst_dict.get(u,0)
                        is_new = True
                        for subst_dict2, subst_unum2 in new_subst_unums:
                            if new_subst_dict == subst_dict2:
                               is_new = False
                               break
                        if is_new:       
                           s = subst_unum.replaced(u,conv_unum)
                           new_subst_unums.append((new_subst_dict,s))
                           new_l = len(s._unit)
                           if new_l < best_l and not (forDisplay and new_l == 0 and best_l == 1):
                              self._value, self._unit = s._value, s._unit
                              best_l = new_l
       return self                     

   def fix(self):
       ''' prevents implicit normalization on self; 
           returns self
       '''
       self._normal = True
       return self
       
   # -- Checking methods --------------------------------------------
   
   def checkNoUnit(self):
       ''' raises DimensionError exception if self has unit
       '''
       if self._unit:
          raise Unum.DimensionError(self)
   
   def maxLevel(self):
       ''' returns the maximum level of self's units
       '''
       return max([0]+[Unum._unitTable[u][1] for u in list(self._unit.keys())])

   def matchUnits(self,other):
       ''' searches a unit compatible with self and other,
           using by preferrence the units of self or other 
           from the argument of maximum level;
           returns a 2-uple with self and other expressed in this unit;
           raises DimensionError exception if self and other have incompatible units
       '''   
       if self._unit == other._unit:
          res = self, other
       else:   
          s = self.copy()
          o = other.copy()
          s_length, o_length = len(s._unit), len(o._unit)
          revert = s_length > o_length  \
               or (s_length == o_length and s.maxLevel() < o.maxLevel())
          if revert:
             s, o = o, s
          target_unum = Unum(s._unit, 1)
          o /= target_unum
          o.normalize()
          if o._unit:
             raise Unum.DimensionError(self,other)
          o._unit = s._unit
          if revert:
             s, o = o, s
          res = s, o
       return res 

   # -- Arithmetic operator methods ---------------------------------
   
   def __add__(self,other):
       ''' overloading of binary addition operator (self + other);
           returns a new unum;
           raises DimensionError exception if self and other have incompatible units
       '''
       s, o = self.matchUnits(Unum.coerceToUnum(other))
       return Unum(s._unit, s._value + o._value)
   
   def __sub__(self,other):
       ''' overloading of binary substraction operator (self - other);
           returns a new unum;
           raises DimensionError exception if self and other have incompatible units
       '''
       s, o = self.matchUnits(Unum.coerceToUnum(other))
       return Unum(s._unit, s._value - o._value)
                 
   def __pos__(self):
       ''' overloading of unary addition operator (+self);
           returns a new unum with a shared unit dictionary
       '''
       return Unum(self._unit, self._value)

   def __neg__(self):
       ''' overloading of unary substraction operator (-self);
           returns a new unum with a shared unit dictionary
       '''
       return Unum(self._unit, -self._value)

   def __mul__(self,other):
       ''' overloading of multiplication operator (self * other);
           returns a new unum
       '''
       other = Unum.coerceToUnum(other)
       if not self._unit:
          unit = other._unit
       elif not other._unit:
          unit = self._unit
       else:
          unit = self._unit.copy()
          for u, exp in list(other._unit.items()):          
              exp += unit.get(u,0)
              if exp:
                 unit[u] = exp
              else:
                 del unit[u]
       return Unum(unit, self._value * other._value)

   def __div__(self,other):
       ''' overloading of division operator (self / other);
           returns a new unum
       '''
       other = Unum.coerceToUnum(other)
       if not other._unit:
          unit = self._unit
       else: 
          unit = self._unit.copy()
          for u, exp in list(other._unit.items()):          
              exp -= unit.get(u,0)
              if exp:
                 unit[u] = -exp
              else:
                 del unit[u]
       return Unum(unit, self._value / other._value)    
   # Python 3.0 compatibility.
   __truediv__ = __div__
   __floordiv__ = __div__
   
   def __pow__(self,other):
       ''' overloading of exponentiation operator (self ** other);
           returns a new unum;
           raises DimensionError exception if other has unit
       '''
       other = Unum.coerceToUnum(other)
       if other._value:
          other = other.copy(True)
          other.checkNoUnit()       
          unit = self._unit.copy()
          for u in list(self._unit.keys()):
              unit[u] *= other._value
       else:
          unit = Unum._NO_UNIT
       return Unum(unit, self._value ** other._value)

   def __cmp__(self,other):
       ''' overloading of comparison operators (self < other,
           self <= other, self == other, self > other, self >= other);
           returns -1, 0 or 1
           raises DimensionError exception if self and other have incompatible units
       '''
       s, o = self.matchUnits(Unum.coerceToUnum(other))
       return cmp(s._value,o._value)

   def __abs__(self):
       ''' overloading of abs() function;
           returns a new unum 
       '''
       return Unum(self._unit, abs(self._value)) 

   # -- Methods to mix unums with non-unums -------------------------

   def asNumber(self,other=None):
       ''' if other is undefined
            returns the raw value of self;
           else
            returns the raw value of self converted to other's units;
           raises DimensionError exception if self and other have incompatible units
           raises UnumError exception if other is null or is not a basic unit           
       '''
       if other is None:
          res = self.copy(True)._value
       else:
          if isinstance(other,Unum):
             if (other._value == 0) or (other != Unum(other._unit,1)):
                raise Unum.UnumError(Unum.ERR_BASIC % other)
             else:
                s, o = self.matchUnits(other)
                res = s._value / o._value
          else:
             s = self.copy(True)
             s.checkNoUnit()
             res = s._value / other
       return res
       
   def __complex__(self):
       ''' overloading of complex(self) operation
           returns a complex matching self's value
           raises DimensionError exception if self has unit(s)
       '''
       return complex(self.asNumber(1))

   def __int__(self):
       ''' overloading of int(self) operation
           returns an integer matching self's value
           raises DimensionError exception if self has unit(s)
       '''          
       return int(self.asNumber(1))

   def __long__(self):
       ''' overloading of long(self) operation
           returns a long matching self's value
           raises DimensionError exception if self has unit(s)
       '''          
       return int(self.asNumber(1))
   
   def __float__(self):
       ''' overloading of float(self) operation
           returns a float matching self's value
           raises DimensionError exception if self has unit(s)
       '''          
       return float(self.asNumber(1))

   def __radd__(self,other):
       ''' overloading of binary addition operator (other + self)
           where self is a unum while other is not
           returns a new unum;
           raises DimensionError exception if self and other have incompatible units
       '''
       return Unum.coerceToUnum(other).__add__(self)

   def __rsub__(self,other):         
       ''' overloading of binary subtraction operator (other + self)
           where self is a unum while other is not
           returns a new unum;
           raises DimensionError exception if self and other have incompatible units
       '''
       return Unum.coerceToUnum(other).__sub__(self)

   def __rmul__(self,other):
       ''' overloading of multiplication operator (other * self)
           where self is a unum while other is not
           returns a new unum
       '''          
       return Unum.coerceToUnum(other).__mul__(self)

   def __rdiv__(self,other):
       ''' overloading of division operator (other / self)
           where self is a unum while other is not
           returns a new unum
       '''          
       return Unum.coerceToUnum(other).__div__(self)
   # Python 3.0 compatibility.
   __rtruediv__ = __rdiv__
   __rfloordiv__ = __rdiv__
       
   def __rpow__(self,other):
       ''' overloading of exponentiation operator (other ** self)
           where self is a unum while other is not
           returns a new unum;
           raises DimensionError exception if self has unit
       '''          
       return Unum.coerceToUnum(other).__pow__(self)

   # -- Methods to put any indexable type as unum's value -----------
   
   def __getitem__(self,index):
       ''' returns a Unum having the same unit as self,
           with a value being self's value sliced to index
       '''
       return Unum(self._unit,self._value[index])

   def __setitem__(self,index,value):
       ''' makes a slice assignment on self's value based on index
           from value converted to self's unit
           raises DimensionError exception if self and value have incompatible units
       '''          
       self._value[index] = Unum.coerceToUnum(value).asNumber(Unum(self._unit,1.0))

   def __len__(self):
       ''' returns the length of self's value
       '''
       return len(self._value)

   # -- String representation methods -------------------------------

   def strUnit(self):
       ''' returns a string representing the unum's unit
       '''
       def fmt(exp):
           f = ''
           if exp != 1:
              f = str(exp)
           return f
       num, den = '', ''
       units = list(self._unit.items())       
       if Unum.UNIT_SORTING:
          units.sort()
       for u, exp in units:          
           if exp > 0 or not Unum.UNIT_DIV_SEP:
              if num:
                 num += Unum.UNIT_SEP
              num += u + fmt(exp)
           else:
              if den:
                 den += Unum.UNIT_SEP
              den += u + fmt(-exp)
       if den:
          den = Unum.UNIT_DIV_SEP + den
          if not num:
             num = '1'
       if not num and Unum.UNIT_HIDE_EMPTY:
          res = ''
       else:
          res = Unum.UNIT_FORMAT % (num + den)  
       return res

   def __str__(self):
       ''' overloaded 'str' function;
           returns a string representing the unum's value and unit;
           if AUTO_NORM is set, then self is normalized to an equivalent unum and flagged as such;
           (this side-effect was chosen to avoid unneeded normalizations, the str request is the
            best trigger to normalize the unum)
       '''
       if Unum.AUTO_NORM and not self._normal:
          self.normalize(True)
          self._normal = True  
       return Unum.VALUE_FORMAT % self._value + Unum.UNIT_INDENT + self.strUnit()
          
   def __repr__(self):
       ''' overloaded 'repr' method
           see __str__
       '''
       return str(self)

   def converted(self): 
       ''' returns self converted following _unitTable
           raises UnumError exception if the self's unit is not unique
            or if no conversion exists for self
       '''
       if len(self._unit) != 1:
          raise Unum.UnumError(Unum.ERR_NOCONVERT % (+self).fix())
       u = list(self._unit.keys())[0]
       conv = Unum._unitTable[u][0]
       if conv is None:
          raise Unum.UnumError(Unum.ERR_NOCONVERT % self)    
       return self.replaced(u,conv).fix()

   # == Unum static methods =========================================

   def unit(symbol,conv=0,name=''):
       ''' define a new unum unit represented by the string symbol
           being a base unit                   if conv is 0
                 a derived unit equal to conv  otherwise
           returns this unum                  
       '''
       return Unum({symbol:1},1.0,conv,name)
   unit = staticmethod(unit)
   
   def reset(unitTable=None):
       ''' set the unit table to unitTable       if unitTable defined
                              to an empty table  otherwise
       '''
       if unitTable is None:
          Unum._unitTable = {}
       else:
          Unum._unitTable = unitTable
   reset = staticmethod(reset)

   def getUnitTable():
       ''' returns a copy of the unit table
       '''
       return Unum._unitTable.copy()
   getUnitTable = staticmethod(getUnitTable)

   def coerceToUnum(value):
       ''' returns value                       if value is a unum
                or a unum equivalent to value  otherwise
       '''
       if isinstance(value,Unum):
          res = value
       else:
          res = Unum(Unum._NO_UNIT, value)
       return res
   coerceToUnum = staticmethod(coerceToUnum)

# Maintain API compatibility with Unum 4 and lower.
# "as" became a reserved word in 2.5, so we can't use it.
if sys.version_info < (2,5):
   setattr(Unum, "as", Unum.as_unit)


# == end of Unum class ==============================================

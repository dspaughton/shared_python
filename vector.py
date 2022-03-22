# import sys
# sys.path.append(PATH-TO-THIS-FILE)
# import vector as ...

import math


class Vector:
    """A class to represent a 3-D vector.

    Methods:
    --------
    dot(rhs):
        return the (scalar) dot product with another vector 'rhs'

    X(rhs):
        return the (vector) cross product with another vector 'rhs'

    norm():
        return the vector's 'norm' (aka 'size' or 'magnitude')

    unit():
        return the vector's direction, i.e. the original vector divided by its size

    format(fmt):
        return a user-formatted string representation of the vector
        e.g:
        U = Vector(1,2,3)
        U.format('{:.2f},{:.2f},{:.2f}')  -> '1.00,2.00,3.00'

    Special methods:
    ----------------
    __str__():
        defaults to __repr__

    __repr__():
        return a string representation of the vector
        e.g:
        U = vec.Vector(1,2,3)
        str(U) -> 'Vector(1,2,3)'
        or in the python interpreter:
        U -> 'Vector(1,2,3)'

    Special arithmetic methods:
    ---------------------------
    Vectors may be added and subtracted
        e.g:
        U = vec.Vector(1,2,3)
        V = vec.Vector(4,5,6)
        U+V -> Vector(5,7,9)
        U-V -> Vector(-3,-3,-3)

    Vectors may be multiplied by and divided by scalars
        e.g:
        U = vec.Vector(1,2,3)
        3*U -> Vector(3,6,9)
        U*3 -> Vector(3,6,9)
        U/2 -> Vector(0.5,1.0,1.5)

    LoadObj(filename):
         Returns a list of the vectors found in a wavefront 'obj' file
    """


    def __init__(self,x=0,y=0,z=0):
        """
    Creates a vector.

    Make a vector with components x,y,z from the arguments given.
    The default vector, i.e. V=Vector() makes (0,0,0).
    NB defaults work in order so e.g: V=Vector(1,2) makes (1,2,0)
    """
        self.x=x
        self.y=y
        self.z=z


    def __pos__(self):
        return Vector( self.x,  self.y,  self.z)

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)


    def __mul__(self,s):
        """Return the vector multiplied by a scalar."""
        return Vector(self.x*s, self.y*s, self.z*s)


    def __rmul__(self,s):
        """Return the vector multiplied by a preceding scalar."""
        return Vector(self.x*s, self.y*s, self.z*s)


    def __truediv__(self,s):
        """Return the vector divided by a scalar."""
        return Vector(self.x/s, self.y/s, self.z/s)


    def __add__(self,rhs):
        """Return the sum of two vectors."""
        return Vector(self.x+rhs.x, self.y+rhs.y, self.z+rhs.z)


    def __sub__(self,rhs):
        """Return the difference between two vectors."""
        return Vector(self.x-rhs.x, self.y-rhs.y, self.z-rhs.z)


    def dot(self,rhs):
        """Return the scalar dot product of two vectors.
    e.g:
    U = Vector(1,2,3)
    V = Vector(4,5,6)
    U.dot(V) -> 32
    V.dot(U) -> 32
    """
        return self.x*rhs.x + self.y*rhs.y + self.z*rhs.z


    def X(self,rhs):
        """Return the vector cross product of two vectors.
    e.g:
    U = Vector(1,2,3)
    V = Vector(4,5,6)
    U.X(V) -> Vector(-3,6,-3)
    V.X(U) -> Vector(3,-6,3)
    """
        x = self.y*rhs.z - self.z*rhs.y
        y = self.z*rhs.x - self.x*rhs.z
        z = self.x*rhs.y - self.y*rhs.x
        return Vector(x,y,z)


    def norm(self):
        """Return the vector cross product of two vectors.
    return the vector's 'norm' (aka 'size' or 'magnitude')
    e.g:
    U = Vector(1,2,3)
    U.norm() -> 3.7416573867739413
    """
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)


    def unit(self):
        """Return the vector's direction, i.e. the original vector divided by its size
    e.g:
    U = Vector(1,2,3)
    U.unit()   -> Vector(0.2672612419124244,0.5345224838248488,0.8017837257372732)
    U/U.norm() -> Vector(0.2672612419124244,0.5345224838248488,0.8017837257372732)
    """
        return Vector(self.x,self.y,self.z) * (1/self.norm() )


    def __repr__(self):
        return 'Vector(' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) + ')'


    def format(self,fmt):
        return fmt.format(self.x,self.y,self.z)




def MakeVector(text,sep=''):
    """MakeVector(text,sep='')
    Returns a new vector made from the string (str) argument.

    The string argument should contain three numeric strings.
    The three numeric strings must be separated by exactly 
    two separator strings, made up of any number of spaces,
    commas, and, optionally 'sep'.
    For example all the following make vector(1,2,3):
       V.from_str('1,2,3')
       V.from_str('1 2 3')
       V.from_str('1#2#3', '#')
       V.from_str('1, 2, 3')
       V.from_str('1, , 2, , 3') <- misleading, but works
       V.from_str('1, ,## 2, ##, 3', '#') <- even more misleading, but works
    """
    text = text.strip() # remove leading and trailing white-space
    if len(sep):
        text = text.replace(sep,' ') # change sep to spaces
    text = text.replace(',',' ')     # change commas to spaces

    lentext = -1 # impossible string length means we always loop once
    while lentext != len(text):       # we need to improve
        lentext=len(text)             # but not loop forever ...
        text = text.replace('  ',' ') # we only want single space separators

    Fields = text.split(' ')  # get three numeric strings
    if 3 != len(Fields):
        err = 'Needed exactly THREE numeric strings, not {:d}:'.format(len(Fields))
        for F in Fields:
            err += ' "' + F + '"'
        raise ValueError(err)
    x = float(Fields[0])
    y = float(Fields[1])
    z = float(Fields[2])
    return Vector(x,y,z)








def LoadObj(filename):
    """MakeVector(text,sep='')
    Returns a list of the vectors found in a wavefront 'obj' file
    """
    VectorList = []
    with open(filename) as file:
        for line in file:
            if not line.startswith('v '):
                continue
            line=line[2:]
            x,y,z = line.split()
            VectorList.append(vector( float(x), float(y), float(z) ))
    return VectorList

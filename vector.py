"""
The vector module implements basic 3D vectors.

Class Vector implements 3D vectors.

Function MakeVector(text,sep='') takes text
and returns the vector that it specifies.

Function MakeDir(elevation,azimuth) makes
a new unit vector pointing towards an elevation and azimuth
(see the function documentation for details).

Function LoadObj(filename) returns a list of
the 3D vectors found in a wavefront OBJ file.
"""



# import sys
# sys.path.append(PATH-TO-THIS-FILE)
# import vector as ...

import math


class Vector:
    """A class to represent a 3-D vector.

    Methods:
    --------
    dot(rhs):
        Return the (scalar) dot product with another vector 'rhs'

    X(rhs):
        Return the (vector) cross product with another vector 'rhs'

    norm():
        Return the vector's 'norm' (aka 'size' or 'magnitude')

    unit():
        return a copy of the vector with unit size (i.e. its direction)

    rotated(axis, angle):
        Return a copy of the vector rotated by 'angle' degrees about an
        axis vector (which must be unit).

    rotated_ca(axis, cos, sin):
        As above, but using user-computed cosine and sine of the angle.
        (May be more eficient when rotating lots of vectors).

    format(fmt):
        Return a user-formatted text representation of the vector

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
        """    Unary plus, returns a copy of the Vector."""
        return Vector( self.x,  self.y,  self.z)

    def __neg__(self):
        """    Unary minus, returns a negated copy of the Vector."""
        return Vector(-self.x, -self.y, -self.z)


    def __mul__(self,s):
        """Return the vector post-multiplied by a scalar."""
        return Vector(self.x*s, self.y*s, self.z*s)


    def __rmul__(self,s):
        """Return the vector pre-multiplied by a scalar."""
        return Vector(self.x*s, self.y*s, self.z*s)


    def __truediv__(self,s):
        """Return the vector divided by a scalar."""
        return Vector(self.x/s, self.y/s, self.z/s)


    def __add__(self,rhs):
        """Return the vector sum: self + rhs."""
        return Vector(self.x+rhs.x, self.y+rhs.y, self.z+rhs.z)


    def __sub__(self,rhs):
        """Return the vector difference: self - rhs."""
        return Vector(self.x-rhs.x, self.y-rhs.y, self.z-rhs.z)


    def dot(self,rhs):
        """Return the scalar dot product of self and rhs.
    e.g:
    U = Vector(1,2,3)
    V = Vector(4,5,6)
    U.dot(V) -> 32
    V.dot(U) -> 32
    """
        return self.x*rhs.x + self.y*rhs.y + self.z*rhs.z


    def X(self,rhs):
        """Return the vector cross product between self and rhs.
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
        """Return the vector's 'norm' (aka 'size' or 'magnitude')
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


    def rotated(self, Axis, angle):
        """Return the vector rotated about a unit axis vector.
    cos is the cosine of the rotation angle, sin is its sine.
    """
        a = angle * math.pi / 180
        ca = math.cos(a)
        sa = math.sin(a)
        return self.rotated_ca(Axis, ca, sa)

    def rotated_ca(self, Axis, cos, sin):
        """As above, but using user-computed cosine and sine of the angle.
    """
        size = self.norm()
        # rotating a zero-length vector is trivial
        if 0==size:
            return Vector()
        P = Axis * self.dot(Axis) # Axis-parallel component
        N = self-P                # Axis-normal component
        T = N.X(Axis)             # T is normal to both Axis and N
        # do a 2D rotation with N and T, preserving P
        Rx = N.x*cos - sin*T.x + P.x;
        Ry = N.y*cos - sin*T.y + P.y;
        Rz = N.z*cos - sin*T.z + P.z;
        return Vector(Rx,Ry,Rz)



    def __repr__(self):
        """Return a text representation of the vector."""
        return 'Vector(' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) + ')'


    def format(self,fmt):
        """Return a user-formatted text representation of the vector.
        e.g:
        U = Vector(1,2,3)
        U.format('{:.2f},{:.2f},{:.2f}')  -> '1.00,2.00,3.00'
        """
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


def MakeDir(elevation,azimuth):
    """MakeDirection(elevation,azimuth) (both angles in degrees)
    Returns a new unit vector made from elevation and azimuth,
    (or from the centre of the earth to a latitude and longitude),
    following the convention:
    the x-axis points right  (or  0 North, 90 East)
    the y-axis points up     (or 90 North)
    the z-axis points behind (or 0 North,  0 degrees East)
    """
    elev = elevation * math.pi / 180
    azim = azimuth   * math.pi / 180
    ce = math.cos(elev)
    se = math.sin(elev)
    ca = math.cos(azim)
    sa = math.sin(azim)
    return Vector(ce*sa, se, ce*ca)






def LoadObj(filename):
    """MakeVector(text,sep='')
    Returns a list of the vectors found in a wavefront OBJ file
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

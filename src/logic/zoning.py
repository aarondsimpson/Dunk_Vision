from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Tuple
import math 

ZoneName = Literal[
    "L Corner", "L Short Corner", "L Wing (2)", "L Wing (3)", "L Slot",
    "R Corner", "R Short Corner", "R Wing (2)", "R Wing (3)", "R Slot",
    "Key", "Nail", "L Low Post", "R Low Post", "L High Post", "R High Post",
    "Top of Key", "R Arc (2)", "R Arc (3)", "Left Arc (2)", "Left Arc (3)", 
    "Deep Three", "Center Zone" 
]

@dataclass(frozen=True)
class Rect:
    x0: float; y0: float; x1: float; y1: float 
    def contains(self, nx:float, ny:float) -> bool:
        return self.x0 <= nx <= self.x1 and self.y0 <= ny <= self.y1
    
class _C:
    #HOOP AND 3 POINT ARC
    HOOP_X = 0.50
    HOOP_Y = 0.12
    ARC_RADIUS = 0.28
    ARC_BAND = 0.02
    ARC_INNER = ARC_RADIUS - ARC_BAND
    ARC_OUTER = ARC_RADIUS + ARC_BAND
    ARC_CUTOFF_Y = 0.34
    CORNER_Y = 0.86

    #HORIZONTAL SPLITS
    X_L_CORNER = 0.08
    X_L_WING = 0.34
    X_R_WING = 1 - X_L_WING
    X_R_CORNER = 1 - X_L_CORNER

    #VERTICAL BANDS
    Y_BASE = 0.00
    Y_LOW = 0.20
    Y_MID = 0.34
    Y_TOPOFKEY = 0.46 
    Y_DEEP = 0.66
    Y_CENTER = 0.84
    Y_BOTTOM = 1.00

    #RECTANGULAR ZONES

    L_CORNER = Rect(0.00, Y_BASE, X_L_CORNER, Y_LOW)
    R_CORNER = Rect(X_R_CORNER, Y_BASE, 1.00, Y_LOW)
    L_SHORT_CORNER = Rect(0.00, Y_LOW,X_L_WING, Y_MID)
    R_SHORT_CORNER = Rect(X_R_WING, Y_LOW, 1.00, Y_MID)

    L_WING = Rect(X_L_CORNER, Y_BASE, X_L_WING, Y_LOW)
    R_WING = Rect(X_R_WING, Y_BASE, X_R_CORNER, Y_LOW)

    L_SLOT = Rect(0.00, Y_TOPOFKEY, X_L_WING, Y_DEEP)
    R_SLOT = Rect(X_R_WING, Y_TOPOFKEY, 1.00, Y_DEEP)

    TOP_OF_KEY = Rect(X_L_WING, Y_MID, X_R_WING, Y_TOPOFKEY)

    DEEP_THREE = Rect(0.00, Y_DEEP, 1.00, Y_CENTER)
    CENTER_ZONE = Rect(0.00, Y_CENTER, 1.00, Y_BOTTOM)

    KEY_RECTANGLE = Rect(0.38, Y_LOW - 0.02, 0.62, Y_MID)
    NAIL_RECTANGLE = Rect(0.46, Y_MID - 0.06, 0.54, Y_MID)
    L_LOW_POST = Rect(0.34, Y_LOW, 0.38, Y_MID)
    R_LOW_POST = Rect(0.62, Y_LOW, 0.66, Y_MID)
    L_HIGH_POST = Rect(0.36, Y_MID, 0.40, Y_TOPOFKEY)
    R_HIGH_POST = Rect(0.60, Y_MID, 0.64, Y_TOPOFKEY)

def _in(nx: float, ny: float, r: Rect) -> bool:
    return r.contains(nx,ny)

def _side(nx: float, hoop_x: float) -> Literal["L","R"]:
    return "L" if nx <= hoop_x else "R"

def get_zone(nx: float, ny: float, *, court_type: Literal["half", "full"]="half") -> Tuple[ZoneName, int]:
    #Maps noramlized click (nx,ny) -> zone_name, points_if_made).nx and ny are [0,1] relative to the displayed image
    c = _C
    #posts, key, and nail 
    if _in(nx, ny, c.L_LOW_POST): return "L Low Post", 2 
    if _in(nx, ny, c.R_LOW_POST): return "R Low Post", 2
    if _in(nx, ny, c.L_HIGH_POST): return "L High Post", 2
    if _in(nx, ny, c.R_HIGH_POST): return "R High Post", 2
    if _in(nx, ny, c.KEY_RECTANGLE): return "Key", 2
    if _in(nx, ny, c.NAIL_RECTANGLE): return "Nail", 2
    
    #corners and short corners
    if _in(nx, ny, c.L_CORNER): return "L Corner", 3
    if _in(nx, ny, c.R_CORNER): return "R Corner", 3
    if _in(nx, ny, c.L_SHORT_CORNER): "L Short Corner", 3
    if _in(nx, ny, c.R_SHORT_CORNER): return "R Short Corner", 3

    #distance from hoop center for arc testing
    dx, dy = nx = c.HOOP_X, ny - c.HOOP_Y
    dist = math.hypot(dx,dy)
    side = _side(nx, c.HOOP_X)

    #wings split
   

##ZONES
# L_Corner : 3 Points 
# L_Short_Corner : 2 Points
# L_Low Post_Block : 2 Points
# L_Wing (3) : 3 Points
# L_Wing (2) : 2 Points
# L_High_Post_Elbow
# L_Slot : 3 Points
# L_Arc_2 : 2 Points
# L_Arc_3 : 3 Points
# Nail : 2 Points
# Key : 2 Points
# Top_of_Key : 3 Points
# Deep_Three : 3 Points
# Center : 3 Points
# R_Slot : 3 Points
# R_Arc_2 : 2 Points
# R_Arc_3 : 3 Points
# R_High Post_Elbow
# R_Wing(2) : 2 Points
# R_Wing(3) : 3 Points
# R_Low_Post_Block : 2 Points
# R_Short_Corner : 2 Points
# R_Corner : 3 Points
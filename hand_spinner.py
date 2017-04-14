#!$HOME/anaconda/bin/python
# -*- coding: utf-8 -*-
'''
Ripped from template.py 
- makes an apollonian gasket
'''

import inkex       # Required
import simplestyle # will be needed here for styles support


import numpy as np


__version__ = '0.1'

inkex.localize()


### Your helper functions go here



def draw_SVG_circle(parent, r, cx, cy, name):
    " structre an SVG circle entity under parent "
    circ_attribs = { 'cx': str(cx), 'cy': str(cy), 
                    'r': str(r),
                    inkex.addNS('label','inkscape'): name}
    
    
    circle = inkex.etree.SubElement(parent, inkex.addNS('circle','svg'), circ_attribs )
    
    
class Myextension(inkex.Effect): # choose a better name
    
    def __init__(self):
        " define how the options are mapped from the inx file "
        inkex.Effect.__init__(self) # initialize the super class
        
            
        ## list of parameters defined in the .inx file
        #self.OptionParser.add_option("-d", "--depth",
        #                             action="store", type="int",
        #                             dest="depth", default=3,
        #                             help="command line help")
        
        self.OptionParser.add_option("", "--rr",
                                     action="store", type="float",
                                     dest="rr", default=24.2,
                                     help="command line help")
        
        self.OptionParser.add_option("", "--RR",
                                     action="store", type="float",
                                     dest="RR", default=40,
                                     help="command line help")
        
        
        
        self.OptionParser.add_option("", "--rotate",
                                     action="store", type="inkbool", 
                                     dest="rotate", default=False,
                                     help="command line help")
        
        self.OptionParser.add_option("", "--holes",
                                     action="store", type="string", 
                                     dest="holes", default=False,
                                     help="command line help")
        
        
        # here so we can have tabs - but we do not use it directly - else error
        self.OptionParser.add_option("", "--active-tab",
                                     action="store", type="string",
                                     dest="active_tab", default='title', # use a legitmate default
                                     help="Active tab.")
        
 
           
    def calc_unit_factor(self):
        """ return the scale factor for all dimension conversions.
            - The document units are always irrelevant as
              everything in inkscape is expected to be in 90dpi pixel units
        """
        # namedView = self.document.getroot().find(inkex.addNS('namedview', 'sodipodi'))
        # doc_units = self.getUnittouu(str(1.0) + namedView.get(inkex.addNS('document-units', 'inkscape')))
        unit_factor = self.getUnittouu(str(1.0) + self.options.units)
        return unit_factor


### -------------------------------------------------------------------
### Main function and is called when the extension is run.

    
    def effect(self):

        #set up path styles
        path_stroke = '#DD0000' # take color from tab3
        path_fill   = 'none'     # no fill - just a line
        path_stroke_width  = 1. # can also be in form '0.6mm'
        page_id = self.options.active_tab # sometimes wrong the very first time
        
        style_curve = { 'stroke': path_stroke,
                 'fill': 'none',
                 'stroke-width': path_stroke_width }

        
        # This finds center of current view in inkscape
        sx = sy  = 3.543307
        if self.options.rotate:
            rot = 60
        else:
            rot = 0
        t = [ 'translate(%s,%s)' % (self.view_center[0], self.view_center[1] ),
             'scale(%f,%f)'%(sx,sy),
             'rotate(%d)'%rot
              ]
        
        t = ' '.join(t)
        
        # add a group to the document's current layer
        #all the circles inherit style from this group
        g_attribs = { inkex.addNS('label','inkscape'): 'cirlce_gp' + "_%d"%(166),
                      inkex.addNS('transform-center-x','inkscape'): str(0),
                      inkex.addNS('transform-center-y','inkscape'): str(0),
                      'transform': t,
                      'style' : simplestyle.formatStyle(style_curve),
                      'info':'N: '}
        topgroup = inkex.etree.SubElement(self.current_layer, 'g', g_attribs )
        
        
        #set up parameters for placing the holes
        CX, CY = 0,0
        distance2center, off  = self.options.RR, np.pi/6
        #the -1  is a hack - otherwise it is out by a couple of px
        hole_radius= .5*(self.options.rr - 1)

        #the 3 outer holes
        if self.options.holes in ['all','no_center']:
            angles = [ 2*np.pi/3*k + off for k in range(3)]
            for aa in angles:
                r,cx, cy =  hole_radius,CX + distance2center*np.cos(aa), CY + distance2center*np.sin(aa)
                draw_SVG_circle(topgroup,r,cx,cy,'apo')
        
        #the central hole
        if self.options.holes in ['all','center']:
            draw_SVG_circle(topgroup,hole_radius,CX,CY,'apo')   
        


if __name__ == '__main__':
    e = Myextension()
    e.affect()



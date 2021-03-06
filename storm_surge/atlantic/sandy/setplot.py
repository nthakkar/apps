
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
"""

import os

import numpy as np
import matplotlib

import matplotlib.pyplot as plt

from geoclaw import topotools
from clawpack.visclaw import colormaps, geoplot, gaugetools
from clawpack.clawutil.oldclawdata import Data

import geoclaw.surge as surge

try:
    from setplotfg import setplotfg
except:
    setplotfg = None


def setplot(plotdata):
    r"""Setplot function for surge plotting"""
    

    plotdata.clearfigures()  # clear any old figures,axes,items data

    # Load data from output
    amrdata = Data(os.path.join(plotdata.outdir,'amr2ez.data'))
    physics = Data(os.path.join(plotdata.outdir,'physics.data'))
    surge_data = Data(os.path.join(plotdata.outdir,'surge.data'))

    # Load storm track
    track = surge.plot.track_data(os.path.join(plotdata.outdir,'fort.track'))
    surge_afteraxes = lambda cd: surge.plot.surge_afteraxes(cd,track)

    # Limits for plots
    full_xlimits = [-92.0,-45.0]
    full_ylimits = [13.0,41.0]

    # Color limits
    surface_range = 1.0
    speed_range = 2.0

    xlimits = full_xlimits
    ylimits = full_ylimits
    eta = physics.eta_init
    if not isinstance(eta,list):
        eta = [eta]
    surface_limits = [eta[0]-surface_range,eta[0]+surface_range]
    speed_limits = [0.0,speed_range]
    
    wind_limits = [0,55]
    pressure_limits = [966,1013]
    vorticity_limits = [-1.e-2,1.e-2]

    def pcolor_afteraxes(current_data):
        surge_afteraxes(current_data)
        surge.plot.gauge_locations(current_data)
    
    def contour_afteraxes(current_data):
        surge_afteraxes(current_data)

    
    # ==========================================================================
    # ==========================================================================
    #   Plot specifications
    # ==========================================================================
    # ==========================================================================

    # ========================================================================
    #  Surface Elevations - Entire Atlantic
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Surface - Atlantic', figno=0)
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    plotaxes.afteraxes = pcolor_afteraxes
    
    surge.plot.add_surface_elevation(plotaxes,bounds=surface_limits)
    surge.plot.add_land(plotaxes)


    # ========================================================================
    #  Water Speed - Entire Atlantic
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Currents - Atlantic', figno=1)
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Currents'
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    plotaxes.afteraxes = pcolor_afteraxes

    # Speed
    surge.plot.add_speed(plotaxes,bounds=speed_limits)

    # Land
    surge.plot.add_land(plotaxes)


    # ========================================================================
    # Hurricane forcing - Entire Atlantic
    # ========================================================================
    # Pressure field
    plotfigure = plotdata.new_plotfigure(name='Pressure', figno=2)
    plotfigure.show = surge_data.pressure_forcing
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = full_xlimits
    plotaxes.ylimits = full_ylimits
    plotaxes.title = "Pressure Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    
    surge.plot.add_pressure(plotaxes,bounds=pressure_limits)
    # surge.plot.add_pressure(plotaxes)
    surge.plot.add_land(plotaxes)
    
    # Wind field
    plotfigure = plotdata.new_plotfigure(name='Wind Speed',figno=3)
    plotfigure.show = surge_data.wind_forcing
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = full_xlimits
    plotaxes.ylimits = full_ylimits
    plotaxes.title = "Wind Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    
    surge.plot.add_wind(plotaxes,bounds=wind_limits,plot_type='imshow')
    # surge.plot.add_wind(plotaxes,bounds=wind_limits,plot_type='contour')
    # surge.plot.add_wind(plotaxes,bounds=wind_limits,plot_type='quiver')
    surge.plot.add_land(plotaxes)
    
    # Wind field components
    plotfigure = plotdata.new_plotfigure(name='Wind Components',figno=4)
    plotfigure.show = surge_data.wind_forcing
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = "subplot(121)"
    plotaxes.xlimits = full_xlimits
    plotaxes.ylimits = full_ylimits
    plotaxes.title = "X-Component of Wind Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True

    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = surge.plot.wind_x
    plotitem.imshow_cmap = colormaps.make_colormap({1.0:'r',0.5:'w',0.0:'b'})
    plotitem.imshow_cmin = -wind_limits[1]
    plotitem.imshow_cmax = wind_limits[1]
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1,1,1]
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = "subplot(122)"
    plotaxes.xlimits = full_xlimits
    plotaxes.ylimits = full_ylimits
    plotaxes.title = "Y-Component of Wind Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True

    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = surge.plot.wind_y
    plotitem.imshow_cmap = colormaps.make_colormap({1.0:'r',0.5:'w',0.0:'b'})
    plotitem.imshow_cmin = -wind_limits[1]
    plotitem.imshow_cmax = wind_limits[1]
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1,1,1]

    # ========================================================================
    #  Figures for gauges
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Surface & topo', figno=300, \
                    type='each_gauge')
    plotfigure.show = True
    plotfigure.clf_each_gauge = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    try:
        plotaxes.xlimits = [amrdata.t0,amrdata.tfinal]
    except:
        pass
    plotaxes.ylimits = surface_limits
    plotaxes.title = 'Surface'
    plotaxes.afteraxes = surge.plot.gauge_afteraxes

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 3
    plotitem.plotstyle = 'r-'


    #-----------------------------------------
    
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_gaugenos = 'all'          # list of gauges to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata


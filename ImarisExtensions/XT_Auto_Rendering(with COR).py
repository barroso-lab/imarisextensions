# Rendering
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 18:09:06 2024

@author: orukod
"""

# Description
# This XTension will find the surface contact area between 2 surfaces. The
# primary surface is the base, and secondary is one covering the primary.

# The result of the XTension will generate a one voxel thick unsmoothed
# surface object above the primary surface representing where the 2 surfaces
# physically overlap.

# Two new statistics will be generated.  1)The first will be a total surface
# area of each new surface object. The measurement will be estimated by
# taking the number of voxels and multiplying by the area a a single (XY
# pixel).  2) The second statistic will be in the "overall" tab, reporting
# the percentage of surface contact area relative to the total surface area
# of the primary surfaces.

# Python libraries - no special libraries are required for this XTension
# See list below for standard libraries being used

import ImarisLib
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

def XT_Auto_Rendering(imaris_id):
    try:
        # Initialize ImarisLib
        vImarisLib = ImarisLib.ImarisLib()
        vImarisApplication = vImarisLib.GetApplication(imaris_id)
        vFactory = vImarisApplication.GetFactory()
        vSurpassScene = vImarisApplication.GetSurpassScene()
        vImageProcessing = vImarisApplication.GetImageProcessing()



        

        # Get the current dataset
        vImage = vImarisApplication.GetDataSet()

        # Check if dataset is loaded
        if vImage is None:
            print("No dataset loaded.")
            return

        # Get the number of channels
        num_channels = vImage.GetSizeC()

        # Prompt the user to enter the nucleus channel index
        nucleus_channel_index = input("Please enter the nucleus channel indices: ")
        # Convert input string into a list of integers
        nucleus_channel_index_list = [int(i) for i in nucleus_channel_index.split(',')]
        print(nucleus_channel_index_list)
               
        # Prompt the user to enter the nucleus channel index
        first_channel_index = int(input("Enter the first channel index: "))
        # Prompt the user to enter the nucleus channel index
        last_channel_index = int(input("Enter the last channel index: "))

        # Iterate through each channel and create surfaces
        for channel_index in range(num_channels):

        # Parameters for surface detection
            intensity_threshold_manual = 0.1  # Reduced threshold value
            
            surface_filter_string = ''  # No filter by default

            # Calculate the largest object radius from the diameter
            if channel_index + 1 not in nucleus_channel_index_list:
                largest_object_radius = 0.265  # Reduced radius
                smooth_filter = 0.007  # Reduced smoothing
            else:
                largest_object_radius = 20  # Reduced radius
                smooth_filter = 0.00600  # Reduced smoothing

            if channel_index < last_channel_index + 1 and channel_index + 1 >= first_channel_index:
                # Detect surfaces for the current channel
                vSurfaces = vImageProcessing.DetectSurfaces(
                    vImage,                      # Dataset
                    None,                        # Context (None in this case)
                    channel_index,               # Channel index
                    smooth_filter,               # Reduced smoothing filter
                    largest_object_radius,       # Reduced local contrast filter width
                    True,                        # Automatic intensity threshold
                    intensity_threshold_manual,  # Reduced manual intensity threshold
                    surface_filter_string        # Surface filters
                )

                # Set the name for the surfaces object
                vSurfaces.SetName(f"Surface from Channel {channel_index + 1}")

                # Set the color of the surfaces to match the channel color
                colorRGBA = vImage.GetChannelColorRGBA(channel_index)
                vSurfaces.SetColorRGBA(colorRGBA)

                # Add surfaces to the Surpass scene
                vSurpassScene.AddChild(vSurfaces, -1)

                print(f"Surfaces for channel {channel_index + 1} created and added to Surpass scene.")
                print(f"New channel for masked data from channel {channel_index + 1} created.")



        # Create a reference frame centered on the surface
        
        global NamesSurfaces, NamesSpots, NamesFilaments

        
        NamesSurfaces = []
        NamesSpots = []
        NamesFilaments = []
        NamesFilamentsIndex = []
        NamesSurfacesIndex = []
        NamesSpotsIndex = []
        NamesReferenceFrames = []
        NamesReferenceFramesIndex = []

        vSurpassSurfaces = 0
        vSurpassSpots = 0
        vSurpassFilaments = 0
        vSurpassReferenceFrame = 0
        
        vNumberSurpassItems = vImarisApplication.GetSurpassScene().GetNumberOfChildren()


        for vChildIndex in range(0, vNumberSurpassItems):
            vDataItem = vSurpassScene.GetChild(vChildIndex)
            IsSurface = vImarisApplication.GetFactory().IsSurfaces(vDataItem)
            print(IsSurface)
            IsSpot = vImarisApplication.GetFactory().IsSpots(vDataItem)
            IsFilament = vImarisApplication.GetFactory().IsFilaments(vDataItem)
            IsReferenceFrame = vImarisApplication.GetFactory().IsReferenceFrames(vDataItem)
            if IsSurface:
                vSurpassSurfaces += 1
                NamesSurfaces.append(vDataItem.GetName())
                NamesSurfacesIndex.append(vChildIndex)
            elif IsSpot:
                vSurpassSpots += 1
                NamesSpots.append(vDataItem.GetName())
                NamesSpotsIndex.append(vChildIndex)
            elif IsFilament:
                vSurpassFilaments += 1
                NamesFilaments.append(vDataItem.GetName())
                NamesFilamentsIndex.append(vChildIndex)
            elif IsReferenceFrame:
                vSurpassReferenceFrame += 1
                NamesReferenceFrames.append(vDataItem.GetName())
                NamesReferenceFramesIndex.append(vChildIndex)
               
        vSurfaceCenter = vSurfaces.GetCenterOfMass(4)
                
        try:

            def SelectSurface():
                global selectedSurface
                selectedSurface = surfaceSelection.get()
                surfaceSelectBox.destroy()


            surfaceSelectBox = Tk()
            surfaceSelectBox.title("Select Surface")
            surfaceSelectBox.geometry("300x200")

            surfaceSelection = StringVar(surfaceSelectBox)
            surfaceSelection.set(NamesSurfaces[0])  # default value

            print(NamesSurfaces)

            Label(surfaceSelectBox, text="Select Surface:").pack()
            surfaceMenu = OptionMenu(surfaceSelectBox, surfaceSelection, *NamesSurfaces)
            surfaceMenu.pack()

            Button(surfaceSelectBox, text="OK", command=SelectSurface).pack()
            surfaceSelectBox.mainloop()

            selectedSurfaceIndex = NamesSurfaces.index(selectedSurface)
            vSurface = vFactory.ToSurfaces(vImarisApplication.GetSurpassScene().GetChild(NamesSurfacesIndex[selectedSurfaceIndex]))

            timeindex = vSurface.GetTimeIndex(selectedSurfaceIndex)
            vSurfaceCenter = vSurfaces.GetCenterOfMass(selectedSurfaceIndex)
        

            vReferenceFrame = vFactory.CreateReferenceFrames()
            vReferenceFrame.SetName(f"Reference Frame for Surface from Channel {channel_index + 1}")
            print(vSurfaceCenter)
                    
            vReferenceFrame.SetKeyFramesPositionsXYZT([1],vSurfaceCenter)
            print('i am here')
            vSurpassScene.AddChild(vReferenceFrame, -1)
        except Exception as e:  # Catching all exceptions and printing them
            print("An error occurred:", e)
            breakpoint()
        print(f"Reference frame for channel {channel_index + 1} created and added to Surpass scene.")
        
        
    except Exception as e:  # Catching all exceptions and printing them
        print("An error occurred:", e)
        breakpoint()

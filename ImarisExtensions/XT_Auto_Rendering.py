# Rendering
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 18:09:06 2024

@author: orukod
"""
# <CustomTools>
#     <Menu>
#         <Submenu name="Rendering">
#             <Item name="Auto Rendering" icon="Python3">
#                 <Command>Python3XT::XT_Auto_Rendering(%i)</Command>
#             </Item>
#         </Submenu>
#     </Menu>
#     <SurpassTab>
#         <SurpassComponent name="bpSurfaces">
#             <Item name="Auto Rendering" icon="Python3">
#                 <Command>Python3XT::XT_Auto_Rendering(%i)</Command>
#             </Item>
#         </SurpassComponent>
#     </SurpassTab>
# </CustomTools>

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


        # Prompt the user to enter the base naming structure
        base_naming_structure = input("Enter the base naming structure: ")


        # Prompt the user to enter the cell numbers being rendered
        first_cell_number = int(input("Enter the first cell's cell number: "))
        # Prompt the user to enter the nucleus channel index
        last_cell_number = int(input("Enter the last cell's cell number: "))
        #Current Cell Number Holder
        current_cell_number = first_cell_number
        



        # Prompt the user to enter the channels being rendered apart from the nucleus
        channel_names = input("Please enter the channels being rendered(enter a comma between channels):")
        # Convert input string into a list of integers
        channel_names_list = [i.strip() for i in channel_names.split(',')]
        print(channel_names_list)
        #Channel Index Holder
        current_channel_index = 0

        

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
            intensity_threshold_manual = 300  # Reduced threshold value
            
            surface_filter_string = ''  # No filter by default

            # Calculate the largest object radius from the diameter
            if channel_index + 1 not in nucleus_channel_index_list:
                largest_object_radius = 0.265  # Reduced radius
                smooth_filter = 0.08000  # Reduced smoothing
            else:
                largest_object_radius = 200  # Reduced radius
                smooth_filter = 0.0600  # Reduced smoothing
            smallest_object_radius = 0.1
            if channel_index < last_channel_index + 1 and channel_index + 1 >= first_channel_index:
                # Detect surfaces for the current channel
                vSurfaces = vImageProcessing.DetectSurfaces(
                    vImage,                      # Dataset
                    None,                        # Context (None in this case)
                    channel_index,               # Channel index
                    smooth_filter,               # Reduced smoothing filter
                    largest_object_radius,       # Reduced local contrast filter width
                    True,                       # Automatic intensity threshold
                    intensity_threshold_manual,  # Reduced manual intensity threshold
                    surface_filter_string        # Surface filters
                )
                
                
                # Apply size filtering: iterate through surfaces and remove small ones
             #   surface_areas = vSurfaces.GetStatisticsByName('Volume')  # Get areas of detected surfaces
             #   print(surface_areas)
             #   valid_surface_indices = [
             #       i for i, area in enumerate(surface_areas.mValues) if area >= 200
              #  ]
                
                # Remove surfaces below the threshold
            #    min_surface_area =20000 # Adjust this value as needed
             #   i = 0
             #   for surface_area in surface_areas.mValues:
                    
                 #   
                 #   if surface_area <= min_surface_area:
                    #    try:
                            
                       #     vSurfaces.RemoveSurface(i-1)
                       #     print(i-1)
                   #     except:
                  #          pass

                   # i += 1

                # Set the name for the surfaces object
                try:
                    vSurfaces.SetName(f"{base_naming_structure} Cell {current_cell_number} {channel_names_list[current_channel_index]}")
                except:
                    current_channel_index =  0
                    
                    vSurfaces.SetName(f"{base_naming_structure} Cell {current_cell_number} {channel_names_list[current_channel_index]}")
                    
            #    vSurfaces.SetStatisticsAndMeasurements(True)

                # Set the color of the surfaces to match the channel color
                colorRGBA = vImage.GetChannelColorRGBA(channel_index)
                vSurfaces.SetColorRGBA(colorRGBA)

                # Add surfaces to the Surpass scene
                vSurpassScene.AddChild(vSurfaces, -1)

                print(f"{base_naming_structure} Cell {current_cell_number} {channel_names_list[current_channel_index]}")
                print(f"New channel for masked data from channel {channel_index + 1} created.")

                current_channel_index =  current_channel_index + 1

                if channel_index + 1 in nucleus_channel_index_list:
                    current_cell_number = current_cell_number + 1

        #Create Center of Reference Frames
        XT_MJG_ReferenceFrame6(imaris_id)
        
    except Exception as e:  # Catching all exceptions and printing them
        print("An error occurred:", e)
        breakpoint()




def XT_MJG_ReferenceFrame6(aImarisId):
    try:
        # Create an ImarisLib object
        vImarisLib = ImarisLib.ImarisLib()
        # Get an imaris object with id aImarisId
        vImarisApplication = vImarisLib.GetApplication(aImarisId)
        # Get the factory
        vFactory = vImarisApplication.GetFactory()
        # Get the currently loaded dataset
        vImage = vImarisApplication.GetDataSet()
        # Get the Surpass scene
        vSurpassScene = vImarisApplication.GetSurpassScene()

        # Get image properties
        vExtendMin = (vImage.GetExtendMinX(), vImage.GetExtendMinY(), vImage.GetExtendMinZ())
        vExtendMax = (vImage.GetExtendMaxX(), vImage.GetExtendMaxY(), vImage.GetExtendMaxZ())
        vImageSize = (vImage.GetSizeX(), vImage.GetSizeY(), vImage.GetSizeZ())
        vSizeT = vImage.GetSizeT()
        vSizeC = vImage.GetSizeC()
        Xvoxelspacing = (vExtendMax[0] - vExtendMin[0]) / vImageSize[0]
        Yvoxelspacing = (vExtendMax[1] - vExtendMin[1]) / vImageSize[1]
        Zvoxelspacing = round((vExtendMax[2] - vExtendMin[2]) / vImageSize[2], 3)

        vMidX = round((vExtendMax[0] - vExtendMin[0]) / 2, 2)
        vMidY = round((vExtendMax[1] - vExtendMin[1]) / 2, 2)
        vMidZ = round((vExtendMax[2] - vExtendMin[2]) / 2, 2)

        vCurrentVisibleTimeIndex = vImarisApplication.GetVisibleIndexT()

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

       

      
        main = tk.Tk()
        main.title("Select Surfaces")
        main.geometry("300x200")
        main.attributes("-topmost", True)

        names = StringVar()
        names.set(NamesSurfaces)
        lstbox = Listbox(main, listvariable=names, selectmode=MULTIPLE, width=20, height=10)
        lstbox.grid(column=0, row=0, columnspan=2)

        def select():
            global ObjectSelection
            ObjectSelection = list()
            selection = lstbox.curselection()
            for i in selection:
                entrada = lstbox.get(i)
                ObjectSelection.append(i)
            if not ObjectSelection:
                messagebox.showerror(title='Surface menu', message='Please choose at least one surface')
                main.mainloop()
            else:
                main.destroy()

        btn = ttk.Button(main, text="Choose Surfaces", command=select)
        btn.grid(column=1, row=1)
        lstbox.selection_set(0)
        main.mainloop()
        selectedSurfaces = [NamesSurfaces[i] for i in ObjectSelection]
        
        
        selectedSurfacesIndex = [NamesSurfacesIndex[i] for i in ObjectSelection]


        
        for selectedSurfaceIndex in selectedSurfacesIndex:
            
            vSurface = vFactory.ToSurfaces(vSurpassScene.GetChild(selectedSurfaceIndex))
            
            #vSurfaceIndexT = vSurface.GetIndexT()
            vSurfacePosXYZ = vSurface.GetCenterOfMass(0)
            vSurfacePosXYZT = (vSurfacePosXYZ, 1)
         
            qCurrentReferenceFrame = vFactory.CreateReferenceFrames()

            qCurrentReferenceFrame.SetKeyFramesPositionsXYZT([0], [[vSurfacePosXYZ[0][0], vSurfacePosXYZ[0][1], vSurfacePosXYZ[0][2]]])
            vSurpassScene.AddChild(qCurrentReferenceFrame, -1)
           # else:
            #    qCurrentReferenceFrame = vSurpassScene.GetChild(NamesReferenceFramesIndex[0])
            #qCurrentReferenceFrame.SetPositionsXYZT([vSurfaceIndexT], [[vSurfacePosXYZ[0], vSurfacePosXYZ[1], vSurfacePosXYZ[2]]])
    
    except Exception as e:
        print("An error occurred: ", e)
        breakpoint()


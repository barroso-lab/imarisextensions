# Rendering
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 18:09:06 2024

@author: orukod
"""
# <CustomTools>
#     <Menu>
#         <Submenu name="Rendering">
#             <Item name="Reference Frame" icon="Python3">
#                 <Command>Python3XT::XT_MJG_ReferenceFrame6(%i)</Command>
#             </Item>
#         </Submenu>
#     </Menu>
#     <SurpassTab>
#         <SurpassComponent name="bpSurfaces">
#             <Item name="Reference Frame" icon="Python3">
#                 <Command>Python3XT::XT_MJG_ReferenceFrame6(%i)</Command>
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
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import ImarisLib

aImarisId = 0

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

        # Delete all pre-existing reference frames
        for vChildIndex in range(vNumberSurpassItems - 1, -1, -1):  # Reverse iteration to safely remove items
            vDataItem = vSurpassScene.GetChild(vChildIndex)
            if vImarisApplication.GetFactory().IsReferenceFrames(vDataItem):
                vSurpassScene.RemoveChild(vDataItem)

        
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


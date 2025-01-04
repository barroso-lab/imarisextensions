# Surface Surface Contact Area

# Written by Matthew J. Gastinger
# Spet 2020 - Imaris 9.6.0

    # <CustomTools>
    #     <Menu>
    #         <Submenu name="Surfaces Functions">
    #             <Item name="Export" icon="Python3">
    #                 <Command>Python3XT::XT_Export(%i)</Command>
    #             </Item>
    #         </Submenu>
    #     </Menu>
    #     <SurpassTab>
    #         <SurpassComponent name="bpSurfaces">
    #             <Item name="Export" icon="Python3">
    #                 <Command>Python3XT::XT_Export(%i)</Command>
    #             </Item>
    #         </SurpassComponent>
    #     </SurpassTab>
    # </CustomTools>

# Description
# This XTension will find the surface contact area between 2 surfaces.  The
# primary surface is the base, and secondary is one covering the primary.

# The result of the XTension will generate a one voxel thick unsmoothed
# surface object above the primary surface representing where the 2 surfaces
# physically overlap.

# Two new statistics will be generated.  1)The first will be a total surface
# area of each new surface object.  The measurement will be estimate by
# taking the number of voxels and multiplying by the area a a single (XY
# pixel).  2) The second statistic will be in the "overall" tab, reporting
# the percentage of surface contact area relative to the total surface area
# of the primary surfaces.

#Python libraries - no special libraries are required for this XTension
#See list below for standard libraries being used


import ImarisLib
import csv

#
# Python Imaris Library to initiate communication with Imaris via ImarisXT
#
# Copyright by Bitplane AG
#


   
    
def XT_Export(imaris_id):
     
    try:
        # Initialize ImarisLib
        vImarisLib = ImarisLib.ImarisLib()
        vImarisApplication = vImarisLib.GetApplication(imaris_id)
        vFactory = vImarisApplication.GetFactory()
        vSurpassScene = vImarisApplication.GetSurpassScene()
      
        # Ensure that a dataset is loaded
        vImage = vImarisApplication.GetDataSet()
        if vImage is None:
            print("No dataset loaded.")
            return
        
        # Iterate through the Surpass scene and export data
        for i in range(vSurpassScene.GetNumberOfChildren()):
            
            vChild = vSurpassScene.GetChild(i)
            if vFactory.IsSurfaces(vChild):
                vSurfaces = vFactory.ToSurfaces(vChild)
                # Extract data from surfaces
                
                surface_data = extract_surface_data(vSurfaces)
                # Save data to CSV
                
                print("No dataset loaded.")
                save_to_csv(surface_data, f"{vSurfaces.GetName()}_data.csv")
        
        
    except Exception as e:
        print("An error occurred during data export:", e)
        

def extract_surface_data(vSurfaces):
    num_surfaces = vSurfaces.GetNumberOfSurfaces()
    surface_data = []
    for i in range(num_surfaces):
        surface_area = vSurfaces.GetStatisticsByName('Surface Area')[0][i]
        surface_data.append([i + 1, surface_area])
    return surface_data

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Surface ID", "Surface Area"])
        writer.writerows(data)
        
XT_Export(0)
breakpoint()
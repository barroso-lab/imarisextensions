# Rendering
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 18:09:06 2024

@author: orukod
"""
# <CustomTools>
#     <Menu>
#         <Submenu name="Rendering">
#             <Item name="Auto Export" icon="Python3">
#                 <Command>Python3XT::XT_Auto_Rendering(%i)</Command>
#             </Item>
#         </Submenu>
#     </Menu>
#     <SurpassTab>
#         <SurpassComponent name="bpSurfaces">
#             <Item name="Auto Export" icon="Python3">
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

try:
    import ImarisLib
    import tkinter as tk
    from tkinter import ttk, messagebox
    import csv



    def XT_Auto_Rendering(imaris_id):
        try:
            # Initialize ImarisLib
            vImarisLib = ImarisLib.ImarisLib()
            vImarisApplication = vImarisLib.GetApplication(imaris_id)
            vFactory = vImarisApplication.GetFactory()
            vSurpassScene = vImarisApplication.GetSurpassScene()

            # Check if a Surpass scene is loaded
            if vSurpassScene is None:
                print("No Surpass scene loaded.")
                return

            # Gather all surfaces in the Surpass scene
            surface_names = []
            surface_objects = []
            num_children = vSurpassScene.GetNumberOfChildren()
            for i in range(num_children):
                child = vSurpassScene.GetChild(i)
                if vFactory.IsSurfaces(child):
                    surface_names.append(child.GetName())
                    surface_objects.append(child)

            if not surface_names:
                print("No surfaces found in the Surpass scene.")
                return

            # Function to export selected surface statistics to CSV
            def export_statistics(vSurface,vNucleusSurface):
    
                # Retrieve statistics
                surface_name = vSurface.GetName()
                vStatisticValues = vSurface.GetStatistics()
                
                # Prepare a dictionary to hold statistic names and their corresponding values
                statistics_dict = {}

                # Fill the dictionary with statistics
                for i in range(len(vStatisticValues.mNames)):
                    statistic_name = vStatisticValues.mNames[i]
                    statistic_value = vStatisticValues.mValues[i]

                    # Append the value to the list of the corresponding statistic name
                    if statistic_name not in statistics_dict:
                        statistics_dict[statistic_name] = []
                    statistics_dict[statistic_name].append(statistic_value)


                vNucleusStatisticValues = vNucleusSurface.GetStatistics()
                 # Fill the dictionary with statistics
                for i in range(len(vNucleusStatisticValues.mNames)):
                    nucleus_statistic_name = vNucleusStatisticValues.mNames[i]
                    nucleus_statistic_value = vNucleusStatisticValues.mValues[i]
 
                    # Append the value to the list of the corresponding statistic name
                    if nucleus_statistic_name == "Shortest Distance to Surfaces" :                        
                        if "Shortest Distance to Surfaces(Nucleus)" not in statistics_dict:
                            statistics_dict["Shortest Distance to Surfaces(Nucleus)"] = []
                        statistics_dict["Shortest Distance to Surfaces(Nucleus)"].append(nucleus_statistic_value)



                # Determine the maximum number of entries for any statistic
                max_entries = max(len(values) for values in statistics_dict.values())

                # Ensure all lists have the same length by padding with empty strings
                for key in statistics_dict:
                    statistics_dict[key].extend([''] * (max_entries - len(statistics_dict[key])))

                # Prepare data for export
                headers = list(statistics_dict.keys())
                rows = zip(*statistics_dict.values())

                # Export to CSV
                csv_filename = f"Y:/Research/CCS/Barroso/Dancan/{surface_name}_Statistics.csv"
                with open(csv_filename, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)  # Write the header row
                    writer.writerows(rows)    # Write the data rows

            

                print(f"Statistics exported to {csv_filename}")

            # GUI for selecting a surface
            
            # GUI for selecting surfaces (both primary and nucleus)
            def select_surface():
                selected_indices = lstbox.curselection()
                
                selected_indices_nucleus = lstbox.curselection()
                
                if len(selected_indices) >= 2:
             
                    
                    for index in selected_indices:
                        print(index-1)
                        print(surface_objects)
                        surface = surface_objects[index]
                        if "Nucleus" in surface.GetName():
                            print(surface.GetName())
                            nucleus_surface =  surface
                        else:
                            print(surface.GetName())
                            primary_surface =  surface
                            
                  
                    # Proceed with export for primary surface
                    export_statistics(primary_surface,nucleus_surface)
            
                 
                    print("Both primary and nucleus surfaces selected and processed.")
                    main.destroy()  # Close the GUI
                    
                elif len(selected_indices) == 1:
                    messagebox.showwarning("Selection Error", "Please select two surfaces (Primary and Nucleus).")
                else:
                    messagebox.showwarning("Selection Error", "Please select two surfaces (Primary and Nucleus).")

    

            main = tk.Tk()
            main.title("Select a Surface")
            main.geometry("500x500")
            main.attributes("-topmost", True)

            lstbox = tk.Listbox(main, selectmode=tk.MULTIPLE)
            for name in surface_names:
                lstbox.insert(tk.END, name)
            lstbox.pack(padx=10, pady=10)

            btn = ttk.Button(main, text="Export Statistics", command=select_surface)
            btn.pack(pady=10)
            
            
            

            main.mainloop()

        except Exception as e:
            print("An error occurred:", e)
            breakpoint()
        breakpoint()    


except Exception as e:
    print(e)
    breakpoint()



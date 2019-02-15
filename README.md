# BlenderXamlExporter
A XAML Exporter for Blender

The Blender export script was created to make it easy to get 3D models into the XAML format for use in WPF applications. The limitations is that only certain Blender items can be exported such as 3D Models, Materials, Textures and Lamps.
The script has been tested with Blender version 2.71 and 2.79 installed on Windows. It may work on other versions but has not yet been tested.

INSTALL

You can use the Blender user preferences window to import the script into blender.
The “io_export_xaml.py” script needs to be placed in the “C:\Program Files\Blender Foundation\Blender\2.79\scripts\addons” directory, depending on your install location and Blender version.

ENABLE

To enable the script:
Open Blender.
From the “File” menu select “User Preferences”.
From the User Preferences dialog select the Add-ons tab.
Filter the list by selecting the Import-Export Category.
Scroll to the bottom of the list and check the Import-Export: XAML format (.xaml) list item.
Save User Settings.

EXPORT

Once installed and enabled it should be available in the “File >> Export” list.

EXPORT OPTIONS

These options maybe available from the “Export to XAML” pane.
Namesace
The namespace to use with the Window and code behind. The class name will be the same as the file name.
Container
The Window or Resource Dictionary.
Panel
The layout panel to be used when using a Window.
Viewport
You can use the standard WPF Viewport3D or the Helix Toolkit Viewport3D. The Helix Toolkit Viewport requires your project to reference Helix Toolkit (Available via nuget)
Convert to Y-up
Blender uses a Z-up coordinate system while XAML typically uses Y-up.
XAML Camera
A default XAML Camera or the camera defined by Blender. If no camera in scene the default XAML camera will be added.
XAML Lights
Use the default XAML Lights or the ones defined by Blender.

SUPPORT

None.

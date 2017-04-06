--Blender .gbxmodel importer v0.6.0--

By Fulsam, based off code by Adam Papamarcos (TheGhost)

--INSTRUCTIONS--

The importer is a standard blender addon that can be installed via the following:

1. Download and unzip the .py file anywhere.
2. Open up blender, and go to File > User Preferences
3. Go to Addons.
4. At the bottom of the user preferences window, hit the button that says "Install from file"
5. Navigate to where you put the .py file.
6. Scroll up, and where it says "Import-Export: Gbxmodel Importer", and hit the checkbox all the way to the right, enabling the addon.
7. Click "Save user settings" if you want the addon to be active every time you start blender.

--CHANGELOG--

v0.4.0:

-First release, only for demonstration purposes.
-File browser added for improved ease-of-use.

v0.5.0

-First release as a blender addon, rather than a script.
-GUI added
-Options added to disable/enable node importing, model importing, and UVW importing.
-User adjustable node size added.

v0.5.1

-Revised addon credits to include Adam Papamarcos, who is responsible for the original maxscript that this is a port of.

v0.6.0

-Fixed user being able to set node/marker size to negative values.
-Fixed tilde (~) being out of range of the string reading function.
-Added marker importing functionality.
-Added color selection for markers and nodes.
-Added region/permutation selection.
-Added LOD selection.
-Added text field showing the name of the currently loaded model.
-UI elements now grey out when their corresponding importing option is disabled.


--KNOWN BUGS--

-The tools bar is a bit too small to display the full text of many options. This can be fixed easily by dragging the bar to resize it,
but might want to look into moving the importer to another portion of the UI.
-RegionList property stays after unloading the addon. Can be fixed by a simple blender restart.
-Certain models -MIGHT- throw an error upon importing markers. 

--CONTACT--

Email: mrfulsy@gmail.com
Facepunch and Halomaps username: Fulsam
REPORT BUGS OR I CAN'T FIX THEM.



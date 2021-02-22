# CNC-Export
This API is used to output the intermeditate CNC files for the Fusion CAM toolpaths, this API serves two functionalitis one is it creates a .dmp files which has all the toolpath information and other one is to create a cnc file for debugging the post in vs code

**DUMPER**
The dumper file is an intermediate CNC file and output a file that contains all of the information passed from HSM to the post processor. The output file has a file extension of .dmp. The contents of the dump file will show the settings of all parameter values and will list the entry functions called along the arguments passed to the function and any settings that apply to that function. The dumper output can be of tremendous value when developing and debugging a post processor.

**CNC file usage**
The Autodesk Post Processor extension comes with built-in CNC intermediate files that are generated using the HSM Benchmark Parts. These can be used for testing most aspects of the post processor, but there are times when you will need to test specific scenarios. For these cases you can create your own CNC file to use as input.
By using this API you can export cnc files from fusion 360 to vs code with ease.

To know more about the Autodesk post processor refer the training guide here https://cam.autodesk.com/posts/posts/guides/Post%20Processor%20Training%20Guide.pdf


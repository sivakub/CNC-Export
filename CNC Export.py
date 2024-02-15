#Author-Boopathi Sivakumar
#Description-Dumper Export and CNC file export
import adsk.core, adsk.fusion, adsk.cam, traceback, os

#Common Calls
app = adsk.core.Application.cast(None)
ui = adsk.core.UserInterface.cast(None)

# Global list to keep all event handlers in scope.
# This is only needed with Python.
handlers = []

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        # Get the CommandDefinitions collection.
        cmdDefs = ui.commandDefinitions
        
        addinDefnition = cmdDefs.addButtonDefinition('ExportPostID','Dumper Output','Create Post dumper output','Resources')  

        clickAddins = ExportPostCommandCreatedHandler()
        addinDefnition.commandCreated.add(clickAddins)
        handlers.append(clickAddins)
        
        # Get the ADD-INS panel in the model workspace. 
        addInsPanel = ui.allToolbarPanels.itemById('CAMActionPanel')

        # Add the button to the bottom of the panel.
        buttonControl = addInsPanel.controls.addCommand(addinDefnition)

        buttonControl.isPromotedByDefault = True
        buttonControl.isPromoted = True
       
        # CNC Export Toolbar codes
        CNCaddInsDef = cmdDefs.addButtonDefinition('ExportCNCID','CNC Output','Create CNC Output for HSM Post Edit Utility for VS code','Resources/cnc')
        
        clickCNCaddIns = ExportCNCCommandCreatedHandler()
        CNCaddInsDef.commandCreated.add(clickCNCaddIns)
        handlers.append(clickCNCaddIns)

        CNCaddInsPanel = ui.allToolbarPanels.itemById('CAMActionPanel')

        CNCbuttonControl = CNCaddInsPanel.controls.addCommand(CNCaddInsDef)
        CNCbuttonControl.isPromotedByDefault = True
        CNCbuttonControl.isPromoted = True

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class ExportPostCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)
            cmd = eventArgs.command
            inputs = cmd.commandInputs
            #Create Selection button
            selections =  inputs.addSelectionInput('ncSelection','Select NC file','Select the ncfiles or setups or folders to post')
            selections.setSelectionLimits(1)

            onExecuteDMP = dmpCommandExcuteHandler()
            cmd.execute.add(onExecuteDMP)
            handlers.append(onExecuteDMP)

        except:
         if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class dmpCommandExcuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            doc = app.activeDocument
            products = doc.products
            product = products.itemByProductType('CAMProductType')
            cam = adsk.cam.CAM.cast(product)
            # specify the program name
            programName = doc.name
            outputFolder = cam.temporaryFolder
            
            postConfig = os.path.join(cam.genericPostFolder, 'dump.cps') 
            # specify the NC file output units

            units = adsk.cam.PostOutputUnitOptions.DocumentUnitsOutput 
            postOperations = getSelection()
            #ui.messageBox((ui.activeSelections.objectType))
            if postOperations.count>0 :
                postInput = adsk.cam.PostProcessInput.create(programName, postConfig, outputFolder, units)
                postInput.isOpenInEditor = True
                cam.postProcess(postOperations, postInput)
            else:
                errorMsg()

        except:
         if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class ExportCNCCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            
            eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)
            cmd = eventArgs.command
            inputs = cmd.commandInputs

            #Program Name Input
            global _InputPgName 
            _InputPgName = inputs.addStringValueInput('inputPgName','FileName','1001')
            #Create Selection button
            selections =  inputs.addSelectionInput('ncSelection','Select NC file','Select the ncfiles or setups or folders to post')
            selections.setSelectionLimits(1)
            
            onExecuteCNC = CNCcommandExcuteHandler()
            cmd.execute.add(onExecuteCNC)
            handlers.append(onExecuteCNC)
                  
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class CNCcommandExcuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            doc = app.activeDocument
            products = doc.products
            product = products.itemByProductType('CAMProductType')
            cam = adsk.cam.CAM.cast(product)

            programName = _InputPgName.value
            outputFolder = cam.temporaryFolder
            postConfig =  os.path.join(cam.genericPostFolder, 'export cnc file to vs code.cps') 
            # specify the NC file output units
            units = adsk.cam.PostOutputUnitOptions.DocumentUnitsOutput

            #give all the operation group for the post setup   
            setup = getSelection()
            #ui.messageBox(str(ui.activeSelections.classType()))
            if setup.count > 0  :
                postInput = adsk.cam.PostProcessInput.create(programName, postConfig, outputFolder, units)
                postInput.isOpenInEditor = False
                cam.postProcess(setup, postInput)
            else:
                errorMsg()        
        except:
         if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        # Clean up the UI.
        cmdDef = ui.commandDefinitions.itemById('ExportPostID')
        if cmdDef:
            cmdDef.deleteMe()

        cmdDef1 = ui.commandDefinitions.itemById('ExportCNCID')
        if cmdDef1:
            cmdDef1.deleteMe()
            
        addinsPanel = ui.allToolbarPanels.itemById('CAMActionPanel')
        cntrl = addinsPanel.controls.itemById('ExportPostID')
        if cntrl:
            cntrl.deleteMe()
        cntrl1 = addinsPanel.controls.itemById('ExportCNCID')
        if cntrl1:
            cntrl1.deleteMe()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))	

def getSelection():
    app = adsk.core.Application.get()
    doc = app.activeDocument
    products = doc.products
    product = products.itemByProductType('CAMProductType')
    cam = adsk.cam.CAM.cast(product)

    obcoll = adsk.core.ObjectCollection.create()
    count = int(0)
    setupnos = int(cam.setups.count)

    # Check for all the setups if any operations has been selected or not
    while (count < setupnos):
        setup = cam.setups.item(count)
        # Check if setup is selected or not
        if setup.isSelected == True:
            if setup.isSuppressed == True:
                errorMsg()
            else:
                obcoll.add(setup)
        #Check for all Operations   
        if setup.allOperations.count > 0:
            OpCount = int(0)
            OperationsCount =int(setup.allOperations.count)
            for OpCount in range(OperationsCount):
                CheckOperation = setup.allOperations.item(OpCount)
                #if Operations is selected then collect the operation
                if CheckOperation.isSelected == True :
                    #ui.messageBox(str(CheckOperation.parent.objectType())
                    obcoll.add(CheckOperation)
                OpCount = int(OpCount+1)
        # Check setup has any folders or not

        if setup.folders.count > 0 :
            fldCount = int(0)
            fldCountTotal = int(setup.folders.count)
            for fldCount in range(fldCountTotal):
                selectedFldr = setup.folders.item(fldCount)
                if selectedFldr.isSelected == True :
                    obcoll.add(selectedFldr)
                fldCount = int(fldCount+1)

        # Check for patterns if any
        if setup.patterns.count > 0:
            patCount = int(0)
            patCountTotal = int(setup.patterns.count)
            for patCount in range(patCountTotal):
                selectedPatt = setup.patterns.item(patCount)
                if selectedPatt.isSelected == True :
                    obcoll.add(selectedPatt)
                patCount = int(patCount+1)

        count = int(count+1)

    return obcoll

def errorMsg():

    ui.messageBox("Select valid toolpaths", "Post Process Error",0,4)


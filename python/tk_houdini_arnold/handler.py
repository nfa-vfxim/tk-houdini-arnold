# MIT License

# Copyright (c) 2020 Netherlands Film Academy

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sgtk
import hou
import os


class TkHoudiniArnoldHandler(object):
    # handler class for the actual business logic

    def __init__(self, app):
        # initialize class

        self.app = app

    # class wide methods

    def sceneWasSaved(self, event_type):
        # event callback for saving the scene

        if event_type == hou.hipFileEventType.AfterSave:

            nodes = hou.nodeType(hou.ropNodeTypeCategory(),
                                 "sgtk_arnold").instances()

            for node in nodes:
                self.updateNode(node)

    # methods executed by the hda

    def updateNode(self, node):
        # update all node parameters
        beautyOutputLabel = node.parm("outputLabel")
        beautyOutputString = node.parm("outputPath")

        # update beauty label and string
        try:
            beautyPath = self.__getBeautyPath(node)
            beautyOutputLabel.set(os.path.split(beautyPath)[1])
            beautyOutputString.set(beautyPath)
        except Exception as e:
            self.app.logger.error(
                "One or more parameters on %s could not be set:" % (node))
            self.app.logger.error(e)

        # get all aov parms that are enabled
        aovs = self.__getDifferentFileAOVs(node)

        # for each found parm, update the filepath
        for aov in aovs:
            self.__updateAOVParm(node, aov)

    def useDifferentFileAOV(self, **kwargs):
        # callback for use different file on aov's

        node = kwargs["node"]
        parm = kwargs["parm"]

        self.__updateAOVParm(node, parm)

    # private functions

    def __getBeautyPath(self, node):
        # get the main render template path
        self.app.logger.debug(node)

        # get template objects
        renderTemplate = self.app.get_template("output_render_template")
        workFileTemplate = self.app.get_template("work_file_template")
        workFilePath = hou.hipFile.path()

        # get fields from work file
        fields = workFileTemplate.get_fields(workFilePath)

        # format sequence key to houdini formatting
        fields["SEQ"] = "FORMAT: $F"

        # add resolution to fields
        cam = self.__getCameraNode(node)
        fields["width"] = cam.evalParm("resx")
        fields["height"] = cam.evalParm("resy")

        self.app.logger.debug(
            "Using the following fields for path creation: %s" % fields)

        # apply fields and create path
        path = renderTemplate.apply_fields(fields)

        self.app.logger.debug(
            "Built the following path from template: %s" % (path))

        return path

    def __getAOVPath(self, aov, node):
        # get the aov render template path

        # get template objects
        aovTemplate = self.app.get_template("output_aov_template")
        workFileTemplate = self.app.get_template("work_file_template")
        workFilePath = hou.hipFile.path()

        # get fields from work file
        fields = workFileTemplate.get_fields(workFilePath)

        # format sequence key to houdini formatting
        fields["SEQ"] = "FORMAT: $F"

        # add resolution to fields
        cam = self.__getCameraNode(node)
        fields["width"] = cam.evalParm("resx")
        fields["height"] = cam.evalParm("resy")

        # add aov name to fields
        fields["aov_name"] = aov

        self.app.logger.debug(
            "Using the following fields for path creation: %s" % fields)

        # apply fields and create path
        path = aovTemplate.apply_fields(fields)

        self.app.logger.debug(
            "Built the following path from template: %s" % path)

        return path

    def __getCameraNode(self, arnoldNode):
        # return the camera node

        camPath = arnoldNode.evalParm("camera")
        camNode = hou.node(camPath)

        return camNode

    def __getDifferentFileAOVs(self, node):
        # return all enabled aov file parameters

        parms = node.globParms("ar_aov_separate* ^*_file*")

        return parms

    def __updateAOVParm(self, node, parm):
        # update the parameter

        # replace the parameter basename with nothing, leaving the aov number
        aov_number = parm.name().replace("ar_aov_separate", "")
        self.app.logger.debug("running on aov_number %s" % (aov_number))

        # when checkbox is ticked
        if parm.eval():
            node.parm("ar_aov_separate_file%s" % aov_number).lock(False)

            # get the custom layer name
            value = node.parm("ar_aov_exr_layer_name%s" % (aov_number)).eval()

            # if the custom layer name was not used, use aov label
            if not value:
                value = node.parm("ar_aov_label%s" % (aov_number)).eval()

            node.parm("ar_aov_separate_file%s" % (aov_number)).set(
                self.__getAOVPath(value, node))
            node.parm("ar_aov_separate_file%s" % aov_number).lock(True)

        # when checkbox is not ticked
        else:
            parm_path = node.parm("ar_aov_separate_file%s" % aov_number)
            parm_path.lock(False)
            parm_path.set("Disabled")
            parm_path.lock(True)

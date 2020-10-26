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
            self.app.logger.error("One or more parameters on %s could not be set:" % (node))
            self.app.logger.error(e)

    # private functions

    def __getBeautyPath(self, node):
        # get the main render template path

        # get template objects
        renderTemplate = self.app.get_template("output_render_template")
        workFileTemplate = self.app.get_template("work_file_template")
        workFilePath = hou.hipFile.path()
    
        # get fields from work file
        fields = workFileTemplate.get_fields(workFilePath)

        # format sequence key to houdini formatting
        fields["SEQ"] = "FORMAT: $F"

        # add resolution to fields
        camPath = node.evalParm("camera")
        camNode = hou.node(camPath)
        fields["width"] = camNode.evalParm("resx")
        fields["height"] = camNode.evalParm("resy")

        self.app.logger.debug(fields)

        # apply fields and create path
        path = renderTemplate.apply_fields(fields)

        self.app.logger.debug("Built the following path from template: %s" % (path))

        return path
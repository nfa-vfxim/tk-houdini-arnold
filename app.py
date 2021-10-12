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


class TkHoudiniArnold(sgtk.platform.Application):
    # shotgun arnold output node

    def init_app(self):
        # initialize the app

        # Only initialize when HtoA is loaded
        htoa_env = os.getenv('HTOA')

        if htoa_env:
            tk_houdini_arnold = self.import_module("tk_houdini_arnold")
            self.handler = tk_houdini_arnold.TkHoudiniArnoldHandler(self)

            # register callback
            hou.hipFile.addEventCallback(self.handler.sceneWasSaved)

        else:
            self.logger.info("Arnold is not loaded. Skipping importing for tk-houdini-arnold.")

    def destroy_app(self):
        # breakdown the app
        if self.htoa_env:
            hou.hipFile.removeEventCallback(self.handler.sceneWasSaved)

    def getWorkFileTemplate(self):
        # return the work file template object

        template = self.get_template("work_file_template")

        return template

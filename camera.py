import subprocess

class Camera():
    def __init__(self):
        # Set command to capture and download camera image
        name = "--filename 'img.jpg'"
        opts = "--force-overwrite --capture-image-and-download"
        self.command = "gphoto2 " + name + " " + opts

        

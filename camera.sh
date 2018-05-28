# gphoto2 --force-overwrite --filename 'img.jpg' --capture-image-and-download

gphoto2 --capture-movie --stdout > fifo.mjpg &

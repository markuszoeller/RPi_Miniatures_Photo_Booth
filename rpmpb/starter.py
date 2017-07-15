import os
from os.path import expanduser
HOME = expanduser("~")
import re
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import sys
try:
    import picamera
    import RPi.GPIO as GPIO
except:
    print("we just gonna test things outside of a raspy")
import time


# create our little application :)
app = Flask(__name__)



# TODO use logging

@app.route('/')
def show_albums():
    return redirect(url_for('show_entries'))
    
@app.route('/albums/')
def show_entries():
    gallery = Gallery()
    return render_template('albums.html', entries=gallery.get_albums())

def _slugify(text):
    # ascii it is (I'm biased)
    slug = text.encode('ascii', 'ignore')
    # lower case and without space left and right
    slug = slug.lower().strip()  
    # replace all occurences of a chars series which are not letters or numbers 
    # with one single dash
    slug = re.sub(r'[^a-z0-9]+', '-', slug)  
    # ^ could add '-' at the beginning or end, let's remove that
    slug = slug.strip('-')  
    return slug


@app.route('/previews/')
def show_preview():
    return render_template('previews.html', preview="preview.png")


@app.route('/previews/capture/')
def capture_preview():
    c = Camera()
    c.capture("static/images/preview.png")
    return redirect('/previews/')


@app.route('/albums/<album_id>/', methods=['POST', 'GET'])
def show_album(album_id=None):
    print("mz: show album")
    if album_id == "new":
        if request.method == "POST":
            name = request.form['name']
            name = _slugify(name)
            desc = request.form['description']
            g = Gallery()
            g.create_album(name, desc)
            return redirect('/albums/' + name + '/')
        else:
            print("mz: create album")
            return render_template('album_new.html')
    else:
        print("mz: album details")
        g = Gallery()
        entries = g.get_minis(album_id)
        return render_template('album_details.html', entries=entries)
   
@app.route('/albums/<album_id>/minis/<mini_id>/', 
           methods=['POST', 'GET'])
def show_mini(album_id, mini_id):
    print("mz: show mini")
    if mini_id == "new":
        if request.method == "POST":
            name = request.form['name']
            desc = request.form['description']
            name = _slugify(name)
            g = Gallery()
            g.create_mini(album_id, name, desc)
            return redirect('/albums/' + album_id + '/minis/' + name + '/')
        else:
            print("mz: create mini")
            return render_template('mini_new.html')
    else:
        print("mz: mini details")
        imgs = Gallery().get_mini_images(album_id, mini_id)
        print(imgs)
        path = ""
        numbers = ""
        if len(imgs) > 0:
            path = os.path.dirname(imgs[0]) + "/####.png"  # TODO Gallery attribute?
            numbers = "0.." + str(len(imgs) - 1)
        return render_template('mini_details.html', path=path, numbers=numbers)

@app.route('/albums/<album_id>/minis/<mini_id>/new/', 
           methods=['POST', 'GET'])
def capture_mini(album_id, mini_id):
    print("mz: capture mini")
    if "picamera" not in sys.modules: # TODO make that configurable
        camera = CameraFake()
    else:
        camera = Camera()
    if "RPi.GPIO" not in sys.modules: # TODO make that configurable
        print("mz: We gonna fake the motor")
        stepmotor = StepMotorFake()
    else:
        stepmotor = StepMotor()
    gallery = Gallery()
    photo_session = PhotoSession(camera, stepmotor)
    if PhotoSession.is_in_progress:
        return redirect('/error/')  # TODO put message in here
    file_path = gallery.get_mini_dir(album_id, mini_id)
    photo_session.start(32, file_path)  # TODO use config
    return redirect('/albums/' + album_id + '/minis/' + mini_id + '/') # TODO return 'accepted' status code and take photos async

@app.route('/error/')
def show_error():
    # TODO that message needs to be given from the outside
    return render_template('error.html', msg="session in progress"), 403

@app.route('/albums/<album_id>/minis/<mini_id>/360')
def show_mini_360(album_id, mini_id):
    return render_template('mini_360.html')


class Gallery(object):

    def __init__(self):
        # TODO make that configurable
        self.pic_dir = os.path.join(HOME, "Pictures/Miniatures/gallery/")
        try:
            if not os.path.exists(self.pic_dir):
                os.makedirs(self.pic_dir)
        except:
            print("mz: could not create dir %s" % self.pic_dir)

    def get_albums(self):
        entries = os.listdir(self.pic_dir)
        return [e for e in entries if os.path.isdir(os.path.join(self.pic_dir, e))]

    def create_album(self, name, desc):
        album_dir = os.path.join(self.pic_dir, name)
        os.mkdir(album_dir)
        with open(os.path.join(album_dir, 'attributes.txt'), 'a') as f:
            f.write(desc)

    def get_minis(self, album):
        album_dir = os.path.join(self.pic_dir, album)
        entries = os.listdir(album_dir)
        return [e for e in entries 
                if os.path.isdir(os.path.join(album_dir, e))]        

    def get_mini_images(self, album, mini):
        mini_dir = os.path.join(self.pic_dir, album, mini)
        entries = os.listdir(mini_dir)
        return sorted([ os.path.join(album, mini, e) for e in entries 
                      if e.endswith(".png")])  # TODO is image???
    
    def get_mini_dir(self, album, mini):
        return os.path.join(self.pic_dir, album, mini)

    def create_mini(self, album, name, desc):
        mini_dir = os.path.join(self.pic_dir, album, name)
        os.mkdir(mini_dir)
        with open(os.path.join(mini_dir, 'attributes.txt'), 'a') as f:
            f.write(desc)

class StepMotor(object):

    def __init__(self):
        GPIO.setmode(GPIO.BCM)  # TODO: change to board layout
        GPIO.setwarnings(False)
        self.coil_A_1_pin = 17 # 4 # pink
        self.coil_A_2_pin = 24 # 17 # orange
        self.coil_B_1_pin = 4 # 23 # blue
        self.coil_B_2_pin = 23 # 24 # yellow
        GPIO.setup(self.coil_A_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_A_2_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_2_pin, GPIO.OUT)
        self.StepCount = 8
        self.Seq = range(0, self.StepCount)
        self.Seq[0] = [0,1,0,0]
        self.Seq[1] = [0,1,0,1]
        self.Seq[2] = [0,0,0,1]
        self.Seq[3] = [1,0,0,1]
        self.Seq[4] = [1,0,0,0]
        self.Seq[5] = [1,0,1,0]
        self.Seq[6] = [0,0,1,0]
        self.Seq[7] = [0,1,1,0]

    def setStep(self, w1, w2, w3, w4):
        GPIO.output(self.coil_A_1_pin, w1)
        GPIO.output(self.coil_A_2_pin, w2)
        GPIO.output(self.coil_B_1_pin, w3)
        GPIO.output(self.coil_B_2_pin, w4)

    def forward(self, delay, steps):
        for i in range(steps):
            print("step: %d" % i)
            for j in range(self.StepCount):
                self.setStep(self.Seq[j][0], self.Seq[j][1], 
                             self.Seq[j][2], self.Seq[j][3])
                # print("wait for %0.2f s" % delay)
                time.sleep(delay)
    
    def rotate_360(self, segments=4, pause=1, clockwise=True, pause_callback=None):
        # make enough steps to divide the 360 round into n segments
        # pause after each segment for n seconds
        # call pause_callback and give it the segment number
        if pause_callback:
            pause_callback(0)
        steps = 4096 / self.StepCount / segments  # TODO magic number
        for segment in range(1, segments):
            self.forward(0.1, steps)
            if pause_callback:
                pause_callback(segment)

class StepMotorFake(StepMotor):
    def __init__(self):
        self.StepCount = 8

    def forward(self, delay, steps):
        print("mz: Fake move forward")


class Camera(object):
    
    def capture(self, file_name):
        print("mz: capture image: %s" % file_name)
        with picamera.PiCamera() as cam:
            cam.capture(file_name)

class CameraFake(Camera):
    def capture(self, file_name):
        print("mz: fake camera capture: %s" % file_name)

class PhotoSession(object):
    
    is_in_progress = False

    def __init__(self, camera, stepmotor):
        self.camera = camera
        self.motor = stepmotor
        if not os.path.exists('static/images'):
            os.symlink(Gallery().pic_dir, 'static/images')  # TODO make that nice
    
    def start(self, segments, file_path):
        PhotoSession.is_in_progress = True
        print("mz: start photosession: %s" % file_path)

        def _capture(segment):
            self.camera.capture(file_path + "/" + '%04d' % segment + ".png")    
        
        # TODO that needs to be async, that takes a while
        # http://stackoverflow.com/a/1239108
        self.motor.rotate_360(segments, pause_callback=_capture)
        PhotoSession.is_in_progress = False


def main():
    app.run()


if __name__ == "__main__":
    main()


#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Demonstrates how to  to record a video file on the robot"""

import qi
import argparse
import sys
import time


def main(session):
    """
    This example demonstrates how to use the ALVideoRecorder module to record a
    video file on the robot.
    """
    # Get the service ALVideoRecorder.

    vid_recorder_service = session.service("ALVideoRecorder")
    videoInfo = vid_recorder_service.stopRecording()

    # This records a 320*240 MJPG video at 20 fps.
    # Note MJPG can't be recorded with a framerate lower than 3 fps.
    vid_recorder_service.setResolution(2)
    vid_recorder_service.setFrameRate(20)
    vid_recorder_service.setCameraID(0)
    vid_recorder_service.setVideoFormat("MJPG")
    vid_recorder_service.setColorSpace(13)
    vid_recorder_service.startRecording("/home/nao/recordings/cameras", "myvideoCameraBottom")

    #time.sleep(5)
    while True:
        try:
            time.sleep(.3)
        except KeyboardInterrupt:
            # Video file is saved on the robot in the
            # /home/nao/recordings/cameras/ folder.
            videoInfo = vid_recorder_service.stopRecording()

            print "Video was saved on the robot: ", videoInfo[1]
            print "Num frames: ", videoInfo[0]
            sys.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)

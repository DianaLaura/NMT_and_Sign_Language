from datetime import time, timedelta, datetime



def timestamp_to_50_fps(timestamp):
    time = datetime.strftime(timestamp, '%H:%M:%S:%f') 
    hours = int(time[0:2])
    minutes = int(time[3:5]) + (hours * 60)
    seconds = int(time[6:8]) + (minutes * 60)
    frames = int(time[9:11]) + (seconds * 50)

    return frames

def fps_50_to_fps_30(frames_50_fps):
    secs = frames_50_fps / 50
    return int(round((secs * 30),0))
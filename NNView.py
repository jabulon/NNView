import sys
import subprocess
import socket

# 15/7/2017
# Eli Abramson

#global variables
controlPort = 9000
currentlyRecording = False

def listener(port):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('', port))
    serversocket.listen(5) # become a server socket, maximum 5 connections

    while True:
        connection, address = serversocket.accept()
        buffer = connection.recv(256)
        print ("Command received from: " + address[0] + ":" + str(address[1]) + " : " + str(buffer))
        bufferToArgs(buffer)
        if not currentlyRecording:
            print("Launching recorder")
            runFfmpegDesktop(bufferToArgs(buffer))
        connection.close()

def bufferToArgs(buffer):
    strParam = []
    splitStr = buffer.split()
    for parametr in splitStr:
        strParam.append(str(parametr, 'utf-8'))

    #['error', '-an', 'desktop', '1', '40', '16', 'file2.flv', '1', '2', '6']
    return(strParam)

#def notifyVSE():
    #nginX ot responding
    #general error + exception


#example for received parameters: error -an desktop -r 6 -c:v libx264 -preset ultrafast -crf 40 4 -g 32 -tune zerolatency -f 192.168.220.40 1935 live streamID

#Launch FFMPEG in desktop mode
def runFfmpegDesktop(args):

    loglevel = args[0]
    sound = args[1]
    inputMethod = args[2]
    frameRate = args[3]
    crf = args[4]
    keyFrame = args[5]
    nginxServer = args[6]
    nginxPort = args[7]
    nginxApp = args[8]
    streamId = args[9]

    ffmpeg = subprocess.call(
        ['ffmpeg.exe', '-loglevel', loglevel, sound, '-f', 'gdigrab', '-i', inputMethod, '-r', frameRate,
         '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', crf, '-r', frameRate, '-g', keyFrame, '-tune',
         'zerolatency', '-f', 'flv', 'rtmp://' + nginxServer + ':' + nginxPort + '/' + nginxApp + '/' + streamId])

    currentlyRecording = True

    #return ffmpeg's exit code
    return(ffmpeg)

#Launch FFMPEG in window mode
def runFfmpegWindow(parameters):

    ffmpeg = subprocess.call(
        ['ffmpeg.exe', '-loglevel', 'error', '-an', '-f', 'gdigrab', '-i', 'desktop', '-r', '1', '-c:v', 'libx264',
         '-preset', 'ultrafast', '-crf', '40', '-r', '1', '-g', '16', '-tune', 'zerolatency', 'file.flv'])
    print("FFMPEG exited with: " + ffmpeg)
    #stdin q
    #currentlyRecording = False
    return(ffmpeg)

def main():
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if len(args) != 10:
        print ("ERROR: Incorrect number of arguments\nUsage: NNview.exe error -an desktop 1 40 16 file2.flv 1 2 3")
        sys.exit(1)
    listener(controlPort)

    #if args[2] == 'desktop':
        #runFfmpegDesktop(args)
    #else:
        #runFfmpegWindow(args)





if __name__ == '__main__':
  main()
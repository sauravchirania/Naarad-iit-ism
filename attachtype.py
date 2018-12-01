image_extensions = ['jpeg', 'bmp', 'png', 'gif', 'tiff']
video_extensions = ['3g2', '3gp', '3gpp', 'asf', 'avi', 'dat', 'divx', 'dv',
'f4v', 'flv', 'gif', 'm2ts', 'm4v', 'mkv', 'mod', 'mov', 'mp4', 'mpe', 'mpeg',
'mpeg4', 'mpg', 'mts', 'nsv', 'ogm', 'ogv', 'qt', 'tod', 'ts', 'vob', 'wmv']

def attachmentType(attachName):
    #returns 0 if attachment is image
    #returns 1 if attachment is video
    #returns 2 if attachment is neither image or video.
    
    l = attachName.split('.')
    if(len(l)>=2):
        if(l[-1].lower() in image_extensions):
            return 0
        elif(l[-1].lower() in video_extensions):
            return 1
    return 2
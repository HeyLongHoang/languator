import numpy as np
import cv2
import os
from PIL import Image
import core



# Converting to RGB color format
def convertColor(img,option=0):
    """
    Convert image color space
    :param img: Image matrix returned by cv2.imread()
    :param option: Correspond to core.COLOR_OPTIONS
    :return: New image matrix
    """
    if option == 0:
        None
    elif option == 1:
        None
    elif option == core.OptionsColor['GRAYSCALE']:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    elif option == core.OptionsColor['HSV']:
        img = cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
    elif option == core.OptionsColor['CMY']:
        img = cv2.cvtColor(img,cv2.COLOR_RGB2YCrCb)
    return img
# Open an image and process it
def processImg(img_path,new_path,color,resize,flip_axis):
    """
    Process image 
    Args:
    img_path: Path to image to be processed
    new_path: Path to save processed image
    color: Color option
    resize: Size option
    flip_axis: Flip option
    """
    img = cv2.imread(img_path)
    
    img = convertColor(img,color)
    
    (height, width) = img.shape[:2]
    if resize == core.OptionsCrop['4:3']:
        img = cv2.resize(img, (int(width), int(width/4*3)), interpolation = cv2.INTER_CUBIC)
    elif resize == core.OptionsCrop['16:9']:
        img = cv2.resize(img, (int(width), int(width/16*9)), interpolation = cv2.INTER_CUBIC)
    elif resize == core.OptionsCrop['SQUARE']:
        img = cv2.resize(img, (int(max(height,width)), int(max(height,width))), interpolation = cv2.INTER_CUBIC)

    if flip_axis == core.OptionsFlip['HORIZONTAL']:
        img = cv2.flip(img,1)
    elif flip_axis == core.OptionsFlip['VERTICAL']:
        img = cv2.flip(img,0)

    cv2.imwrite(new_path, img)
    return img

# Extract frames from a video
def extractFrame(original_video):
    try:
        # open video for frame extraction
        cam = cv2.VideoCapture(original_video)
    except:
        print("Error: Opening source video")
    try:
        # creating a folder named data
        if not os.path.exists('data'):
            os.makedirs('data')
    # if not created then raise error
    except OSError:
        print ('Error: Creating directory of data')

    currentframe = 0
    while(True):
        ret,frame = cam.read()
        if ret:
            # if video is still left continue creating images
            if currentframe < 10:
                name = './data/frame' + str(0) + str(currentframe) + '.jpg'
            else :
                name = './data/frame' + str(currentframe) + '.jpg'
            if currentframe%10 == 0:
                print ('Created ' + name)
            # writing the extracted images
            cv2.imwrite(name, frame)
            # increasing counter so that it will show how many frames are created
            currentframe += 1
        else:
            break
    
    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()

#Generate edited video from edited frames
def pil_to_cv(pil_image):
    """
    Returns a copy of an image in a representation suited for OpenCV
    :param pil_image: PIL.Image object
    :return: Numpy array compatible with OpenCV
    """
    return np.array(pil_image)[:, :, ::-1]
def writeVideo(file_path, frames, fps):
    """
    Writes frames to an mp4 video file
    :param file_path: Path to output video, must end with .mp4
    :param frames: List of PIL.Image objects
    :param fps: Desired frame rate
    """

    w, h = frames[0].size
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    writer = cv2.VideoWriter(file_path, fourcc, fps, (w, h))

    for frame in frames:
        writer.write(pil_to_cv(frame))

    writer.release() 

# Process and resize frames
def generateVideoFrame(image_folder,color,resize,flip):
    """
    From frames saved as images in a folder, process and resize them 
    :param image_folder: Location of the images
    :return: Array of PIL.Images, processed and resized 
    """

    mean_height = 0
    mean_width = 0
    images = [img for img in os.listdir(image_folder)
              if img.endswith(".jpg") or
                 img.endswith(".jpeg") or
                 img.endswith("png")]     
    # Array images should only consider the image files ignoring others if any
    num_of_images = len(images) 
    print("Total number of frames: " + str(num_of_images))

    # Process the frames
    for file in os.listdir(image_folder):
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"):
            processImg(os.path.join(image_folder, file),os.path.join(image_folder, file),color,resize,flip)

    for image in images:
        im = Image.open(os.path.join(image_folder, image))
        width, height = im.size
        mean_width += width
        mean_height += height
    mean_width = int(mean_width / num_of_images)
    mean_height = int(mean_height / num_of_images)

    pil_images = []
    # Resizing of the images to give them same width and height 
    for file in images:
        # opening image using PIL Image
        im = Image.open(os.path.join(image_folder, file)) 

        imResize = im.resize((mean_width, mean_height), Image.ANTIALIAS) 
        #imResize.save( file, 'JPEG', quality = 95) # setting quality
        # printing each resized image name
        pil_images.append(imResize)
        #print(im.filename.split('\\')[-1], " is resized") 
    print("Frames have been resized and ready to be written into video")
    return pil_images
    
# To extract and process a video
def processVideo(org_vid,new_vid,color,resize,flip,fps):
    """
    Process video
    Args:
    org_vid: Path to video to be processed
    new_vid: Path to save processed video
    color: Color option
    resize: Size option
    flip: Flip option
    fps: Video fps
    """
    extractFrame(org_vid)
    pil_images = generateVideoFrame(core.IMAGE_FOLDER,color,resize,flip)
    writeVideo(new_vid,pil_images,fps)

#processVideo(core.ORIGINAL_VIDEO, core.GENERATED_VIDEO, -1,1,-1,40)

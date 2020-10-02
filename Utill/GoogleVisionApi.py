import io
import os

# 구글 라이브러리 import
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image
from PIL import ImageDraw

from Utill  import UtillFileDirectot



likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')



IMAGE_SIZE = 96,96
#global_image_hash

def draw_hint(strFullPath, image_file, vects, strOutputPath):
    """Draw a border around the image using the hints in the vector list."""
    #vects = get_crop_hint(strFullPath + image_file)

    #디렉토리가 없으면 만들어준다.
    UtillFileDirectot.CreateCurrentDateDiretory(strOutputPath)

    im = Image.open(strFullPath + image_file)

    if type(vects) == type(list()) :
        draw = ImageDraw.Draw(im)
        for vect in vects :
            draw.polygon([
                vect[0].x, vect[0].y,
                vect[1].x, vect[1].y,
                vect[2].x, vect[2].y,
                vect[3].x, vect[3].y], None, 'red')

    else :
        draw = ImageDraw.Draw(im)
        draw.polygon([
            vects[0].x, vects[0].y,
            vects[1].x, vects[1].y,
            vects[2].x, vects[2].y,
            vects[3].x, vects[3].y], None, 'red')
    
    #image_file.replace(".png", ".jpg")
    #im.save(strOutputPath + image_file, 'JPEG')
    im.save(strOutputPath + image_file, 'png')

    im.close()

    print('Saved new image to {}'.format(image_file))

def crop_to_hint(strFullPath, image_file, vects, strOutputPath):
    """Crop the image using the hints in the vector list."""

    #디렉토리가 없으면 만들어준다.
    UtillFileDirectot.CreateCurrentDateDiretory(strOutputPath)

    im = Image.open(strFullPath + image_file)

    nCnt = 0

    if type(vects) == type(list()) :
        for vect in vects :
            im2 = im.crop([vect[0].x, vect[0].y,
                vect[2].x - 1, vect[2].y - 1])

            # 크기를 IMAGE_SIZE로 변환해서 저장해줌(학습을 위해 같은 크기로!)
            im2 = im2.resize(IMAGE_SIZE,Image.ANTIALIAS)
            
            image_file = image_file.replace(".png", "") + "F{0:03d}".format(nCnt) + ".png"
            im2.save(strOutputPath + image_file, 'png')

            nCnt += 1

            im2.close()


    else :
        im2 = im.crop([vect[0].x, vect[0].y,
                vect[2].x - 1, vect[2].y - 1])

        # 크기를 IMAGE_SIZE로 변환해서 저장해줌(학습을 위해 같은 크기로!)
        im2 = im2.resize(IMAGE_SIZE,Image.ANTIALIAS)

        image_file = image_file.replace(".png", "") + "F{0:03d}".format(nCnt) + ".png"
        im2.save(strOutputPath + image_file, 'png')

        im2.close()

    im.close()
    



def crop_face(image_file,rect,outputfile):
    
    try:
        with io.open(image_file, 'rb') as image_file:
            content = image_file.read()
        
        #image = types.Image(content=content)
        crop = content.crop(rect)


        fd = io.open(image_file,'rb')
        image = Image.open(fd)  

        # extract hash from image to check duplicated image
        #m = hashlib.md5()
        #with io.BytesIO() as memf:
        #    image.save(memf, 'PNG')
        #    data = memf.getvalue()
        #    m.update(data)
        #image_hash = m.hexdigest()
        #
        #if image_hash in global_image_hash:
        #    print('[Error] %s: Duplicated image' %(image_file) )
        #    return None
        #global_image_hash.append(image_hash)

        crop = image.crop(rect)
        im = crop.resize(IMAGE_SIZE,Image.ANTIALIAS)
        
        
        im.save(outputfile,"JPEG")
        fd.close()
        print('[Info]  %s: Crop face %s and write it to file : %s' %( image_file,rect,outputfile) )
        return True
    except Exception as e:
        print('[Error] %s: Crop image writing error : %s' %(image_file,str(e)) )


#if __name__ == '__main__':
#run_quickstart("IMG.jpg")

#a = 0


def run_quickstart(strPath, strFile_name) :
 
    # 사용할 클라이언트 설정
    client = vision.ImageAnnotatorClient()
    
    # 이미지 읽기
    with io.open(strPath + strFile_name, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    
    image_file.close()


    # Object 뽑아냄 
    ##response = client.object_localization(image=image)
    ##Objects = response.localized_object_annotations
    ##
    ##if len(Objects) > 0 :
    ##    print('Object :')
    ##    listObject = list()
    ##    for Object in Objects:
    ##        print('\n{} (confidence: {})'.format(Object.name, Object.score))
    ##        vertices = Object.bounding_poly.normalized_vertices
    ##        for vertex in Object.bounding_poly.normalized_vertices:
    ##            print(' - ({}, {})'.format(vertex.x, vertex.y))
    ##        #vertices = Object.bounding_poly.normalized_vertices
    ##        listObject.append(vertices)
    ##    
    ##    #정규화되서 다른값으로 저장해주어햔다.
    ##    #draw_hint(strPath, strFile_name, listObject, strPath + "OBJECT\\")


    # label 뽑아냄 -> 라벨은 버티컬이 없다!!
    response = client.label_detection(image=image)
    labels = response.label_annotations
    
    if len(labels) > 0 :
        print('Labels:')
        for label in labels:
            print(label.description + " = " + str(int(label.score*100)) + "%")


    ###HINT 뽑아냄 -> 가장 포커스가 맞춰지는 부분의 1.77를 뽑아내는듯하다.
    ##crop_hints_params = types.CropHintsParams(aspect_ratios=[1.77])
    ##image_context = types.ImageContext(crop_hints_params=crop_hints_params)
    ##
    ##response = client.crop_hints(image=image, image_context=image_context)
    ##hints = response.crop_hints_annotation.crop_hints
    ##
    ##if len(hints) > 0 :
    ##    listHint = list()
    ##
    ##    for hint in hints :
    ##        vertices = hint.bounding_poly.vertices
    ##        listHint.append(vertices)
    ##    draw_hint(strPath, strFile_name, listHint, strPath + "HINT\\")

    # Face를 뽑아냄
    response = client.face_detection(image=image)
    faces = response.face_annotations
    

    if len(faces) > 0 :
        print('Faces:')

        listVertex = list()

        for face in faces:
            print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
            print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
            print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

            vertices = (['({},{})'.format(vertex.x, vertex.y)
                        for vertex in face.bounding_poly.vertices])

            print('face bounds: {}'.format(','.join(vertices)))

            listVertex.append(face.bounding_poly.vertices)
        
        #draw_hint(strPath, strFile_name, listVertex, strPath + "FACE\\")
        crop_to_hint(strPath, strFile_name, listVertex, strPath + "FACE\\")




class GoogleVisionAPI(object):
    #def __init__(self, credential, image):
    def __init__(self, image):
        #json_credential = credential
        img_file = image
        self.img_file = img_file
        #self.face_max_results = face_max_results
        # for internal
        self.client = None
        self.image = None
        self._open()

    def _open(self):
        #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.json_credential
        self.client = vision.ImageAnnotatorClient()
        with io.open(os.path.abspath(self.img_file), 'rb') as ifp:
            content = ifp.read()
        # noinspection PyUnresolvedReferences
        self.image = vision.types.Image(content=content)
        
        
    def DetectFace(self):
        rp = self.client.face_detection(image=self.image)





    def do(self, op):
        if op == 'Face':
            rp = self.client.face_detection(image=self.image)
            r = self._save_face_result(rp, self.argspec.output_image)
            sys.stdout.write(str(r))
        elif op == 'Label':
            rp = self.client.label_detection(image=self.image)
            r = self._save_label_result(rp, self.argspec.output_image)
            c = csv.writer(sys.stdout, lineterminator='\n')
            c.writerow(['description', 'score'])
            if r:
                for line in r:
                    c.writerow(line)
        elif op == 'Landmark':
            rp = self.client.landmark_detection(image=self.image)
            r = self._save_landmark_result(rp, self.argspec.output_image)
            c = csv.writer(sys.stdout, lineterminator='\n')
            c.writerow(['description', 'score', 'latitude', 'longitude'])
            if r:
                for line in r:
                    c.writerow(line)


    # noinspection PyMethodMayBeStatic
    def _save_landmark_result(self, rp, save_img_path):
        if save_img_path:
            img = cv2.imread(self.img_file)
            overlay = img.copy()
        lines = list()
        rs = rp.landmark_annotations
        for lm in rs:
            row = [lm.description, float('%.2f' % lm.score)]
            box = [(vertex.x, vertex.y) for vertex in lm.bounding_poly.vertices]
            if save_img_path:
                cv2.rectangle(overlay, box[0], box[2], (255, 0, 255), 2)
                cv2.putText(overlay, lm.description, (box[0][0]+10, box[0][1]+20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
            for loc in lm.locations:
                row.extend([loc.lat_lng.latitude, loc.lat_lng.longitude])
            lines.append(row)
        if save_img_path:
            alpha = 0.7
            image_new = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
            cv2.imwrite(save_img_path, image_new)
        return lines




#GoogleVisionAPITemp = GoogleVisionAPI("My_First_Project-8c08c8e8a7ec.json", "IMG.jpg")
#GoogleVisionAPI.do()










import io
import os

# 구글 라이브러리 import
from google.cloud import vision
from google.cloud.vision import types


def run_quickstart(file_name) :
 
    # 사용할 클라이언트 설정
    client = vision.ImageAnnotatorClient()
    
    # 이미지 읽기
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
 
    image = types.Image(content=content)
 
    # label 뽑아냄.
    response = client.label_detection(image=image)
    labels = response.label_annotations
 
    print('Labels:')
    for label in labels:
        print(label.description + " = " + str(int(label.score*100)) + "%")




#if __name__ == '__main__':
#run_quickstart("IMG.jpg")

#a = 0





class GoogleVisionAPI(object):
    def __init__(self, credential, image):
        json_credential = credential
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
        a = 0

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










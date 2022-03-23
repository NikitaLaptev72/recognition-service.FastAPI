import os
import pickle
import dlib
from skimage import io
from scipy.spatial import distance
import easygui

sp = dlib.shape_predictor('/home/nikita/Downloads/shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('/home/nikita/Downloads/dlib_face_recognition_resnet_model_v1.dat')
detector = dlib.get_frontal_face_detector()


def face_rec(ids_array, vectors_array):
    '''
    Чтение шаблонов из бд и распознавание лица по фотографии
    '''
    face_descriptors = []
    for i in vectors_array:
        face_descriptors.append(pickle.loads(pickle.loads(i)))

    img = io.imread(easygui.fileopenbox(filetypes=["*.jpeg"]))
    dets_webcam = detector(img, 1)
    for k, d in enumerate(dets_webcam):
        shape = sp(img, d)
    main_descriptor = facerec.compute_face_descriptor(img, shape)

    distances = []
    for i in face_descriptors:
        distances.append(distance.euclidean(main_descriptor, i))
    min_dist = min(distances)

    return ids_array[distances.index(min_dist)]


class ImageVector:

    def __init__(self, image_name, vector):
        self.image_name = image_name
        self.vector = vector


def get_vectors_from_images(path_to_photos):
    """
    Вставка шаблонов лиц в бд
    """
    image_vectors = []
    faces = os.listdir(path_to_photos)
    i = 0
    for i in faces:
        img = io.imread(path_to_photos + '/' + i)
        dets = detector(img, 1)
        if len(dets) != 0:
            for k, d in enumerate(dets):
                shape = sp(img, d)
            vector = ImageVector(
                path_to_photos + '/' + i,
                pickle.dumps(facerec.compute_face_descriptor(img, shape))
            )
            image_vectors.append(vector)
        else:
            print(path_to_photos + '/' + i)
    return image_vectors


def get_vector_from_image():
    """
    Вставка шаблона выбранного лица в бд
    """
    imp_path = easygui.fileopenbox(filetypes=["*.jpeg"])
    img = io.imread(imp_path)
    dets = detector(img, 1)
    if len(dets) != 0:
        for k, d in enumerate(dets):
            shape = sp(img, d)
        vector = ImageVector(
            imp_path,
            pickle.dumps(facerec.compute_face_descriptor(img, shape))
        )
    else:
        print(img)
    return vector

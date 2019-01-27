import numpy as np
import os
from keras.models import load_model
import sys
import codecs
from keras import backend as K


class Predictor(object):

    def __init__(self):
        self.colNames = ["block1", "block2", "isClone", "COMP1", "NOS1", "HVOC1", "HEFF1", "CREF1", "XMET1", "LMET1",
                         "NOA1", "HDIF1", "VDEC1", "EXCT1", "EXCR1", "CAST1",
                         "NAND1", "VREF1", "NOPR1", "MDN1", "NEXP1", "LOOP1", "NBLTRL1", "NCLTRL1", "NNLTRL1",
                         "NNULLTRL1", "NSLTRL1", "COMP2", "NOS2", "HVOC2", "HEFF2", "CREF2",
                         "XMET2", "LMET2", "NOA2", "HDIF2", "VDEC2", "EXCT2", "EXCR2", "CAST2", "NAND2", "VREF2",
                         "NOPR2", "MDN2", "NEXP2", "LOOP2", "NBLTRL2", "NCLTRL2", "NNLTRL2",
                         "NNULLTRL2", "NSLTRL2"]

        self.thread_counter = 0
        self.num_candidates_31 = 0
        self.array_31 = []
        dirname = os.path.dirname(__file__)
        self.modelfilename_type31 = os.path.join(dirname, 'ml/trained_model0.h5')
        #self.modelfilename_type31 = './ml/trained_model0.h5'
        self.loadModel()
        self.clone_pairs = ''
        self.clone_pairs_count = 0
        self.type2_clonepairs_count = 0
        self.FINISHED = 0
        self.CONTINUE = 1
        self.BATCH_SIZE_FOR_PREDICTION = 1
        self.CLONE_FILE_SIZE = 10000

    def loadModel(self):
        self.loaded_model_type31 = load_model(self.modelfilename_type31)
        print("models loaded")

    def predict_clones(self, array):
        try:
            array_pred = np.array(array)
            X_test = array_pred[:, [i for i in range(3, 51)]]
            X_test = X_test.astype(float)
            X1 = X_test[:, [i for i in range(0, 24)]]
            X2 = X_test[:, [i for i in range(24, 48)]]
            pred = self.loaded_model_type31.predict([X1, X2], batch_size=self.BATCH_SIZE_FOR_PREDICTION, verbose=0)
            predictions = np.zeros_like(pred)
            index = pred > 0.89
            predictions[index] = 1
            for i in range(predictions.shape[0]):
                if predictions[i]:
                    return True
                else:
                    return False
        except Exception:
            print(sys.exc_info()[0])
            return False

    def process(self, data):

        #data_splitted = data.split('#$#')
        candidate_pairs = data.split('~~')
        self.array_31 = []
        self.array_31.append(candidate_pairs)
        self.num_candidates_31 += 1
        if len(self.array_31) == self.BATCH_SIZE_FOR_PREDICTION:
            print("prediction started")
            return self.predict_clones(self.array_31)

    def clear_session(self):
        K.clear_session()

if __name__ == "__main__":
    p = Predictor()
    test_file = "/Users/vaibhavsaini/Downloads/IC_train_20per.txt"
    try:
        with codecs.open(test_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                print(p.process(line), line)
    except FileNotFoundError:
        pass  # do nothing.
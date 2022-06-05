import cv2
import copy
import numpy as np

# classe responsabile per il disegno vero e proprio
class Board:
    def __init__(self):
        # il disegno sarà contenuto sotto forma di canvas
        self.canvas = None
        self.mode = "draw"

        # si potrà tornare indietro a istanze antecedenti del disegno
        # (una nuova istanza sarà creata ogni volta che c'è qualcosa di nuovo nel disegno)
        self.old_me = []
        self.new_thing = False

        # il disegno sarà creato collegando con delle linee ogni punto registrato
        self.x1, self.y1 = 0, 0
        self.x2, self.y2 = 0, 0

    def init_board(self, img):
        # il canvas sarà inizializzato con le dimensioni dell'immagine sulla quale si vuole disegnare
        if self.canvas is not None:
            return

        self.canvas = np.zeros_like(img)
        self.old_me.append(copy.deepcopy(self.canvas))

    def finger_on_board(self, pos_x, pos_y):
        # metodo che registra una nuova posizione del dito sul disegno

        if self.canvas is None:
            return False

        # quando il dito viene spostato in una qualsiasi posizione del disegno
        # si registra che c'è una nuova istanza da registrare
        self.new_thing = True

        self.x2 = pos_x
        self.y2 = pos_y

        # se la precedente posizione è (0, 0) vuol dire che si sta iniziando una nuova linea
        # quindi per questa volta la partenza e l'arrivo coincideranno
        if self.x1 == 0 and self.y1 == 0:
            self.x1, self.y1 = self.x2, self.y2
            return True

        # a seconda della modalità che è attualmente impostata si disegnerà una linea dallo "scorso punto" all'attuale
        # oppure si andra a cancellare quello che era precedentemente contenuto in quella posizione del canvas
        if self.mode == "draw":
            cv2.line(self.canvas, (self.x1, self.y1), (self.x2, self.y2), (255, 255, 255), 5)
        else:
            cv2.circle(self.canvas, (self.x1, self.y1), 20, (0, 0, 0), -1)

        # il punto attuale viene registrato come prossimo punto d'inizio
        self.x1, self.y1 = self.x2, self.y2
        return True

    def finger_off_board(self):
        # metodo per indicare che il dito non è più sulla "scrivania" i parametri verranno resettati

        self.x1, self.y1 = 0, 0

        if self.canvas is None:
            return

        # se ci sono presenti nuovi dettagli nell'attuale istanza essa sarà "conservata"
        if self.new_thing:
            self.old_me.append(copy.deepcopy(self.canvas))
            self.new_thing = False

    def undo(self):
        # metodo utilizzato per ripristinare una vecchia istanza del disegno
        # essa può essere ripristinata (naturalmente) solo se ci sono vecchie istanza del disegno
        if len(self.old_me) <= 1:
            return

        # viene cancellata l'attuale versione sulla quale si stà lavorando
        self.old_me.pop()
        self.canvas = None

        # la vecchia versione viene impostata come attuale
        self.canvas = copy.deepcopy(self.old_me[-1])

    def change_mode(self):
        # metodo utilizzato per cambiare l'attuale modalità d'interazione con il disegno

        if self.mode == "draw":
            self.mode = "delete"
        else:
            self.mode = "draw"
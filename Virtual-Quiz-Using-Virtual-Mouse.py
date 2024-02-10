import math
import cv2
import cvzone
import time
import csv
from cvzone.HandTrackingModule import HandDetector


class Mcq():

    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])

        self.useranswer = None

    def updat(self, x, y, bbxs):
        for n, b in enumerate(bbxs):
            x1, y1, x2, y2 = b

            if x1 < x < x2 and y1 < y < y2:
                self.useranswer = n + 1

                # رسم مستطيل
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)


# فتح ملف csv
path = "Mcq.csv"
with open(path, newline="\n") as f:
    reder = csv.reader(f)
    dataAll = list(reder)

Qn = 0

Qtotal = len(dataAll)

lqustion = []

# وضع كل سطر في ملف csv علي هيئه bject
for data in dataAll:
    lqustion.append(Mcq(data))
print(len(lqustion))

# فتح كاميرا الجهاز

cap = cv2.VideoCapture(0)

# تحجيم النافه الثانيه
cap.set(3, 1200)
cap.set(4, 650)
# استدعاء moudule لاكتشاف اليد
detector = HandDetector()
totaltime = 60

starttime = time.time()

scors = None
while (cap.isOpened()):
    # قراءه الفديو
    _, frame = cap.read()
    # وضع الصوره كالمرايه
    cv2.flip(frame, 1)

    # ايجاد اليد
    hand, g = detector.findHands(frame)
    if Qn < Qtotal:
        mcq = lqustion[Qn]

        # وضع السؤال الذي يظهر علي النافذه
        imr, boxr = cvzone.putTextRect(frame, mcq.question, [100, 100], 2, 2, offset=50, colorR=[0, 0, 0],
                                       border=5)
        # الاختيار الاول
        im1, box1 = cvzone.putTextRect(frame, mcq.choice1, [100, 250], 2, 2, offset=50, colorR=[0, 0, 0],
                                       border=5)
        # الاختيار الثاني
        im2, box2 = cvzone.putTextRect(frame, mcq.choice2, [600, 250], 2, 2, offset=50, colorR=[0, 0, 0],
                                       border=5)
        # الاختيار الثالث
        im3, box3 = cvzone.putTextRect(frame, mcq.choice3, [100, 400], 2, 2, offset=50, colorR=[0, 0, 0],
                                       border=5)
        # الاختيار الرابع
        im4, box4 = cvzone.putTextRect(frame, mcq.choice4, [600, 400], 2, 2, offset=50, colorR=[0, 0, 0],
                                       border=5)

        if hand:
            lm = hand[0]['lmList']

            # ايجاد احداثيات السبابه
            x8, y8, h8 = lm[8]
            x5, y5, h5 = lm[5]
            # ايجاد احداثيات الاوسط
            x12, y12, h12 = lm[12]
            # ايجاد طول بين الاصبعين
            lent = int(math.sqrt((x8 - x12) ** 2 + (y8 - y12) ** 2))

            dis = int(math.sqrt((x8 - x5) ** 2 + (y8 - y5) ** 2))

            scaler = 6.3

            f = 1500
            cv2.line(frame, (x8, y8), (x12, y12), (0, 0, 255), 2)
            # ايجاد المسافه بين الشاشه واليد
            distance = int((scaler * f) / dis)

            # print(lent, distance)

            if lent < 35 and distance < 120:
                scor = 0

                mcq.updat(x8, y8, [box1, box2, box3, box4])
                if mcq.useranswer is not None:
                    for lis in lqustion:
                        if lis.useranswer == lis.answer:
                            scor += 1

                    scors = scor
                    Qn += 1

                    time.sleep(0.5)

    else:

        d, f = cvzone.putTextRect(frame, f" THE QUIZ IS COMPELETED", [100, 300], 2, 2, offset=50,
                                  colorR=[0, 0, 0],
                                  border=5)
        d, f = cvzone.putTextRect(frame, f" THE SCORE {scor}", [750, 300], 2, 2, offset=50,
                                  colorR=[0, 0, 0],
                                  border=5)
    # اظهار النافذه
    cv2.imshow("exam", frame)

    if cv2.waitKey(1) & 0XFF == 27:

        break
cap.release()
cv2.destroyAllWindows()
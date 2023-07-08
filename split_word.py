import cv2
from imutils import contours


def split_word(file_name=None, image=None, save_chars=False):
    if not file_name and image is None: return
    if image is None:
        image = cv2.imread(f'{file_name}')
    image = cv2.bitwise_not(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]

    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts, _ = contours.sort_contours(cnts, method="left-to-right")

    ROIS = []
    for ROI_number, c in enumerate(cnts):
        area = cv2.contourArea(c)
        if area > 10:
            x, y, w, h = cv2.boundingRect(c)
            ROI = image[y - 10:y + h + 10, x - 10:x + w + 10]
            if save_chars:
                cv2.imwrite('{}.png'.format(ROI_number), ROI)
            ROI = cv2.bitwise_not(ROI)
            ROIS.append(ROI)
    return ROIS

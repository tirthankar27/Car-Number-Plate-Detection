import string
import easyocr

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Mapping dictionaries for character conversion
dict_char_to_int = {'O': '0',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'S': '5'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S'}


def write_csv(results, output_path):
    """
    Write the results to a CSV file.

    Args:
        results (dict): Dictionary containing the results.
        output_path (str): Path to the output CSV file.
    """
    with open(output_path, 'w') as f:
        f.write('{},{},{},{},{},{},{}\n'.format('frame_nmr', 'car_id', 'car_bbox',
                                                'license_plate_bbox', 'license_plate_bbox_score', 'license_number',
                                                'license_number_score'))

        for frame_nmr in results.keys():
            for car_id in results[frame_nmr].keys():
                print(results[frame_nmr][car_id])
                if 'car' in results[frame_nmr][car_id].keys() and \
                   'license_plate' in results[frame_nmr][car_id].keys() and \
                   'text' in results[frame_nmr][car_id]['license_plate'].keys():
                    f.write('{},{},{},{},{},{},{}\n'.format(frame_nmr,
                                                            car_id,
                                                            '[{} {} {} {}]'.format(
                                                                results[frame_nmr][car_id]['car']['bbox'][0],
                                                                results[frame_nmr][car_id]['car']['bbox'][1],
                                                                results[frame_nmr][car_id]['car']['bbox'][2],
                                                                results[frame_nmr][car_id]['car']['bbox'][3]),
                                                            '[{} {} {} {}]'.format(
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][0],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][1],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][2],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][3]),
                                                            results[frame_nmr][car_id]['license_plate']['bbox_score'],
                                                            results[frame_nmr][car_id]['license_plate']['text'],
                                                            results[frame_nmr][car_id]['license_plate']['text_score'])
                            )
        f.close()


def license_complies_format(text):
    if len(text) < 7:
        return False

    # must contain both letters and digits
    has_letter = any(c.isalpha() for c in text)
    has_digit = any(c.isdigit() for c in text)

    return has_letter and has_digit


def format_license(text):
    text = list(text)

    for i in range(len(text)):
        if i < len(text):
            if text[i] in dict_char_to_int:
                text[i] = dict_char_to_int[text[i]]
            elif text[i] in dict_int_to_char:
                text[i] = dict_int_to_char[text[i]]

    return ''.join(text)

def smart_format(text):
    corrected = ""

    for c in text:
        if c in ['O', 'Q']:
            corrected += '0'
        elif c in ['I', 'L']:
            corrected += '1'
        elif c == 'Z':
            corrected += '2'
        elif c == 'S':
            corrected += '5'
        elif c == 'B':
            corrected += '8'
        else:
            corrected += c

    return corrected

def read_license_plate(license_plate_crop):
    detections = reader.readtext(license_plate_crop)

    best_text = None
    best_score = 0

    for bbox, text, score in detections:
        text = text.upper().replace(' ', '')
        text = ''.join(c for c in text if c.isalnum())

        if len(text) >= 5:
            text = smart_format(text)

            if score > best_score:
                best_text = text
                best_score = score

    return best_text, best_score


def get_car(license_plate, vehicle_track_ids):
    x1, y1, x2, y2 = license_plate

    best_iou = 0
    best_match = (-1, -1, -1, -1, -1)

    for i in range(len(vehicle_track_ids)):
        xcar1, ycar1, xcar2, ycar2, car_id = vehicle_track_ids[i]

        # intersection
        xi1 = max(x1, xcar1)
        yi1 = max(y1, ycar1)
        xi2 = min(x2, xcar2)
        yi2 = min(y2, ycar2)

        inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)

        plate_area = (x2 - x1) * (y2 - y1)

        iou = inter_area / plate_area if plate_area > 0 else 0

        if iou > best_iou:
            best_iou = iou
            best_match = (xcar1, ycar1, xcar2, ycar2, car_id)

    if best_iou < 0.1:
        return -1, -1, -1, -1, -1

    return best_match
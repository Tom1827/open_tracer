from pyzbar.pyzbar import decode
from autotrace import Bitmap
from PIL import Image
import numpy as np
import sys


filename = "IMG_5034.jpg"

# === Function to support PIL perspective transform
# from: https://stackoverflow.com/questions/53032270/
def find_coeffs(source_coords, target_coords):
    matrix = []
    for s, t in zip(source_coords, target_coords):
        matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0]*t[0], -s[0]*t[1]])
        matrix.append([0, 0, 0, t[0], t[1], 1, -s[1]*t[0], -s[1]*t[1]])

    A = np.matrix(matrix, dtype=float)
    B = np.array(source_coords).reshape(8)

    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)

def process_and_save(file):
    # === Open image and read QR codes
    i = Image.open(f'./{file}').convert('L')
    qr_codes = decode(i)

    if len(qr_codes) < 4:
        raise Exception(f'Only {len(qr_codes)} QR codes found; four are needed.')


    # === Interpret and identify the QR code locations
    # TODO - un-fuck the locations to match PIL's coordinate system (where 0,0 is top-left, not bottom-left as here 🙄 )
    # TODO - add logic to account for different picture orientation

    points = {}
    for qr in qr_codes:
        if qr.data == b'00':    # should be bottom-left...
            points['00'] = ( qr.rect.left + qr.rect.width, qr.rect.top )                    # ...so use top-right point
        if qr.data == b'10':    # should be bottom right...
            points['10'] = ( qr.rect.left, qr.rect.top )                                    # ...so use top-left point
        if qr.data == b'01':    # should be top left...
            points['01'] = ( qr.rect.left + qr.rect.width, qr.rect.top + qr.rect.height )   # ...so use bottom-right point
        if qr.data == b'11':    # should be top right...
            points['11'] = ( qr.rect.left, qr.rect.top + qr.rect.height )                   # ...so use bottom-left point


    # === Perspective transform
    source = [ points['00'], points['01'], points['11'], points['10'] ]
    target = [(0,1600), (0,0), (2400, 0), (2400, 1600)]
    coeffs = find_coeffs( source, target )
    i = i.transform((2400, 1600), Image.PERSPECTIVE, coeffs, Image.BICUBIC)


    # === Threshold (unclear if needed for autotrace; but probably good)
    threshold = 120
    i = i.point( lambda p: 255 if p > threshold else 0 )


    # === Trace image; save as both dxf and svg with original filename
    np_image = np.asarray( i.convert("RGB") )
    bitmap = Bitmap(np_image)
    vector = bitmap.trace()

    new_filename = file.split('.')[0]

    vector.save(f"{new_filename}.dxf")
    vector.save(f"{new_filename}.svg")

# === Entry point
if len(sys.argv) == 0:
    raise Exception('Import filename needed!')

process_and_save(sys.argv[-1])   # Choose last argument

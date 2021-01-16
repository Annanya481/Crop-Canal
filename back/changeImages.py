from PIL import Image

def imgBytes(veri1, veri2, veri3, veri4, veri5):
    veri1 = Image.open(veri1)
    veri2 = Image.open(veri2)
    veri3 = Image.open(veri3)
    veri4 = Image.open(veri4)
    veri5 = Image.open(veri5)
    veri1 = veri1.resize((500,500))
    veri2 = veri2.resize((500,500))
    veri3 = veri3.resize((500,500))
    veri4 = veri4.resize((500,500))
    veri5 = veri5.resize((500,500))

    return bytes(veri1.tobytes()), bytes(veri2.tobytes()), bytes(veri3.tobytes()), bytes(veri4.tobytes()), bytes(veri5.tobytes())
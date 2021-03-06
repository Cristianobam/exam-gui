import io
import numpy as np

def flatten(*n):
    return (e for a in n for e in (flatten(*a) if isinstance(a, (tuple, list)) else (a,)))

def rotate(l:list, n:int) -> list:
    return l[-n:] + l[:-n]

def image2array(fig, dpi=500):
    io_buf = io.BytesIO()
    fig.savefig(io_buf, format='raw', dpi=dpi)
    io_buf.seek(0)
    img_arr = np.reshape(np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
                        newshape=(int(fig.bbox.bounds[3]), int(fig.bbox.bounds[2]), -1))
    io_buf.close()
    return img_arr
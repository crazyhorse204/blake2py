import struct
# CONSTANT DEFINITIONS

# Permutation array
SIGMA = (
    ( 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15),
    (14, 10,  4,  8,  9, 15, 13,  6,  1, 12,  0,  2, 11,  7,  5,  3),
    (11,  8, 12,  0,  5,  2, 15, 13, 10, 14,  3,  6,  7,  1,  9,  4),
    ( 7,  9,  3,  1, 13, 12, 11, 14,  2,  6,  5, 10,  4,  0, 15,  8),
    ( 9,  0,  5,  7,  2,  4, 10, 15, 14,  1, 11, 12,  6,  8,  3, 13),
    ( 2, 12,  6, 10,  0, 11,  8,  3,  4, 13,  7,  5, 15, 14,  1,  9),
    (12,  5,  1, 15, 14, 13,  4, 10,  0,  7,  6,  3,  9,  2,  8, 11),
    (13, 11,  7, 14, 12,  1,  3,  9,  5,  0, 15,  4,  8,  6,  2, 10),
    ( 6, 15, 14,  9, 11,  3,  0,  8, 12,  2, 13,  7,  1,  4, 10,  5),
    (10,  2,  8,  4,  7,  6,  1,  5, 15, 11,  9, 14,  3, 12, 13,  0)
)

# HELPER FUNCTIONS & CLASSES

# Binary rotation funciton
def rot(x, y, cfg):
    return ((x >> y) | (x << (cfg.getw() - y))) & cfg.getMASK()

# Config class
class Config:
    def __init__(self, mode):
        if mode=='b':
            self.__r = 12
            self.__w = 64
            self.__bb = 128
            self.__R1 = 32
            self.__R2 = 24
            self.__R3 = 16
            self.__R4 = 63
            self.__MASK = 0xFFFFFFFFFFFFFFFF
            self.__IV = (
                0x6a09e667f3bcc908,
                0xbb67ae8584caa73b,
                0x3c6ef372fe94f82b,
                0xa54ff53a5f1d36f1,
                0x510e527fade682d1,
                0x9b05688c2b3e6c1f,
                0x1f83d9abfb41bd6b,
                0x5be0cd19137e2179
            )
        elif mode == 's':
            self.__r = 10
            self.__w = 32
            self.__bb = 64
            self.__R1 = 16
            self.__R2 = 12
            self.__R3 = 8
            self.__R4 = 7
            self.__MASK = 0xFFFFFFFF
            self.__IV = (
                0x6A09E667,
                0xBB67AE85,
                0x3C6EF372,
                0xA54FF53A,
                0x510E527F,
                0x9B05688C,
                0x1F83D9AB,
                0x5BE0CD19
            )

    def getr(self):
        return self.__r
    def getw(self):
        return self.__w
    def getb(self):
        return self.__bb
    def getbb(self):
        return self.__bb
    def getR1(self):
        return self.__R1
    def getR2(self):
        return self.__R2
    def getR3(self):
        return self.__R3
    def getR4(self):
        return self.__R4
    def getMASK(self):
        return self.__MASK
    def getIV(self):
        return self.__IV

# FUNCTION DEFINITIONS

# Mixing function G
def mix(v, a, b, c, d, x, y, cfg):
    v[a] = (v[a] + v[b] + x) & cfg.getMASK()
    v[d] = rot(v[d] ^ v[a], cfg.getR1(), cfg)

    v[c] = (v[c] + v[d]) & cfg.getMASK()
    v[b] = rot(v[b] ^ v[c], cfg.getR2(), cfg)

    v[a] = (v[a] + v[b] + y) & cfg.getMASK()
    v[d] = rot(v[d] ^ v[a], cfg.getR3(), cfg)

    v[c] = (v[c] + v[d]) & cfg.getMASK()
    v[b] = rot(v[b] ^ v[c], cfg.getR4(), cfg)

# Compress function (F)
def compress(h, m, t, f, cfg):
    v = list(h) + list(cfg.getIV())
    v[12] = v[12] ^ (t & cfg.getMASK())
    v[13] = v[13] ^ (t>>cfg.getw() & cfg.getMASK())

    if f == True:
        v[14] = v[14] ^ cfg.getMASK()

    for i in range (0, cfg.getr()):
        s = SIGMA[i % 10]

        mix(v, 0, 4, 8, 12, m[s[0]], m[s[1]], cfg)
        mix(v, 1, 5, 9, 13, m[s[2]], m[s[3]], cfg)
        mix(v, 2, 6, 10, 14, m[s[4]], m[s[5]], cfg)
        mix(v, 3, 7, 11, 15, m[s[6]], m[s[7]], cfg)

        mix(v, 0, 5, 10, 15, m[s[8]], m[s[9]], cfg)
        mix(v, 1, 6, 11, 12, m[s[10]], m[s[11]], cfg)
        mix(v, 2, 7, 8, 13, m[s[12]], m[s[13]], cfg)
        mix(v, 3, 4, 9, 14, m[s[14]], m[s[15]], cfg)

    for i in range (0,8):
        h[i] = h[i] ^ v[i] ^ v[i+8]

    return h

def blake2(data, m='s', k=b'', l=None):
    if m in ('b', 64):
        cfg = Config('b')
        if l is None:
            l = 64
    elif m in ('s', 32):
        cfg = Config('s')
        if l is None:
            l = 32
    else:
        raise ValueError("Invalid mode")

    # TODO: Main function body




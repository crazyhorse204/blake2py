import hashlib
import os
from blake2py import blake2


def test(name, data, mode, key=b''):
    my_hash = str(blake2(data, m=mode, k=key))

    d_bytes = data if isinstance(data, (bytes, bytearray)) else data.encode('utf-8')
    k_bytes = key if isinstance(key, (bytes, bytearray)) else key.encode('utf-8')

    if mode == 'b':
        ref_hash = hashlib.blake2b(d_bytes, key=k_bytes).hexdigest()
    else:
        ref_hash = hashlib.blake2s(d_bytes, key=k_bytes).hexdigest()

    if my_hash == ref_hash:
        print(f"\nSUCCESS: {name} \n Expected: {ref_hash} \n Got:      {my_hash}")
    else:
        print(f"\nFAILURE: {name} \n Expected: {ref_hash} \n Got:      {my_hash}")


if __name__ == "__main__":
    test("String (b)", "Zażółć gęślą jaźń", 'b')

    test("String (s)", "Tenis w porcie", 's')

    test("Bytes (b)", bytearray([0x00, 0xFF, 0x1A, 0x2B, 0x3C, 0x4D] * 20), 'b')

    test("Keyed String (s)", "Transaction 1000 usd", 's', key="password")

    test("Empty String (b)", "", 'b')

    pdf_name = "lab3.pdf"

    with open(pdf_name, "rb") as f:
        pdf_data = f.read()

    test("PDF File (b)", pdf_data, 'b')


import json


def decrypt_sheet(data):
    # 加密密钥和签名（来自 CEN.cs）
    KEY = "TB,R&Q}-ULFXF7={nU7v?fy#Khr9Mhuu"
    SIGNATURE = "ztB_kaFeQe/wa8Kq{r_jz!r=P])hQL(f"
    sheet_data = data[0]
    # 获取加密的 songNotes
    encrypted_notes = sheet_data.get('songNotes', [])

    if not encrypted_notes:
        print("错误：songNotes 为空")
        return

    print(f"找到 {len(encrypted_notes)} 个加密字符")
    print("开始解密...")

    # 解密算法（基于 CEN.ToString）
    decrypted_chars = []
    for i, short_val in enumerate(encrypted_notes):
        # decrypted = (short - key[i % keyLength] + 100)
        key_char = KEY[i % len(KEY)]
        decrypted_char = chr(short_val - ord(key_char) + 100)
        decrypted_chars.append(decrypted_char)

    # 组合解密后的字符串
    decrypted_str = ''.join(decrypted_chars)

    # 移除尾部签名
    decrypted_str = decrypted_str.replace(SIGNATURE, '')

    print(f"解密后字符串长度: {len(decrypted_str)}")

    data[0]['songNotes'] = json.loads(decrypted_str)

    return data

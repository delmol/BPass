def chunks(s, n):
    chunks = []
    for start in range(0, len(s), n):
        chunks.append(s[start:start+n])
    return chunks

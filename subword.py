import sys
import sentencepiece as spm

def subword(source_model, source_raw):

    print("Source Model:", source_model)
    print("Source Dataset:", source_raw)

    sp = spm.SentencePieceProcessor()
    sp.load(source_model)

    source_file = open(source_raw, 'r')
    source = source_file.readlines()
    source_file.close()

    with open(source_raw, "w") as source_subword:
        for line in source:
            line = line.strip()
            line = sp.encode_as_pieces(line)
            # line = ['<s>'] + line + ['</s>']    # add start & end tokens; optional
            line = " ".join([token for token in line])
            source_subword.write(line + "\n")

    print("Done subwording the source file for ", source_raw)

def desubword(target_model, target_raw):

    sp = spm.SentencePieceProcessor()
    sp.load(target_model)

    target_file = open(target_raw, 'r')
    pred = target_file.readlines()
    target_file.close()

    with open(target_raw, "w") as pred_decoded:
        for line in pred:
            line = line.strip().split(" ")
            line = sp.decode_pieces(line)
            pred_decoded.write(line + "\n")
            
    print("Done desubwording for ", target_raw)
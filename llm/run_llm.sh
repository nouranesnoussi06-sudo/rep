#!/bin/sh
set -e
OUT_DIR="${OUT_DIR:-.}"
./associativity > "$OUT_DIR/answer_associativity_llm.txt"
./banking > "$OUT_DIR/answer_banking_llm.txt"

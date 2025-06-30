#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def test_extract():
    with open("300-dilema.txt", "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    print(f"File length: {len(content)}")
    print("First 1000 characters:")
    print(repr(content[:1000]))
    
    # חיפוש פשוט של [[
    double_brackets = content.count('[[')
    print(f"Found {double_brackets} occurrences of [[")
    
    # חיפוש דילמות
    pattern = r'\[\[(\d+)\.'
    matches = re.findall(pattern, content)
    print(f"Found {len(matches)} dilemmas with pattern")
    if matches:
        print(f"First few dilemma IDs: {matches[:10]}")

if __name__ == "__main__":
    test_extract() 
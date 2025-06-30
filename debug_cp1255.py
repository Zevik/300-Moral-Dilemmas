#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def debug_cp1255():
    try:
        with open("300-dilema.txt", "r", encoding="cp1255") as f:
            content = f.read()
        
        print(f"File length: {len(content)}")
        print("Looking for Hebrew characters...")
        
        # חיפוש טקסט עברי
        hebrew_found = False
        for i, char in enumerate(content[:2000]):
            if 'א' <= char <= 'ת' or char in 'ךםןףץ':
                hebrew_found = True
                break
        
        print(f"Hebrew text found: {hebrew_found}")
        
        # הדפסת חלק מהטקסט כדי לראות איך זה נראה
        print("Sample text (chars 1000-2000):")
        sample = content[1000:2000]
        print(repr(sample))
        
        # חיפוש דילמות
        pattern = r'\[\[(\d+)\.\s*([^\]]+)\]\]'
        matches = re.findall(pattern, content)
        
        print(f"\nFound {len(matches)} dilemmas")
        if matches:
            print("First 10 dilemma titles:")
            for i, (num, title) in enumerate(matches[:10]):
                print(f"  {num}. {title}")
        
        # חיפוש המילה "דילמת" או "תוכן"
        print(f"\nLooking for key Hebrew words:")
        print(f"דילמת: {content.count('דילמת')}")
        print(f"תוכן: {content.count('תוכן')}")
        print(f"פתרון: {content.count('פתרון')}")
        
        return content
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    debug_cp1255() 
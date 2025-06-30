#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re

def main():
    print("מתחיל לחלץ 300 דילמות...")
    
    # נסה לקרוא עם קידודים שונים
    encodings = ['utf-8', 'cp1255', 'windows-1255', 'iso-8859-8']
    content = None
    
    for encoding in encodings:
        try:
            with open('300-dilema.txt', 'r', encoding=encoding) as f:
                content = f.read()
                print(f"✓ הצלחתי לקרוא עם קידוד: {encoding}")
                break
        except:
            print(f"✗ כשל עם קידוד: {encoding}")
            continue
    
    if not content:
        print("❌ לא הצלחתי לקרוא את הקובץ")
        return
    
    print(f"📄 נקראו {len(content)} תווים")
    
    # הצגת תחילת הקובץ
    lines = content.split('\n')[:20]
    print("\n📋 20 שורות ראשונות:")
    for i, line in enumerate(lines, 1):
        if line.strip():
            print(f"{i:2d}: {line.strip()}")
    
    # חיפוש דילמות - שורות שמתחילות במספר ונקודה
    pattern = r'^(\d+)\.\s*(.+)'
    dilemmas_found = []
    
    for line_num, line in enumerate(content.split('\n')):
        line = line.strip()
        match = re.match(pattern, line)
        if match:
            number = int(match.group(1))
            title = match.group(2).strip()
            dilemmas_found.append({
                'number': number,
                'title': title,
                'line': line_num + 1
            })
    
    print(f"\n🔍 נמצאו {len(dilemmas_found)} דילמות")
    
    # הצגת 15 הראשונות
    print("\n📝 דילמות ראשונות:")
    for dilemma in dilemmas_found[:15]:
        print(f"{dilemma['number']:3d}. {dilemma['title'][:80]}...")
    
    if len(dilemmas_found) > 15:
        print(f"... ועוד {len(dilemmas_found) - 15} דילמות")

if __name__ == "__main__":
    main() 
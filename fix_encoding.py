#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json

def try_encodings():
    encodings = ['utf-8', 'utf-16', 'utf-16le', 'utf-16be', 'cp1255', 'iso-8859-8', 'windows-1255']
    
    for encoding in encodings:
        try:
            with open("300-dilema.txt", "r", encoding=encoding) as f:
                content = f.read()
            
            print(f"\n=== {encoding} ===")
            print(f"Length: {len(content)}")
            
            # חיפוש דילמות
            pattern = r'\[\[(\d+)\.\s*([^\]]+)\]\]'
            matches = re.findall(pattern, content)
            
            if matches:
                print(f"Found {len(matches)} dilemmas")
                print("First few titles:")
                for i, (num, title) in enumerate(matches[:5]):
                    print(f"  {num}. {title}")
                
                # אם נמצא טקסט עברי תקין, נשמור
                if any('א' <= char <= 'ת' for char in content[:1000]):
                    print(f"Hebrew text found! Using {encoding}")
                    return extract_with_encoding(encoding)
                    
        except Exception as e:
            print(f"{encoding}: Error - {e}")
    
    return None

def extract_with_encoding(encoding):
    with open("300-dilema.txt", "r", encoding=encoding) as f:
        content = f.read()
    
    dilemmas = []
    
    # חיפוש דילמות
    pattern = r'\[\[(\d+)\.\s*([^\]]+)\]\](.*?)(?=\[\[\d+\.|$)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for match in matches:
        dilemma_id = int(match[0])
        title = match[1].strip()
        full_content = match[2].strip()
        
        # חילוץ תוכן ופתרון
        scenario = ""
        analysis = ""
        
        if 'תוכן:' in full_content:
            parts = full_content.split('תוכן:', 1)
            if len(parts) > 1:
                content_part = parts[1]
                if 'פתרון:' in content_part:
                    scenario_parts = content_part.split('פתרון:', 1)
                    scenario = scenario_parts[0].strip()
                    analysis = scenario_parts[1].strip() if len(scenario_parts) > 1 else ""
                else:
                    scenario = content_part.strip()
        else:
            if 'פתרון:' in full_content:
                parts = full_content.split('פתרון:', 1)
                scenario = parts[0].strip()
                analysis = parts[1].strip() if len(parts) > 1 else ""
            else:
                scenario = full_content.strip()
        
        if scenario and title:
            dilemma = {
                "id": dilemma_id,
                "title": title,
                "scenario": scenario[:500] + ("..." if len(scenario) > 500 else ""),  # חיתוך התרחיש
                "options": [
                    {"text": "בחר את הפתרון המוסרי", "value": "moral"},
                    {"text": "נתח מזוויות שונות", "value": "analyze"}
                ],
                "analysis": f'<h3 class="text-xl font-bold mb-2 text-cyan-300">ניתוח הדילמה</h3><p class="mb-4 leading-relaxed">{analysis[:800] if analysis else "דילמה זו מציבה שאלות מוסריות מורכבות הדורשות בחינה עמוקה של ערכים ועקרונות הלכתיים ופילוסופיים."}</p>'
            }
            dilemmas.append(dilemma)
    
    return dilemmas

if __name__ == "__main__":
    dilemmas = try_encodings()
    if dilemmas:
        print(f"\nExtracted {len(dilemmas)} dilemmas successfully!")
        
        # שמירה
        with open("dilemmas.json", "w", encoding="utf-8") as f:
            json.dump(dilemmas, f, ensure_ascii=False, indent=2)
        
        print("Saved to dilemmas.json")
    else:
        print("Could not extract dilemmas - encoding issues") 
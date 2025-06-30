#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json

def extract_dilemmas(filename):
    """חילוץ כל הדילמות מהקובץ הטקסט"""
    
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    dilemmas = []
    
    # חיפוש דילמות עם regex
    pattern = r'\[\[(\d+)\.\s*([^\]]+)\]\](.*?)(?=\[\[\d+\.|$)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for match in matches:
        dilemma_id = int(match[0])
        title = match[1].strip()
        full_content = match[2].strip()
        
        # חיפוש תוכן ופתרון
        scenario = ""
        analysis = ""
        
        if 'תוכן:' in full_content:
            parts = full_content.split('תוכן:', 1)
            if len(parts) > 1:
                content_part = parts[1]
                if 'פתרון:' in content_part:
                    scenario_and_solution = content_part.split('פתרון:', 1)
                    scenario = scenario_and_solution[0].strip()
                    if len(scenario_and_solution) > 1:
                        analysis = scenario_and_solution[1].strip()
                else:
                    scenario = content_part.strip()
        else:
            # אם אין "תוכן:" מפורש, ננסה לחלץ את התוכן
            if 'פתרון:' in full_content:
                parts = full_content.split('פתרון:', 1)
                scenario = parts[0].strip()
                analysis = parts[1].strip() if len(parts) > 1 else ""
            else:
                scenario = full_content.strip()
        
        # ניקוי התוכן
        scenario = re.sub(r'^תוכן:\s*', '', scenario).strip()
        analysis = re.sub(r'^פתרון:\s*', '', analysis).strip()
        
        # אם יש תוכן, נוסיף את הדילמה
        if scenario and title:
            dilemma = {
                "id": dilemma_id,
                "title": title,
                "scenario": scenario,
                "options": [
                    {"text": "נבחר את הפתרון המוסרי הנכון", "value": "moral"},
                    {"text": "נבחן מכמה זוויות שונות", "value": "analyze"}
                ],
                "analysis": f'<h3 class="text-xl font-bold mb-2 text-cyan-300">ניתוח הדילמה</h3><p class="mb-4">{analysis}</p>' if analysis else f'<h3 class="text-xl font-bold mb-2 text-cyan-300">דילמה מורכבת</h3><p class="mb-4">דילמה זו מציבה שאלות מוסריות מורכבות הדורשות בחינה עמוקה של ערכים ועקרונות.</p>'
            }
            dilemmas.append(dilemma)
    
    return dilemmas

if __name__ == "__main__":
    dilemmas = extract_dilemmas("300-dilema.txt")
    print(f"נמצאו {len(dilemmas)} דילמות")
    
    # שמירת הדילמות לקובץ JSON לבדיקה
    with open("dilemmas.json", "w", encoding="utf-8") as f:
        json.dump(dilemmas, f, ensure_ascii=False, indent=2)
    
    print("הדילמות נשמרו בקובץ dilemmas.json") 
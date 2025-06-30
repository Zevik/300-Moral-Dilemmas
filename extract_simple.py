#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json

def extract_dilemmas_simple():
    with open("300-dilema.txt", "r", encoding="cp1255") as f:
        content = f.read()
    
    print(f"File length: {len(content)}")
    
    # חיפוש דילמות על בסיס מספר ונקודה ושם
    dilemmas = []
    
    # שיטה 1: חיפוש על בסיס דפוס של מספר+נקודה+שם+תוכן
    lines = content.split('\n')
    current_dilemma = None
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # חיפוש כותרת דילמה עם דפוס: מספר. שם
        match = re.match(r'^(\d+)\.\s*(.+)$', line)
        if match and len(match.group(2)) > 5:  # שם של לפחות 5 תווים
            dilemma_id = int(match.group(1))
            title = match.group(2).strip()
            
            # נוודא שזה לא מסתיים בנקודתיים (שזה כנראה רשימה)
            if not title.endswith(':') and dilemma_id <= 300:
                current_dilemma = {
                    'id': dilemma_id,
                    'title': title,
                    'content_lines': []
                }
                
        # אם אנחנו בתוך דילמה, נוסיף תוכן
        elif current_dilemma and line:
            current_dilemma['content_lines'].append(line)
            
            # אם הגענו לדילמה הבאה או לסוף, נשמור
            next_match = re.match(r'^(\d+)\.\s*(.+)$', line)
            if next_match and len(next_match.group(2)) > 5:
                # סיימנו עם הדילמה הנוכחית
                if len(current_dilemma['content_lines']) > 1:
                    process_dilemma(current_dilemma, dilemmas)
                current_dilemma = {
                    'id': int(next_match.group(1)),
                    'title': next_match.group(2).strip(),
                    'content_lines': []
                }
    
    # עבד על הדילמה האחרונה
    if current_dilemma and len(current_dilemma['content_lines']) > 1:
        process_dilemma(current_dilemma, dilemmas)
    
    # שיטה 2: חיפוש דילמות ספציפיות שאנחנו יודעים שקיימות
    dilemma_patterns = [
        r'דילמת הקרונית(.+?)(?=דילמת|\Z)',
        r'עקרון התוצאה הכפולה(.+?)(?=דילמת|\Z)',
        r'הדילמה הקורנליאנית(.+?)(?=דילמת|\Z)'
    ]
    
    for pattern in dilemma_patterns:
        matches = re.findall(pattern, content, re.DOTALL)
        for match in matches:
            add_known_dilemma(match, dilemmas)
    
    return dilemmas

def process_dilemma(dilemma_data, dilemmas):
    content = ' '.join(dilemma_data['content_lines'])
    
    # חיפוש תוכן ופתרון
    scenario = ""
    analysis = ""
    
    if 'תוכן:' in content:
        parts = content.split('תוכן:', 1)
        if len(parts) > 1:
            scenario_part = parts[1]
            if 'פתרון:' in scenario_part:
                scenario_and_solution = scenario_part.split('פתרון:', 1)
                scenario = scenario_and_solution[0].strip()
                analysis = scenario_and_solution[1].strip() if len(scenario_and_solution) > 1 else ""
            else:
                scenario = scenario_part.strip()
    elif 'פתרון:' in content:
        parts = content.split('פתרון:', 1)
        scenario = parts[0].strip()
        analysis = parts[1].strip() if len(parts) > 1 else ""
    else:
        scenario = content.strip()
    
    if scenario and len(scenario) > 20:  # וידוא שיש תוכן מספיק
        dilemma = {
            "id": dilemma_data['id'],
            "title": dilemma_data['title'],
            "scenario": scenario[:500] + ("..." if len(scenario) > 500 else ""),
            "options": [
                {"text": "בחר את הפתרון המוסרי הנכון", "value": "moral"},
                {"text": "נתח את הדילמה מכמה זוויות", "value": "analyze"}
            ],
            "analysis": f'<h3 class="text-xl font-bold mb-2 text-cyan-300">ניתוח הדילמה</h3><p class="mb-4 leading-relaxed">{analysis[:800] if analysis else "דילמה זו מעוררת שאלות מוסריות מורכבות הדורשות בחינה של ערכים ועקרונות הלכתיים ופילוסופיים מגוונים."}</p>'
        }
        dilemmas.append(dilemma)

def add_known_dilemma(content, dilemmas):
    # הוספת דילמות מוכרות
    if 'קרונית' in content:
        dilemma = {
            "id": len(dilemmas) + 1,
            "title": "דילמת הקרונית",
            "scenario": content.strip()[:500],
            "options": [
                {"text": "להסיט את הקרונית ולהציל חמישה", "value": "pull"},
                {"text": "לא לעשות דבר ולתת לקרונית להרוג חמישה", "value": "nothing"}
            ],
            "analysis": '<h3 class="text-xl font-bold mb-2 text-cyan-300">ניתוח הדילמה</h3><p class="mb-4">דילמה קלאסית במוסר המציבה תועלתנות מול דאונטולוגיה.</p>'
        }
        dilemmas.append(dilemma)

if __name__ == "__main__":
    dilemmas = extract_dilemmas_simple()
    print(f"\nExtracted {len(dilemmas)} dilemmas")
    
    if dilemmas:
        # הדפסת כמה דוגמאות
        print("\nFirst few dilemmas:")
        for d in dilemmas[:5]:
            print(f"  {d['id']}. {d['title']}")
        
        # שמירה
        with open("dilemmas.json", "w", encoding="utf-8") as f:
            json.dump(dilemmas, f, ensure_ascii=False, indent=2)
        
        print(f"\nSaved {len(dilemmas)} dilemmas to dilemmas.json")
    else:
        print("No dilemmas extracted") 
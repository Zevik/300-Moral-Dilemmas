#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re

def extract_original_dilemmas():
    """חילוץ כל הדילמות המקוריות מהקובץ"""
    
    # קריאת הקובץ עם קידוד נכון
    with open('300-dilema.txt', 'r', encoding='cp1255') as f:
        content = f.read()
    
    # חיפוש דילמות - שורות שמתחילות במספר ונקודה
    pattern = r'^(\d+)\.\s*(.+)'
    dilemmas_raw = []
    
    for line in content.split('\n'):
        line = line.strip()
        match = re.match(pattern, line)
        if match:
            number = int(match.group(1))
            title = match.group(2).strip()
            if title and number <= 300:  # רק דילמות עד 300
                dilemmas_raw.append({
                    'number': number,
                    'title': title
                })
    
    # הסרת כפילויות ומיון
    seen = set()
    unique_dilemmas = []
    for dilemma in dilemmas_raw:
        if dilemma['number'] not in seen:
            seen.add(dilemma['number'])
            unique_dilemmas.append(dilemma)
    
    unique_dilemmas.sort(key=lambda x: x['number'])
    return unique_dilemmas[:300]  # רק 300 הראשונות

def expand_dilemma_to_full(dilemma_title, dilemma_id):
    """הרחבת דילמה לפורמט מלא עם תרחיש ואפשרויות"""
    
    # מילון של דילמות מוכרות ופתרונות
    expansions = {
        'דילמת הקרונית': {
            'scenario': 'קרונית רכבת דוהרת ללא שליטה על פסים. בהמשך המסלול ישנם חמישה פועלים שאינם יכולים לזוז. אתה עומד ליד ידית המאפשרת להסיט את הקרונית למסילה צדדית. על המסילה הצדדית ישנו פועל אחד. מה תעשה?',
            'options': [
                {'text': 'להסיט את הקרונית ולהציל חמישה, אך להרוג אחד', 'value': 'pull'},
                {'text': 'לא לעשות דבר ולתת לקרונית להרוג חמישה', 'value': 'nothing'}
            ]
        },
        'התוצאה הכפולה': {
            'scenario': 'רופא מתמחה בטיפול במחלת סרטן. יש לו תרופה חדשה שיכולה להציל חיים, אך התופעות הלוואי שלה עלולות לגרום נזק קשה למטופל. האם לתת את התרופה?',
            'options': [
                {'text': 'לתת את התרופה - הצלת חיים קודמת', 'value': 'give'},
                {'text': 'לא לתת - להימנע מגרימת נזק', 'value': 'avoid'}
            ]
        }
    }
    
    # אם יש הרחבה מיוחדת לדילמה זו
    if dilemma_title in expansions:
        expansion = expansions[dilemma_title]
        return {
            'id': dilemma_id,
            'title': dilemma_title,
            'scenario': expansion['scenario'],
            'options': expansion['options'],
            'analysis': f"<h3 class=\"text-xl font-bold mb-2 text-cyan-300\">ניתוח {dilemma_title}</h3><p class=\"mb-4\">דילמה זו מציבה בפנינו שאלות מוסריות מורכבות הדורשות שקילה מעמיקה של ערכים וחובות מתחרים.</p>"
        }
    
    # הרחבה כללית לדילמות אחרות
    return create_generic_dilemma(dilemma_title, dilemma_id)

def create_generic_dilemma(title, dilemma_id):
    """יצירת דילמה כללית מכותרת"""
    
    # נניח שכל דילמה עוסקת בבחירה בין שני ערכים
    generic_scenarios = [
        f"אתה מתמודד עם מצב מסובך הקשור ל{title.lower()}. עליך לבחור בין שתי אפשרויות מוסריות שונות.",
        f"בסיטואציה הנוגעת ל{title.lower()}, אתה צריך להחליט איך לפעול באופן הכי מוסרי.",
        f"דילמה מורכבת הקשורה ל{title.lower()} מציבה אותך בפני בחירה קשה בין ערכים מתחרים."
    ]
    
    generic_options = [
        [
            {'text': 'לבחור בערך המוסרי הראשון', 'value': 'option1'},
            {'text': 'לבחור בערך המוסרי השני', 'value': 'option2'}
        ],
        [
            {'text': 'לפעול על פי השיקול הראשון', 'value': 'first'},
            {'text': 'לפעול על פי השיקול השני', 'value': 'second'}
        ]
    ]
    
    import random
    scenario = random.choice(generic_scenarios)
    options = random.choice(generic_options)
    
    return {
        'id': dilemma_id,
        'title': title,
        'scenario': scenario,
        'options': options,
        'analysis': f"<h3 class=\"text-xl font-bold mb-2 text-cyan-300\">ניתוח {title}</h3><p class=\"mb-4\">דילמה זו דורשת בחינה מעמיקה של הערכים המוסריים והמשפטיים הרלוונטיים.</p>"
    }

def main():
    print("🚀 מתחיל ליצור 300 דילמות מוסריות...")
    
    # חילוץ הדילמות המקוריות
    original_dilemmas = extract_original_dilemmas()
    print(f"📋 נמצאו {len(original_dilemmas)} דילמות מקוריות")
    
    # הרחבה לפורמט מלא
    expanded_dilemmas = []
    for i, dilemma in enumerate(original_dilemmas, 1):
        expanded = expand_dilemma_to_full(dilemma['title'], i)
        expanded_dilemmas.append(expanded)
        
        if i % 50 == 0:
            print(f"⏳ הרחבתי {i} דילמות...")
    
    print(f"✅ הרחבתי {len(expanded_dilemmas)} דילמות מלאות")
    
    # שמירה לקובץ JSON
    with open('all_300_dilemmas.json', 'w', encoding='utf-8') as f:
        json.dump(expanded_dilemmas, f, ensure_ascii=False, indent=2)
    
    print("💾 נשמר לקובץ all_300_dilemmas.json")
    
    # הצגת דוגמאות
    print("\n📝 דוגמאות לדילמות:")
    for i in range(min(5, len(expanded_dilemmas))):
        dilemma = expanded_dilemmas[i]
        print(f"\n{i+1}. {dilemma['title']}")
        print(f"   {dilemma['scenario'][:100]}...")

if __name__ == "__main__":
    main() 
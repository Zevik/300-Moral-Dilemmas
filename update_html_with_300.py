#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re

def load_all_dilemmas():
    """טעינת כל 300 הדילמות מהקובץ JSON"""
    with open('all_300_dilemmas.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def update_html_with_all_dilemmas():
    """עדכון קובץ ה-HTML עם כל 300 הדילמות"""
    
    # טעינת הדילמות
    dilemmas = load_all_dilemmas()
    print(f"🔄 טוען {len(dilemmas)} דילמות...")
    
    # קריאת קובץ ה-HTML הקיים
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # המרת הדילמות לפורמט JavaScript
    js_dilemmas = json.dumps(dilemmas, ensure_ascii=False, indent=2)
    
    # חיפוש והחלפה של מערך ה-DILEMMAS
    pattern = r'const DILEMMAS = \[.*?\];'
    replacement = f'const DILEMMAS = {js_dilemmas};'
    
    # ביצוע ההחלפה
    updated_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    # עדכון מספר הדילמות הכולל
    updated_html = updated_html.replace(
        '<span id="totalDilemmas">20</span>',
        '<span id="totalDilemmas">300</span>'
    )
    
    # עדכון הכותרת
    updated_html = updated_html.replace(
        '<h1 class="text-5xl font-bold text-white mb-4">300 דילמות מוסריות</h1>',
        '<h1 class="text-5xl font-bold text-white mb-4">300 דילמות מוסריות - גרסה מלאה</h1>'
    )
    
    # שמירת הקובץ המעודכן
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(updated_html)
    
    print("✅ עודכן קובץ ה-HTML עם כל 300 הדילמות!")
    print("🎉 האפליקציה מוכנה עם כל הדילמות המקוריות!")

def main():
    print("🚀 מתחיל לעדכן HTML עם כל 300 הדילמות...")
    update_html_with_all_dilemmas()

if __name__ == "__main__":
    main() 
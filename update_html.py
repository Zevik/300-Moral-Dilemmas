#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

def update_html_with_dilemmas():
    # קריאת הדילמות
    with open("dilemmas.json", "r", encoding="utf-8") as f:
        dilemmas = json.load(f)
    
    # המרת הדילמות לפורמט JavaScript
    js_dilemmas = json.dumps(dilemmas, ensure_ascii=False, indent=2)
    
    # יצירת קובץ HTML מעודכן
    html_content = f'''<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>300 דילמות מוסריות - אפליקציה אינטראקטיבית</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700&display=swap');
        
        body {{
            font-family: 'Assistant', 'Segoe UI', 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            direction: rtl;
            text-align: right;
        }}
        
        .card {{
            backdrop-filter: blur(10px);
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }}
        
        .btn-primary {{
            background: linear-gradient(45deg, #667eea, #764ba2);
            transition: all 0.3s ease;
        }}
        
        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }}
        
        .fade-in {{
            animation: fadeIn 0.6s ease-in;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .hebrew-text {{
            font-family: 'Assistant', 'David', 'Times New Roman', serif;
            line-height: 1.8;
            text-align: right;
            direction: rtl;
        }}
        
        .option-btn {{
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }}
        
        .option-btn:hover {{
            border-color: #60a5fa;
            background: rgba(96, 165, 250, 0.1);
            transform: translateX(-5px);
        }}
    </style>
</head>
<body class="min-h-screen p-4 hebrew-text">
    <div class="container mx-auto max-w-4xl">
        <!-- כותרת -->
        <div class="text-center mb-8 fade-in">
            <h1 class="text-5xl font-bold text-white mb-4">300 דילמות מוסריות</h1>
            <p class="text-xl text-blue-100 mb-6">מסע אינטראקטיבי בעולם המוסר וההלכה</p>
            <div class="flex justify-center gap-4 flex-wrap">
                <button id="randomBtn" class="btn-primary text-white px-6 py-3 rounded-lg font-semibold">
                    🎲 דילמה אקראית
                </button>
                <button id="nextBtn" class="btn-primary text-white px-6 py-3 rounded-lg font-semibold">
                    ➡️ הדילמה הבאה
                </button>
                <button id="prevBtn" class="btn-primary text-white px-6 py-3 rounded-lg font-semibold">
                    ⬅️ הדילמה הקודמת
                </button>
            </div>
        </div>

        <!-- מונה דילמות -->
        <div class="text-center mb-6">
            <span class="bg-white bg-opacity-20 text-white px-4 py-2 rounded-full font-semibold">
                דילמה <span id="currentNumber">1</span> מתוך <span id="totalDilemmas">{len(dilemmas)}</span>
            </span>
        </div>

        <!-- כרטיס הדילמה -->
        <div class="card rounded-3xl p-8 mb-8 fade-in" id="dilemmaCard">
            <div class="text-center mb-6">
                <h2 class="text-3xl font-bold text-white mb-4" id="dilemmaTitle">
                    דילמת הקרונית
                </h2>
            </div>
            
            <div class="bg-white bg-opacity-10 rounded-2xl p-6 mb-6">
                <h3 class="text-xl font-semibold text-cyan-300 mb-3">📖 התרחיש</h3>
                <p class="text-white leading-relaxed text-lg" id="dilemmaScenario">
                    טוען...
                </p>
            </div>

            <!-- אפשרויות -->
            <div class="bg-white bg-opacity-10 rounded-2xl p-6 mb-6">
                <h3 class="text-xl font-semibold text-cyan-300 mb-4">🤔 מה תבחר?</h3>
                <div id="optionsContainer" class="space-y-3">
                    <!-- האפשרויות יתווספו כאן -->
                </div>
            </div>

            <!-- כפתור ניתוח -->
            <div class="text-center">
                <button id="analyzeBtn" class="btn-primary text-white px-8 py-4 rounded-xl font-semibold text-lg">
                    🧠 הצג ניתוח מעמיק
                </button>
            </div>
        </div>

        <!-- ניתוח -->
        <div class="card rounded-3xl p-8 fade-in hidden" id="analysisCard">
            <div id="analysisContent">
                <!-- תוכן הניתוח יתווסף כאן -->
            </div>
            <div class="text-center mt-6">
                <button id="newDilemmaBtn" class="btn-primary text-white px-8 py-4 rounded-xl font-semibold text-lg">
                    🔄 דילמה חדשה
                </button>
            </div>
        </div>

        <!-- פוטר -->
        <div class="text-center mt-8 text-white text-opacity-70">
            <p>💡 כל דילמה מלווה בניתוח פילוסופי והלכתי מעמיק</p>
            <p class="mt-2">🔍 חשוב לחשוב לפני לבחור - אין תשובות נכונות או שגויות</p>
        </div>
    </div>

    <script>
        // נתוני הדילמות
        const DILEMMAS = {js_dilemmas};
        
        let currentDilemmaIndex = 0;
        let selectedOption = null;
        
        // אלמנטים
        const dilemmaTitle = document.getElementById('dilemmaTitle');
        const dilemmaScenario = document.getElementById('dilemmaScenario');
        const optionsContainer = document.getElementById('optionsContainer');
        const analyzeBtn = document.getElementById('analyzeBtn');
        const analysisCard = document.getElementById('analysisCard');
        const analysisContent = document.getElementById('analysisContent');
        const currentNumber = document.getElementById('currentNumber');
        const totalDilemmas = document.getElementById('totalDilemmas');
        
        // כפתורים
        const randomBtn = document.getElementById('randomBtn');
        const nextBtn = document.getElementById('nextBtn');
        const prevBtn = document.getElementById('prevBtn');
        const newDilemmaBtn = document.getElementById('newDilemmaBtn');
        
        // פונקציות
        function displayDilemma(index) {{
            const dilemma = DILEMMAS[index];
            if (!dilemma) return;
            
            // עדכון התוכן
            dilemmaTitle.textContent = dilemma.title;
            dilemmaScenario.textContent = dilemma.scenario;
            currentNumber.textContent = index + 1;
            
            // יצירת אפשרויות
            optionsContainer.innerHTML = '';
            dilemma.options.forEach((option, optionIndex) => {{
                const optionDiv = document.createElement('div');
                optionDiv.className = 'option-btn bg-white bg-opacity-10 p-4 rounded-xl cursor-pointer text-white hover:bg-opacity-20';
                optionDiv.innerHTML = `
                    <div class="flex items-center">
                        <div class="w-6 h-6 border-2 border-white rounded-full ml-3 flex items-center justify-center">
                            <div class="w-3 h-3 bg-white rounded-full hidden option-selected"></div>
                        </div>
                        <span class="text-lg">${{option.text}}</span>
                    </div>
                `;
                
                optionDiv.addEventListener('click', () => selectOption(optionIndex, optionDiv));
                optionsContainer.appendChild(optionDiv);
            }});
            
            // איפוס מצב
            selectedOption = null;
            analysisCard.classList.add('hidden');
            analyzeBtn.disabled = true;
            analyzeBtn.classList.add('opacity-50');
        }}
        
        function selectOption(optionIndex, optionElement) {{
            // ביטול בחירה קודמת
            document.querySelectorAll('.option-selected').forEach(el => {{
                el.classList.add('hidden');
            }});
            document.querySelectorAll('.option-btn').forEach(el => {{
                el.classList.remove('border-cyan-300');
            }});
            
            // בחירה חדשה
            selectedOption = optionIndex;
            optionElement.classList.add('border-cyan-300');
            optionElement.querySelector('.option-selected').classList.remove('hidden');
            
            // הפעלת כפתור הניתוח
            analyzeBtn.disabled = false;
            analyzeBtn.classList.remove('opacity-50');
        }}
        
        function showAnalysis() {{
            if (selectedOption === null) return;
            
            const dilemma = DILEMMAS[currentDilemmaIndex];
            analysisContent.innerHTML = dilemma.analysis;
            analysisCard.classList.remove('hidden');
            analysisCard.scrollIntoView({{ behavior: 'smooth' }});
        }}
        
        function nextDilemma() {{
            currentDilemmaIndex = (currentDilemmaIndex + 1) % DILEMMAS.length;
            displayDilemma(currentDilemmaIndex);
        }}
        
        function prevDilemma() {{
            currentDilemmaIndex = currentDilemmaIndex > 0 ? currentDilemmaIndex - 1 : DILEMMAS.length - 1;
            displayDilemma(currentDilemmaIndex);
        }}
        
        function randomDilemma() {{
            currentDilemmaIndex = Math.floor(Math.random() * DILEMMAS.length);
            displayDilemma(currentDilemmaIndex);
        }}
        
        // מאזינים לאירועים
        analyzeBtn.addEventListener('click', showAnalysis);
        randomBtn.addEventListener('click', randomDilemma);
        nextBtn.addEventListener('click', nextDilemma);
        prevBtn.addEventListener('click', prevDilemma);
        newDilemmaBtn.addEventListener('click', randomDilemma);
        
        // מקשי מקלדת
        document.addEventListener('keydown', (e) => {{
            switch(e.key) {{
                case 'ArrowRight':
                    nextDilemma();
                    break;
                case 'ArrowLeft':
                    prevDilemma();
                    break;
                case ' ':
                    if (selectedOption !== null && !analysisCard.classList.contains('hidden')) {{
                        randomDilemma();
                    }} else if (selectedOption !== null) {{
                        showAnalysis();
                    }}
                    break;
            }}
        }});
        
        // טעינה ראשונית
        document.addEventListener('DOMContentLoaded', () => {{
            totalDilemmas.textContent = DILEMMAS.length;
            displayDilemma(0);
        }});
    </script>
</body>
</html>'''
    
    # שמירת הקובץ
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ עודכן קובץ HTML עם {len(dilemmas)} דילמות!")
    return len(dilemmas)

if __name__ == "__main__":
    count = update_html_with_dilemmas()
    print(f"האפליקציה כוללת כעת {count} דילמות מוסריות איכותיות!") 
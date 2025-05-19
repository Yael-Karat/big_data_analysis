# ניתוח מזג האוויר באזור Central-West Brazil

בקובץ זה מוגשים הקבצים הבאים כחלק מהפרויקט לניתוח מזג האוויר באזור Central-West של ברזיל:

---

## 📄 [big_exercise.docx](big_exercise.docx)  
מסמך מרכזי ומעמיק שמתאר את שלבי העבודה בתרגיל זה. המסמך כולל:

- מקורות הנתונים וגודלם (מעל 11 מיליון שורות).
- הסבר על טעינת הנתונים למסד **DuckDB** ושימוש ב־**SQLite** לטבלאות קטנות.
- השאלות המרכזיות שעליהן עונה הניתוח.
- דוגמאות לנתונים מעובדים שהוצגו בדאשבורד.
- תיאור הסיפור שמספר המחקר ואופן בנייתו.
- ויזואליזציות שנבחרו להצגת הממצאים.
- מדריך טכני להרצת הדאשבורד ופתרון בעיות נפוצות.

---

## 📁 [central_west_hourly_weather_sample.csv](central_west_hourly_weather_sample.csv)  
קובץ נתונים לדוגמה בפורמט CSV, המכיל את 500 השורות הראשונות מתוך קובץ הנתונים המקורי הגדול.

---

## 🐍 [duckdb_and_sqlite.py](duckdb_and_sqlite.py)  
קובץ Python שמבצע את השלבים הבאים:

- **טעינת נתונים ל־DuckDB**: טעינת קובץ CSV גדול למסד הנתונים ויצירת טבלה מרכזית.
- **עיבוד וניתוח נתונים**: ביצוע שאילתות SQL להפקת תובנות, כגון:
  - ממוצע טמפרטורה לאורך זמן  
  - סך המשקעים  
  - תנאים קיצוניים לפי תחנות
- **יצירת טבלאות קטנות ב־SQLite**: שמירת תוצאות השאילתות כטבלאות קטנות לשימוש בדאשבורד.

---

## 🗃 [central_west_data.db](central_west_data.db)  
מסד נתונים בפורמט **SQLite**, הכולל את הטבלאות הקטנות ששימשו לניתוח והוויזואליזציה בדאשבורד.

---

## 📊 [streamlit_dashboard.py](streamlit_dashboard.py)  
קובץ הקוד הראשי של הדאשבורד, שנכתב ב־**Streamlit**. הקוד מחולק לעמודים עם ניווט צדדי ומכיל:

- ויזואליזציות גרפיות
- טבלאות נתונים
- תובנות מרכזיות מהמחקר

---

## 📦 [requirements.txt](requirements.txt)  
רשימת כל חבילות ה־Python הנדרשות להרצת הדאשבורד, כולל:

- `streamlit`
- `matplotlib`
- `seaborn`
- `pandas`
- `wordcloud`

---

💡 להרצת הדאשבורד, יש לוודא התקנת התלויות ולהפעיל את הקובץ `streamlit_dashboard.py` באמצעות הפקודה:
```bash
streamlit run streamlit_dashboard.py

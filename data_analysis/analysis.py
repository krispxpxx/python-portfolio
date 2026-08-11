import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Создаём папку для графиков
os.makedirs("charts", exist_ok=True)

# Загружаем датасет (с реального сайта)
url = "https://raw.githubusercontent.com/plotly/datasets/master/student_marks.csv"
df = pd.read_csv(url)

print("📊 Информация о данных:")
print(df.info())
print("\n📈 Статистика:")
print(df.describe())

# 1. Гистограмма оценок по математике
plt.figure(figsize=(10, 6))
sns.histplot(df['MATH'], bins=20, kde=True, color='blue')
plt.title('Распределение оценок по математике')
plt.xlabel('Оценка')
plt.ylabel('Количество студентов')
plt.savefig('charts/math_distribution.png')
plt.close()
print("✅ График 1 сохранён: math_distribution.png")

# 2. Тепловая карта корреляции
plt.figure(figsize=(8, 6))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Корреляция между предметами')
plt.savefig('charts/correlation_heatmap.png')
plt.close()
print("✅ График 2 сохранён: correlation_heatmap.png")

# 3. Boxplot по предметам
plt.figure(figsize=(12, 6))
df_melted = df.melt(id_vars=['NUMBER OF STUDENTS', 'AGE'], 
                     value_vars=['MATH', 'SCIENCE', 'ENGLISH', 'HISTORY'],
                     var_name='Subject', value_name='Score')
sns.boxplot(x='Subject', y='Score', data=df_melted)
plt.title('Распределение оценок по предметам')
plt.savefig('charts/subject_boxplot.png')
plt.close()
print("✅ График 3 сохранён: subject_boxplot.png")

print("\n✅ Все графики сохранены в папке charts/")
print(f"📊 Всего студентов: {len(df)}")
print("🏆 Средние оценки:")
print(df[['MATH', 'SCIENCE', 'ENGLISH', 'HISTORY']].mean())

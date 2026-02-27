import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

def analyze_events(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        df = pd.DataFrame(data["events"])
        
        print("Первые 5 строк данных:")
        print(df.head())
        print("\nРаспределение событий по типам:")
        print(df['signature'].value_counts())

        plt.figure(figsize=(12, 8))
        sns.set_theme(style="whitegrid")
        
        plot = sns.countplot(data=df, y="signature", hue="signature", palette="viridis", legend=False)
        
        plt.title("Распределение типов событий информационной безопасности", fontsize=14)
        plt.xlabel("Количество событий", fontsize=12)
        plt.ylabel("Тип события (Signature)", fontsize=12)
        
        plt.tight_layout()
        plt.show()
        
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    analyze_events('events.json')

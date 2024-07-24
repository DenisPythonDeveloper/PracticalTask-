import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk

# Функция для АВС анализа
def abc_analysis(df):
    df['Total Cost'] = df['Річна потреба'] * df['Ціна за одиницю, у.о.']
    df = df.sort_values(by='Total Cost', ascending=False)
    df['Cumulative Cost'] = df['Total Cost'].cumsum()
    df['Cumulative Cost %'] = 100 * df['Cumulative Cost'] / df['Total Cost'].sum()
    df['ABC Category'] = pd.cut(df['Cumulative Cost %'], bins=[0, 70, 90, 100], labels=['A', 'B', 'C'])
    return df

# Функция для построения кривой Лоренца
def plot_lorenz_curve(df, curve_color='blue', text_color='black'):
    sorted_df = df.sort_values(by='Total Cost')
    cumulative_cost = sorted_df['Total Cost'].cumsum()
    cumulative_cost_percent = cumulative_cost / cumulative_cost.iloc[-1]
    cumulative_items_percent = np.arange(1, len(df) + 1) / len(df)

    plt.figure(figsize=(10, 6))
    plt.plot(cumulative_items_percent, cumulative_cost_percent, label='Lorenz Curve', color=curve_color)
    plt.plot([0,1], [0,1], 'k--', label='Equality Line')
    plt.xlabel('Cumulative Share of Items', color=text_color)
    plt.ylabel('Cumulative Share of Costs', color=text_color)
    plt.title('Lorenz Curve', color=text_color)
    plt.legend()
    plt.show()

# Функция для расчета вероятности банкротства
def calculate_bankruptcy_probability(data):
    current_ratio = data['Оборотні засоби'] / data['Короткострокові зобовязання']
    debt_ratio = data['Загальний борг фірми'] / data['Загальні активи']
    profitability_ratio = data['Балансовий прибуток'] / data['Загальний обсяг продаж']
    
    bankruptcy_probability = 1 - (current_ratio + profitability_ratio) / (2 * debt_ratio)
    return bankruptcy_probability

# Класс для графического интерфейса
class ABCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ABC Analysis, Lorenz Curve, and Bankruptcy Probability")
        
        # Создание интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        self.label = Label(self.root, text="Введите данные для ABC анализа")
        self.label.grid(row=0, column=0, columnspan=4)

        # Заголовки колонок для ABC анализа
        self.headers = ["№ матеріалу", "Річна потреба", "Ціна за одиницю, у.о.", "Загальна вартість матеріалу"]
        for col_num, header in enumerate(self.headers):
            header_label = Label(self.root, text=header)
            header_label.grid(row=1, column=col_num)

        # Ввод данных для ABC анализа
        self.data_entries = []
        for i in range(10):
            entry_row = []
            for j in range(4):
                entry = Entry(self.root)
                entry.grid(row=i+2, column=j)
                entry_row.append(entry)
            self.data_entries.append(entry_row)
        
        self.calculate_button = Button(self.root, text="Рассчитать ABC анализ", command=self.calculate_abc)
        self.calculate_button.grid(row=12, column=0, columnspan=4)

        self.curve_color_label = Label(self.root, text="Цвет кривой:")
        self.curve_color_label.grid(row=13, column=0)
        self.curve_color_entry = Entry(self.root)
        self.curve_color_entry.grid(row=13, column=1)
        
        self.text_color_label = Label(self.root, text="Цвет текста:")
        self.text_color_label.grid(row=13, column=2)
        self.text_color_entry = Entry(self.root)
        self.text_color_entry.grid(row=13, column=3)

        # Заголовки колонок для расчета вероятности банкротства
        self.label_bankruptcy = Label(self.root, text="Вкажіть данні для разоахування банкрутства фірми")
        self.label_bankruptcy.grid(row=14, column=0, columnspan=4)

        self.bankruptcy_headers = ["Показник", "Значення"]
        for col_num, header in enumerate(self.bankruptcy_headers):
            header_label = Label(self.root, text=header)
            header_label.grid(row=15, column=col_num)

        # Ввод данных для расчета вероятности банкротства
        self.bankruptcy_entries = []
        self.bankruptcy_data = ["Оборотні засоби", "Короткострокові зобовязання", "Загальний борг фірми", "Загальні активи", "Балансовий прибуток", "Загальний обсяг продаж"]
        for i, label_text in enumerate(self.bankruptcy_data):
            label = Label(self.root, text=label_text)
            label.grid(row=i+16, column=0)
            entry = Entry(self.root)
            entry.grid(row=i+16, column=1)
            self.bankruptcy_entries.append(entry)
        
        self.calculate_bankruptcy_button = Button(self.root, text="Розрахувати можливість банкрутства", command=self.calculate_bankruptcy)
        self.calculate_bankruptcy_button.grid(row=22, column=0, columnspan=4)
        
    def calculate_abc(self):
        data = []
        for entry_row in self.data_entries:
            row = [entry.get() for entry in entry_row]
            data.append(row)
        
        # Преобразование данных в DataFrame
        columns = ["№ матеріалу", "Річна потреба", "Ціна за одиницю, у.о.", "Загальна вартысть матерыалу"]
        df = pd.DataFrame(data, columns=columns)
        df['Річна потреба'] = df['Річна потреба'].astype(float)
        df['Ціна за одиницю, у.о.'] = df['Ціна за одиницю, у.о.'].astype(float)
        
        # Выполнение АВС анализа
        df = abc_analysis(df)
        
        # Получение цветов для графика
        curve_color = self.curve_color_entry.get() or 'blue'
        text_color = self.text_color_entry.get() or 'black'
        
        # Построение кривой Лоренца
        plot_lorenz_curve(df, curve_color, text_color)
    
    def calculate_bankruptcy(self):
        data = {}
        for i, entry in enumerate(self.bankruptcy_entries):
            data[self.bankruptcy_data[i]] = float(entry.get())
        
        # Преобразование данных в DataFrame
        df = pd.DataFrame([data])
        
        # Расчет вероятности банкротства
        bankruptcy_probability = calculate_bankruptcy_probability(df)
        
        # Вывод результата
        result_label = Label(self.root, text=f"Можливість банкрутства: {bankruptcy_probability:.2f}")
        result_label.grid(row=23, column=0, columnspan=4)

if __name__ == "__main__":
    root = Tk()
    app = ABCApp(root)
    root.mainloop()

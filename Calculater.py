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
        self.label.grid(row=0, column=0, columnspan=5)

        # Заголовки колонок для ABC анализа
        self.headers = ["№ матеріалу", "Річна потреба", "Ціна за одиницю, у.о.", "Одиниця виміру", "Загальна вартість матеріалу"]
        for col_num, header in enumerate(self.headers):
            header_label = Label(self.root, text=header)
            header_label.grid(row=1, column=col_num)

        # Ввод данных для ABC анализа
        self.data_entries = []
        for i in range(10):
            entry_row = []
            for j in range(5):
                entry = Entry(self.root)
                entry.grid(row=i+2, column=j)
                entry_row.append(entry)
            self.data_entries.append(entry_row)
        
        self.calculate_button = Button(self.root, text="Рассчитать ABC анализ", command=self.calculate_abc)
        self.calculate_button.grid(row=12, column=0, columnspan=5)

        self.curve_color_label = Label(self.root, text="Цвет кривой:")
        self.curve_color_label.grid(row=13, column=0)
        self.curve_color_entry = Entry(self.root)
        self.curve_color_entry.grid(row=13, column=1)
        
        self.text_color_label = Label(self.root, text="Цвет текста:")
        self.text_color_label.grid(row=13, column=2)
        self.text_color_entry = Entry(self.root)
        self.text_color_entry.grid(row=13, column=3)

        # Заголовки колонок для расчета вероятности банкротства
        self.label_bankruptcy = Label(self.root, text="Введите данные для расчета вероятности банкротства")
        self.label_bankruptcy.grid(row=14, column=0, columnspan=5)

        self.bankruptcy_headers = ["Показник", "Значення"]
        for col_num, header in enumerate(self.bankruptcy_headers):
            header_label = Label(self.root, text=header)
            header_label.grid(row=15, column=col_num)

        # Ввод данных для расчета вероятности банкротства
        self.bankruptcy_entries = []
        self.bankruptcy_data = ["Оборотні засоби", "Короткострокові зобовязання", "Загальний борг фірми", "Загальні активи", "Балансовий прибуток", "Загальний обсяг продаж", "Накопичений капітал", "Капітал фірми"]
        for i, label_text in enumerate(self.bankruptcy_data):
            label = Label(self.root, text=label_text)
            label.grid(row=i+16, column=0)
            entry = Entry(self.root)
            entry.grid(row=i+16, column=1)
            self.bankruptcy_entries.append(entry)
        
        self.calculate_bankruptcy_button = Button(self.root, text="Рассчитать вероятность банкротства", command=self.calculate_bankruptcy)
        self.calculate_bankruptcy_button.grid(row=24, column=0, columnspan=5)
        
    def calculate_abc(self):
        data = []
        for entry_row in self.data_entries:
            row = [entry.get() for entry in entry_row]
            data.append(row)
        
        # Преобразование данных в DataFrame
        columns = ["№ матеріалу", "Річна потреба", "Ціна за одиницю, у.о.", "Одиниця виміру", "Загальна вартість матеріалу"]
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
        
        # Обновление таблицы с результатами АВС анализа
        self.update_abc_table(df)
    
    def update_abc_table(self, df):
        if hasattr(self, 'abc_treeview'):
            self.abc_treeview.destroy()
        
        self.abc_treeview = ttk.Treeview(self.root)
        self.abc_treeview.grid(row=26, column=0, columnspan=5)
        
        self.abc_treeview["columns"] = ("№ матеріалу", "Річна потреба", "Ціна за одиницю, у.о.", "Одиниця виміру", "Загальна вартість матеріалу", "ABC Category")
        for col in self.abc_treeview["columns"]:
            self.abc_treeview.heading(col, text=col)
            self.abc_treeview.column(col, anchor='center')
        
        for index, row in df.iterrows():
            self.abc_treeview.insert("", "end", values=(row["№ матеріалу"], row["Річна потреба"], row["Ціна за одиницю, у.о."], row["Одиниця виміру"], row["Total Cost"], row["ABC Category"]))
        
        self.abc_treeview["show"] = "headings"
        
        # Кнопки для сортировки
        self.sort_asc_button = Button(self.root, text="Сортировать по возрастанию", command=lambda: self.sort_abc_table(df, ascending=True))
        self.sort_asc_button.grid(row=27, column=0, columnspan=2)

        self.sort_desc_button = Button(self.root, text="Сортировать по убыванию", command=lambda: self.sort_abc_table(df, ascending=False))
        self.sort_desc_button.grid(row=27, column=2, columnspan=2)
    
    def sort_abc_table(self, df, ascending):
        df = df.sort_values(by='Total Cost', ascending=ascending)
        self.update_abc_table(df)

    def calculate_bankruptcy(self):
        data = {}
        for i, entry in enumerate(self.bankruptcy_entries):
            data[self.bankruptcy_data[i]] = float(entry.get())
        
        # Преобразование данных в DataFrame
        bankruptcy_probability = calculate_bankruptcy_probability(data)
        
        if hasattr(self, 'bankruptcy_label'):
            self.bankruptcy_label.destroy()
        
        if bankruptcy_probability > 0.5:
            result_text = "Фирма банкрот"
        elif 0.2 < bankruptcy_probability <= 0.5:
            result_text = "Фирма еще на плаву, но может затонуть"
        else:
            result_text = "Фирма прибыльна!!!"
        
        self.bankruptcy_label = Label(self.root, text=result_text)
        self.bankruptcy_label.grid(row=25, column=0, columnspan=5)

# Основная функция
if __name__ == "__main__":
    root = Tk()
    app = ABCApp(root)
    root.mainloop()

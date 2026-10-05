import glob
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).parent
file_path = BASE_DIR / "data" / "sales_report.xlsx"

pd.set_option("display.max_rows", 100)


sales = pd.read_excel(
    file_path,
    sheet_name="Sales",   # назва аркуша або його номер (0 - перший)
    skiprows=2,           # пропускаємо 2 рядки із заголовком звіту
    usecols="A:H",        # беремо стовпці A-G, без приміток
)


# Умова дає Series з True/False - "маску"
# mask = sales["city"] == "Київ"
# print(mask.head())
# print("================================")
# print(sales[mask])          # лишаються рядки, де True

# big_orders = sales[sales["quantity"] >= 3]
# print(big_orders) # 32

# kyiv_big = sales[(sales["city"] == "Київ") & (sales["quantity"] >= 3)]
# kyiv_or_lviv = sales[(sales["city"] == "Київ") | (sales["city"] == "Львів")]
# not_kyiv = sales[~(sales["city"] == "Київ")]

# print(len(kyiv_big), len(kyiv_or_lviv), len(not_kyiv))


# Зручні скорочення
# print(sales[sales["city"].isin(["Київ", "Львів"])])      # те саме, що з |
# print(sales[sales["price"].between(8000, 10000)])        # від 1000 до 10000 включно
# print(sales[sales["date"] >= "2026-03-01"])              # дату можна порівнювати з рядком
# print(sales[sales["date"].dt.month == 2])                # лютий: .dt дістає частини дати


# СОРТУВАННЯ

# top5 = sales.sort_values(by=["price", "quantity"], ascending=[False, False])
# print(top5.head(100))

# print(sales.query("city == 'Київ' and quantity >= 3"))


# print(sales.query("manager == 'Олена' and city == 'Львів'"))

# print(sales[
#     (
#         (sales["date"].between("2026-03-01", "2026-03-31")) & 
#         (sales["price"] > 1000)
#     )
#     ].sort_values(by="date")
# )

# print(sales[
#     (
#         (sales["price"] <= 2000) &
#         (sales["quantity"] >= 3)
#     )
#     ].sort_values(by="price", ascending=False)
# )

# for row in sales.itertuples():
#     print(row)
#     # row["total"] = row.price * row.quantity

# managers_sold = sales.groupby("manager")["total"].sum().reset_index()
# print(managers_sold)


# Шлях до папки з файлами
path = 'data/monthly_reports/'
# Шаблон для пошуку всіх .xlsx файлів у цій папці
all_files = glob.glob(path + "*.xlsx")
# Порожній список для зберігання DataFrame'ів
li = []
# Цикл по всіх знайдених файлах
for filename in all_files:
    df = pd.read_excel(filename, index_col=None, header=0)
    li.append(df)
    
# Об'єднуємо всі DataFrame'и зі списку в один
annual_report = pd.concat(li, axis=0, ignore_index=True)
print(f"Total rows collected: {len(annual_report)}")

annual_report.to_excel(BASE_DIR / "data" / "annual_report.xlsx", index=False)


from openpyxl.styles import Alignment, Font, PatternFill


def format_sheet(ws) -> None:
    # Шапка: ws[1] - перший рядок аркуша
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="4F81BD")
        cell.alignment = Alignment(horizontal="center")

    # Ширина кожного стовпця - за найдовшим значенням у ньому (код зі слайда 18)
    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length + 2

    ws.freeze_panes = "A2"                # шапка не тікає при прокручуванні
    ws.auto_filter.ref = ws.dimensions    # кнопки фільтра на шапці


pretty_path = BASE_DIR / "sales_h1_pretty.xlsx"

with pd.ExcelWriter(pretty_path, engine="openpyxl") as writer:
    sales.to_excel(writer)

    # writer.sheets - словник {назва аркуша: аркуш openpyxl}
    for ws in writer.sheets.values():
        format_sheet(ws)

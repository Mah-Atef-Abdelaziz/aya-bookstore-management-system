import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import ttkbootstrap as tb
from inventory_manager import *
from datetime import datetime
import random
import string
from tkinter import simpledialog
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import os
from PIL import Image, ImageTk

# محاولة استيراد المكتبات الإضافية
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import arabic_reshaper
    from bidi.algorithm import get_display
    EXTRA_LIBS_AVAILABLE = True
except ImportError:
    EXTRA_LIBS_AVAILABLE = False

app = tb.Window(themename="superhero")
app.title("🛒 نظام إدارة مكتبة آيه")

app.geometry("1200x800")  # يمكنك تعديل الأبعاد حسب الحاجة
# لجعل التطبيق ملء الشاشة فعلياً استخدم السطر التالي بدلاً من ذلك:
app.state('zoomed')
app.resizable(True, True)

# تكوين النافذة لدعم اللغة العربية
app.configure(cursor="arrow")

style = ttk.Style()
style.configure("Treeview.Heading", font=("Cairo", 12, "bold"))
style.configure("Treeview", font=("Cairo", 11))
style.configure('TButton', font=("Cairo", 11))
style.configure('TLabel', font=("Cairo", 11))
style.configure('TEntry', font=("Cairo", 11))

def refresh_list(products=None):
    for row in tree.get_children():
        tree.delete(row)
    data = products if products else get_all_products()
    for name, info in data.items():
        tree.insert('', 'end', values=(
            name,
            info["quantity"],
            f'{info["purchase_price"]} جنيه',
            f'{info["sale_price"]} جنيه',
            info["added"]
        ))

def add_product_ui():
    name = entry_name.get().strip()
    qty = entry_qty.get().strip()
    purchase_price = entry_purchase_price.get().strip()
    sale_price = entry_sale_price.get().strip()
    if (not name or 
        not qty.isdigit() or 
        not purchase_price.replace('.', '', 1).isdigit() or 
        not sale_price.replace('.', '', 1).isdigit()):
        messagebox.showwarning("تحذير", "يرجى إدخال بيانات صحيحة")
        return
    if add_product(name, int(qty), float(purchase_price), float(sale_price)):
        messagebox.showinfo("تم", "تمت إضافة المنتج بنجاح")
        # مسح حقول الإدخال بعد إضافة المنتج بنجاح
        entry_name.delete(0, tk.END)
        entry_qty.delete(0, tk.END)
        entry_purchase_price.delete(0, tk.END)
        entry_sale_price.delete(0, tk.END)
        refresh_list()
    else:
        messagebox.showerror("خطأ", "المنتج موجود بالفعل")

def update_product_ui():
    name = entry_name.get().strip()
    qty = entry_qty.get().strip()
    purchase_price = entry_purchase_price.get().strip()
    sale_price = entry_sale_price.get().strip()
    if (not name or 
        not qty.isdigit() or 
        not purchase_price.replace('.', '', 1).isdigit() or 
        not sale_price.replace('.', '', 1).isdigit()):
        messagebox.showwarning("تحذير", "يرجى إدخال بيانات صحيحة")
        return
    if update_product(name, int(qty), float(purchase_price), float(sale_price)):
        messagebox.showinfo("تم", "تم تحديث المنتج")
        refresh_list()
    else:
        messagebox.showerror("خطأ", "المنتج غير موجود")

def delete_product_ui():
    name = entry_name.get().strip()
    if not name:
        messagebox.showwarning("تحذير", "يرجى إدخال اسم المنتج")
        return
    if delete_product(name):
        messagebox.showinfo("تم", "تم حذف المنتج")
        refresh_list()
    else:
        messagebox.showerror("خطأ", "المنتج غير موجود")

def search_ui():
    name = entry_name.get().strip()
    if name:
        results = search_product(name)
        refresh_list(results)
    else:
        refresh_list()

# ===== إطار الصور والعنوان =====
header_frame = ttk.Frame(app)
header_frame.pack(pady=10, fill='x')

# تحميل وعرض الصور
image_frame = ttk.Frame(header_frame)
image_frame.pack(pady=5)

# تحميل الصور من مجلد الأصول
try:
    # تحديد أبعاد الصور بناءً على حجم الإطار أو حجم ثابت
    screen_width = 800  # يمكنك تعديل هذا الرقم حسب التصميم المطلوب
    screen_height = 120  # يمكنك تعديل هذا الرقم حسب التصميم المطلوب

    # تحميل الصورة الأولى
    img1_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "images", "library1.jpg")
    img1 = Image.open(img1_path)
    img1 = img1.resize((screen_width, screen_height), Image.LANCZOS)
    photo1 = ImageTk.PhotoImage(img1)
    
    # # تحميل الصورة الثانية
    # img2_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "images", "library2.jpg")
    # img2 = Image.open(img2_path)
    # img2 = img2.resize((screen_width, screen_height), Image.LANCZOS)
    # photo2 = ImageTk.PhotoImage(img2)
    
    # عرض الصور في إطار الصور
    img_label1 = ttk.Label(image_frame, image=photo1)
    img_label1.image = photo1  # حفظ مرجع للصورة لمنع حذفها بواسطة جامع القمامة
    img_label1.pack(side='left', padx=10)
    
    # img_label2 = ttk.Label(image_frame, image=photo2)
    # img_label2.image = photo2  # حفظ مرجع للصورة لمنع حذفها بواسطة جامع القمامة
    # img_label2.pack(side='left', padx=10)
    
except Exception as e:
    print(f"خطأ في تحميل الصور: {e}")

# ===== العنوان =====
title = tb.Label(header_frame, text="🛒 نظام إدارة مكتبة آيه", font=("Cairo", 20, "bold"), bootstyle="primary")
title.pack(pady=10)

# ===== حقول الإدخال =====
form_frame = ttk.Frame(app)
form_frame.pack(pady=10)

# ترتيب الحقول في المنتصف مع مراعاة اللغة العربية

# تكوين الإطار
form_frame.pack_configure(fill='both', expand=True)

# إضافة أعمدة فارغة على الجانبين لتوسيط المحتوى
form_frame.columnconfigure(0, weight=1)  # عمود فارغ على اليسار
form_frame.columnconfigure(5, weight=1)  # عمود فارغ على اليمين

# تعريف ترتيب الحقول (النص، الصف، العمود)
labels_data = [
    ("اسم المنتج", 0, 3),
    ("الكمية", 0, 1),
    ("سعر الشراء", 1, 3),
    ("سعر البيع", 1, 1)
]

entries = []
for text, row, col in labels_data:
    # إنشاء تسمية النص
    lbl = ttk.Label(form_frame, text=f"{text}:", font=("Cairo", 12))
    lbl.grid(row=row, column=col, padx=5, pady=5, sticky="e")
    
    # إنشاء حقل الإدخال
    entry = ttk.Entry(form_frame, font=("Cairo", 12), width=22, justify='right')  # محاذاة النص داخل حقل الإدخال إلى اليمين
    entry.grid(row=row, column=col+1, padx=5, pady=5, sticky="w")
    
    entries.append(entry)

entry_name, entry_qty, entry_purchase_price, entry_sale_price = entries

# ===== أزرار العمليات =====
btn_frame = ttk.Frame(app)
btn_frame.pack(pady=10)

# دالة إنشاء باركود للمنتج
def generate_barcode():
    name = entry_name.get().strip()
    if not name:
        messagebox.showwarning("تحذير", "يرجى إدخال اسم المنتج أولاً")
        return
        
    # إنشاء رمز باركود عشوائي
    barcode = ''.join(random.choices(string.digits, k=12))
    
    # عرض الباركود في نافذة منفصلة
    barcode_window = tb.Toplevel(app)
    barcode_window.title(f"باركود المنتج: {name}")
    barcode_window.geometry("400x300")
    
    # عرض الباركود
    barcode_label = tb.Label(barcode_window, text=f"باركود المنتج: {name}", font=("Cairo", 14, "bold"))
    barcode_label.pack(pady=10)
    
    # عرض الباركود كنص
    code_label = tb.Label(barcode_window, text=barcode, font=("Courier New", 16))
    code_label.pack(pady=10)
    
    # عرض الباركود كرسم بسيط
    barcode_frame = ttk.Frame(barcode_window, width=300, height=80, relief="solid", borderwidth=1)
    barcode_frame.pack(pady=10, padx=20)
    barcode_frame.pack_propagate(False)
    
    # رسم الباركود كخطوط عمودية
    canvas = tk.Canvas(barcode_frame, width=280, height=70, bg="white")
    canvas.pack(pady=5)
    
    x = 10
    for digit in barcode:
        # رسم خطوط بسماكات مختلفة حسب الرقم
        thickness = int(digit) + 1
        canvas.create_line(x, 10, x, 60, width=thickness, fill="black")
        x += 7
    
    # زر لطباعة الباركود (محاكاة)
    tb.Button(barcode_window, text="طباعة الباركود", bootstyle="primary", width=20, 
              command=lambda: messagebox.showinfo("طباعة", "تم إرسال الباركود للطباعة")).pack(pady=10)

# دالة عرض تقارير المبيعات
def show_sales_report():
    report_window = tb.Toplevel(app)
    report_window.title("📊 تقارير المبيعات والمخزون")
    report_window.geometry("900x600")
    
    # إنشاء علامات تبويب للتقارير المختلفة
    notebook = ttk.Notebook(report_window)
    notebook.pack(fill='both', expand=True, padx=10, pady=10)
    
    # تبويب تقرير المبيعات
    sales_tab = ttk.Frame(notebook)
    notebook.add(sales_tab, text="تقرير المبيعات")
    
    # تبويب تقرير المخزون
    inventory_tab = ttk.Frame(notebook)
    notebook.add(inventory_tab, text="تقرير المخزون")
    
    # تبويب الأرباح
    profit_tab = ttk.Frame(notebook)
    notebook.add(profit_tab, text="تقرير الأرباح")
    
    # الحصول على البيانات الفعلية للرسوم البيانية
    products = get_all_products()
    sales = load_sales()
    
    # التحقق من وجود بيانات
    if not products or not sales:
        no_data_label = tb.Label(report_window, text="لا توجد بيانات كافية للعرض", font=("Cairo", 14, "bold"))
        no_data_label.pack(pady=50)
        return
    
    # تجهيز بيانات المخزون
    product_names = list(products.keys())[:10] if len(products) > 10 else list(products.keys())  # أخذ أول 10 منتجات فقط للعرض
    quantities = [products[name]["quantity"] for name in product_names]
    
    # تجهيز بيانات المبيعات والأرباح
    sales_summary = {}
    for sale in sales:
        product_name = sale["product_name"]
        if product_name not in sales_summary:
            sales_summary[product_name] = {
                "total_quantity": 0,
                "total_amount": 0,
                "total_profit": 0
            }
        sales_summary[product_name]["total_quantity"] += sale["quantity_sold"]
        sales_summary[product_name]["total_amount"] += sale["total_amount"]
        sales_summary[product_name]["total_profit"] += sale["profit"]
    
    # اختيار أفضل 5 منتجات مبيعاً لعرضها في الرسوم البيانية
    top_products = sorted(sales_summary.items(), key=lambda x: x[1]["total_amount"], reverse=True)[:5]
    top_product_names = [item[0] for item in top_products]
    top_product_sales = [item[1]["total_amount"] for item in top_products]
    top_product_profits = [item[1]["total_profit"] for item in top_products]
    
    # التحقق من توفر المكتبات الإضافية
    if EXTRA_LIBS_AVAILABLE:
        # تحويل النص العربي ليعرض بشكل صحيح في الرسم البياني
        reshaped_names = [arabic_reshaper.reshape(name) for name in product_names]
        bidi_names = [get_display(name) for name in reshaped_names]
        
        # تحويل أسماء المنتجات الأكثر مبيعاً
        top_reshaped_names = [arabic_reshaper.reshape(name) for name in top_product_names] if top_product_names else []
        top_bidi_names = [get_display(name) for name in top_reshaped_names] if top_reshaped_names else []
        
        # رسم بياني للمخزون
        fig1 = plt.Figure(figsize=(8, 4))
        ax1 = fig1.add_subplot(111)
        ax1.bar(bidi_names, quantities)
        ax1.set_title(get_display(arabic_reshaper.reshape("كميات المخزون الحالية")))
        ax1.set_ylabel(get_display(arabic_reshaper.reshape("الكمية")))
        ax1.tick_params(axis='x', rotation=45)
        fig1.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, inventory_tab)
        canvas1.get_tk_widget().pack(fill='both', expand=True)
        
        # رسم بياني للمبيعات
        if top_product_names:
            # رسم بياني للمبيعات
            fig_sales = plt.Figure(figsize=(8, 4))
            ax_sales = fig_sales.add_subplot(111)
            ax_sales.bar(top_bidi_names, top_product_sales)
            ax_sales.set_title(get_display(arabic_reshaper.reshape("أفضل 5 منتجات مبيعاً")))
            ax_sales.set_ylabel(get_display(arabic_reshaper.reshape("إجمالي المبيعات (جنيه)")))
            ax_sales.tick_params(axis='x', rotation=45)
            fig_sales.tight_layout()
            canvas_sales = FigureCanvasTkAgg(fig_sales, sales_tab)
            canvas_sales.get_tk_widget().pack(side='bottom', fill='both', expand=True)
            
            # رسم بياني للأرباح
            fig2 = plt.Figure(figsize=(8, 4))
            ax2 = fig2.add_subplot(111)
            if sum(top_product_profits) > 0:  # تأكد من وجود أرباح موجبة
                ax2.pie(top_product_profits, labels=top_bidi_names, autopct='%1.1f%%')
                ax2.set_title(get_display(arabic_reshaper.reshape("نسبة الأرباح حسب المنتج")))
            else:
                ax2.text(0.5, 0.5, get_display(arabic_reshaper.reshape("لا توجد بيانات أرباح كافية")), 
                         horizontalalignment='center', verticalalignment='center')
            fig2.tight_layout()
            canvas2 = FigureCanvasTkAgg(fig2, profit_tab)
            canvas2.get_tk_widget().pack(fill='both', expand=True)
        else:
            # عرض رسالة إذا لم تكن هناك مبيعات
            for tab in [sales_tab, profit_tab]:
                msg_label = tb.Label(tab, text="لا توجد بيانات مبيعات كافية للعرض", font=("Cairo", 14, "bold"))
                msg_label.pack(pady=50)
    else:
        # عرض رسالة إذا كانت المكتبات غير متوفرة
        for tab in [inventory_tab, profit_tab]:
            msg_frame = ttk.Frame(tab)
            msg_frame.pack(fill='both', expand=True)
            
            msg_label = tb.Label(msg_frame, 
                               text="المكتبات المطلوبة للرسوم البيانية غير متوفرة\nيرجى تثبيت المكتبات: matplotlib, arabic-reshaper, python-bidi", 
                               font=("Cairo", 14), wraplength=500, justify="center")
            msg_label.pack(pady=50)
    
    # جدول المبيعات (البيانات الفعلية)
    sales_frame = ttk.Frame(sales_tab)
    sales_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    # إطار للتصفية والبحث
    filter_frame = ttk.Frame(sales_frame)
    filter_frame.pack(fill='x', pady=10)
    
    # اختيار المنتج للتصفية
    product_filter_frame = ttk.Frame(filter_frame)
    product_filter_frame.pack(side='left', padx=10)
    
    ttk.Label(product_filter_frame, text="تصفية حسب المنتج:", font=("Cairo", 11)).pack(side='left')
    
    # الحصول على قائمة المنتجات
    products = get_all_products()
    product_names = ["الكل"] + list(products.keys())
    
    product_filter_var = tk.StringVar(value="الكل")
    product_filter_combo = ttk.Combobox(product_filter_frame, textvariable=product_filter_var, values=product_names, font=("Cairo", 11), width=20)
    product_filter_combo.pack(side='left', padx=5)
    
    # زر تطبيق التصفية
    tb.Button(filter_frame, text="تطبيق التصفية", bootstyle="info-outline", width=15, 
             command=lambda: refresh_sales_report()).pack(side='left', padx=10)
    
    # عنوان الجدول
    sales_label = tb.Label(sales_frame, text="سجل المبيعات", font=("Cairo", 14, "bold"))
    sales_label.pack(pady=10)
    
    # جدول المبيعات
    sales_columns = ("المنتج", "الكمية المباعة", "سعر البيع", "إجمالي المبيعات", "الربح", "تاريخ البيع")
    sales_tree = ttk.Treeview(sales_frame, columns=sales_columns, show="headings", height=10)
    for col in sales_columns:
        sales_tree.heading(col, text=col)
        sales_tree.column(col, anchor="center", width=120)
    sales_tree.pack(fill='both', expand=True)
    
    # إطار ملخص المبيعات
    summary_frame = ttk.LabelFrame(sales_frame, text="ملخص المبيعات")
    summary_frame.pack(fill='x', pady=10, padx=10)
    
    summary_grid = ttk.Frame(summary_frame)
    summary_grid.pack(pady=10, padx=10, fill='x')
    
    # متغيرات لعرض ملخص المبيعات
    total_sales_var = tk.StringVar(value="0 جنيه")
    total_profit_var = tk.StringVar(value="0 جنيه")
    total_items_var = tk.StringVar(value="0")
    
    ttk.Label(summary_grid, text="إجمالي المبيعات:", font=("Cairo", 12, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=2)
    ttk.Label(summary_grid, textvariable=total_sales_var, font=("Cairo", 12)).grid(row=0, column=1, sticky="w", padx=5, pady=2)
    
    ttk.Label(summary_grid, text="إجمالي الأرباح:", font=("Cairo", 12, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=2)
    ttk.Label(summary_grid, textvariable=total_profit_var, font=("Cairo", 12)).grid(row=1, column=1, sticky="w", padx=5, pady=2)
    
    ttk.Label(summary_grid, text="عدد المنتجات المباعة:", font=("Cairo", 12, "bold")).grid(row=2, column=0, sticky="w", padx=5, pady=2)
    ttk.Label(summary_grid, textvariable=total_items_var, font=("Cairo", 12)).grid(row=2, column=1, sticky="w", padx=5, pady=2)
    
    # دالة تحديث تقرير المبيعات
    def refresh_sales_report():
        # مسح الجدول
        for row in sales_tree.get_children():
            sales_tree.delete(row)
        
        # الحصول على المبيعات
        sales = load_sales()
        
        # تصفية حسب المنتج إذا تم اختيار منتج محدد
        selected_product = product_filter_var.get()
        if selected_product != "الكل":
            sales = [sale for sale in sales if sale["product_name"] == selected_product]
        
        # إضافة البيانات للجدول
        total_sales_amount = 0
        total_profit_amount = 0
        total_items_sold = 0
        
        for sale in sales:
            sales_tree.insert('', 'end', values=(
                sale["product_name"],
                sale["quantity_sold"],
                f'{sale["sale_price"]} جنيه',
                f'{sale["total_amount"]} جنيه',
                f'{sale["profit"]} جنيه',
                sale["date"]
            ))
            
            # تحديث الإجماليات
            total_sales_amount += sale["total_amount"]
            total_profit_amount += sale["profit"]
            total_items_sold += sale["quantity_sold"]
        
        # تحديث متغيرات الملخص
        total_sales_var.set(f"{total_sales_amount} جنيه")
        total_profit_var.set(f"{total_profit_amount} جنيه")
        total_items_var.set(str(total_items_sold))
        
        # عرض رسالة إذا لم تكن هناك مبيعات
        if not sales:
            sales_tree.insert('', 'end', values=("لا توجد مبيعات", "", "", "", "", ""))
    
    # تحديث تقرير المبيعات عند فتح النافذة
    refresh_sales_report()

# دالة إعدادات النظام
def show_settings():
    settings_window = tb.Toplevel(app)
    settings_window.title("⚙️ إعدادات النظام")
    settings_window.geometry("500x400")
    
    settings_label = tb.Label(settings_window, text="⚙️ إعدادات النظام", font=("Cairo", 16, "bold"))
    settings_label.pack(pady=15)
    
    # إطار الإعدادات
    settings_frame = ttk.Frame(settings_window)
    settings_frame.pack(pady=10, fill='both', expand=True, padx=20)
    
    # إعداد حد المخزون المنخفض
    stock_frame = ttk.Frame(settings_frame)
    stock_frame.pack(fill='x', pady=10)
    
    stock_label = ttk.Label(stock_frame, text="حد المخزون المنخفض:", font=("Cairo", 12))
    stock_label.pack(side='left', padx=10)
    
    stock_var = tk.StringVar(value="5")
    stock_entry = ttk.Entry(stock_frame, textvariable=stock_var, width=10)
    stock_entry.pack(side='left', padx=10)
    
    # إعداد العملة
    currency_frame = ttk.Frame(settings_frame)
    currency_frame.pack(fill='x', pady=10)
    
    currency_label = ttk.Label(currency_frame, text="العملة:", font=("Cairo", 12))
    currency_label.pack(side='left', padx=10)
    
    currency_var = tk.StringVar(value="جنيه")
    currency_entry = ttk.Entry(currency_frame, textvariable=currency_var, width=10)
    currency_entry.pack(side='left', padx=10)
    
    # زر حفظ الإعدادات
    tb.Button(settings_window, text="حفظ الإعدادات", bootstyle="success", width=20,
              command=lambda: messagebox.showinfo("تم", "تم حفظ الإعدادات بنجاح")).pack(pady=20)

# دالة التراجع عن آخر إجراء
def undo_ui():
    if undo_last_action():
        messagebox.showinfo("تم", "تم التراجع عن آخر إجراء")
        refresh_list()
    else:
        messagebox.showwarning("تحذير", "لا يوجد إجراء للتراجع عنه")

# دالة فتح نافذة سلة المهملات
def open_recycle_bin():
    # إنشاء نافذة جديدة لسلة المهملات
    recycle_bin_window = tb.Toplevel(app)
    recycle_bin_window.title("🗑️ سلة المهملات")
    recycle_bin_window.geometry("800x500")
    recycle_bin_window.resizable(True, True)
    
    # عنوان النافذة
    title_label = tb.Label(recycle_bin_window, text="🗑️ سلة المهملات", font=("Cairo", 16, "bold"), bootstyle="danger")
    title_label.pack(pady=10)
    
    # إنشاء جدول لعرض المنتجات المحذوفة
    rb_columns = ("اسم المنتج", "الكمية", "سعر الشراء", "سعر البيع", "تاريخ الإضافة", "تاريخ الحذف")
    rb_tree = ttk.Treeview(recycle_bin_window, columns=rb_columns, show="headings", height=10)
    for col in rb_columns:
        rb_tree.heading(col, text=col)
        rb_tree.column(col, anchor="center", width=130)
    rb_tree.pack(padx=10, pady=10, fill='both', expand=True)
    
    # دالة تحديث قائمة المنتجات المحذوفة
    def refresh_recycle_bin():
        for row in rb_tree.get_children():
            rb_tree.delete(row)
        deleted_products = get_recycle_bin()
        for name, info in deleted_products.items():
            rb_tree.insert('', 'end', values=(
                name,
                info["quantity"],
                f'{info["purchase_price"]} جنيه',
                f'{info["sale_price"]} جنيه',
                info["added"],
                info.get("deleted_at", "غير معروف")
            ))
    
    # دالة استعادة منتج محدد
    def restore_product():
        selected_item = rb_tree.selection()
        if not selected_item:
            messagebox.showwarning("تحذير", "يرجى تحديد منتج لاستعادته")
            return
        
        item_values = rb_tree.item(selected_item[0], 'values')
        product_name = item_values[0]
        
        if restore_from_recycle_bin(product_name):
            messagebox.showinfo("تم", f"تمت استعادة المنتج: {product_name}")
            refresh_recycle_bin()
            refresh_list()  # تحديث القائمة الرئيسية أيضاً
        else:
            messagebox.showerror("خطأ", "فشلت عملية الاستعادة")
    
    # دالة حذف منتج نهائياً
    def delete_permanently_ui():
        selected_item = rb_tree.selection()
        if not selected_item:
            messagebox.showwarning("تحذير", "يرجى تحديد منتج لحذفه نهائياً")
            return
        
        item_values = rb_tree.item(selected_item[0], 'values')
        product_name = item_values[0]
        
        if messagebox.askyesno("تأكيد", f"هل أنت متأكد من حذف المنتج {product_name} نهائياً؟\nلا يمكن التراجع عن هذا الإجراء!"):
            if delete_permanently(product_name):
                messagebox.showinfo("تم", f"تم حذف المنتج: {product_name} نهائياً")
                refresh_recycle_bin()
            else:
                messagebox.showerror("خطأ", "فشلت عملية الحذف")
    
    # دالة تفريغ سلة المهملات
    def empty_recycle_bin_ui():
        if not rb_tree.get_children():
            messagebox.showinfo("معلومات", "سلة المهملات فارغة بالفعل")
            return
            
        if messagebox.askyesno("تأكيد", "هل أنت متأكد من تفريغ سلة المهملات بالكامل؟\nلا يمكن التراجع عن هذا الإجراء!"):
            if empty_recycle_bin():
                messagebox.showinfo("تم", "تم تفريغ سلة المهملات")
                refresh_recycle_bin()
            else:
                messagebox.showerror("خطأ", "فشلت عملية تفريغ سلة المهملات")
    
    # إطار الأزرار
    rb_btn_frame = ttk.Frame(recycle_bin_window)
    rb_btn_frame.pack(pady=10)
    
    # أزرار العمليات
    tb.Button(rb_btn_frame, text="استعادة", bootstyle="success-outline", width=15, command=restore_product).grid(row=0, column=0, padx=10)
    tb.Button(rb_btn_frame, text="حذف نهائي", bootstyle="danger-outline", width=15, command=delete_permanently_ui).grid(row=0, column=1, padx=10)
    tb.Button(rb_btn_frame, text="تفريغ السلة", bootstyle="warning-outline", width=15, command=empty_recycle_bin_ui).grid(row=0, column=2, padx=10)
    
    # تحديث قائمة المنتجات المحذوفة
    refresh_recycle_bin()

# الصف الأول من الأزرار
tb.Button(btn_frame, text="➕ إضافة", bootstyle="success-outline", width=20, command=add_product_ui).grid(row=0, column=0, padx=10, pady=5)
tb.Button(btn_frame, text="🔄 تحديث", bootstyle="warning-outline", width=20, command=update_product_ui).grid(row=0, column=1, padx=10, pady=5)
tb.Button(btn_frame, text="❌ حذف", bootstyle="danger-outline", width=20, command=delete_product_ui).grid(row=0, column=2, padx=10, pady=5)

# الصف الثاني من الأزرار
tb.Button(btn_frame, text="🔍 بحث", bootstyle="info-outline", width=20, command=search_ui).grid(row=1, column=0, padx=10, pady=5)
tb.Button(btn_frame, text="↩️ تراجع", bootstyle="secondary-outline", width=20, command=undo_ui).grid(row=1, column=1, padx=10, pady=5)
tb.Button(btn_frame, text="🗑️ سلة المهملات", bootstyle="danger", width=20, command=open_recycle_bin).grid(row=1, column=2, padx=10, pady=5)

# دالة الاستعادة (عكس التراجع)
def restore_ui():
    # تحقق إذا كان هناك إجراء يمكن استعادته
    if can_restore():
        # استعادة آخر إجراء تم التراجع عنه
        if restore_last_action():
            messagebox.showinfo("تم", "تم استعادة الإجراء السابق")
            refresh_list()
        else:
            messagebox.showwarning("تحذير", "لا يمكن استعادة الإجراء")
    else:
        messagebox.showwarning("تحذير", "لا توجد إجراءات للاستعادة")

# دالة تسجيل المبيعات وحساب الأرباح تلقائياً
def record_sale_ui():
    sale_window = tb.Toplevel(app)
    sale_window.title("💰 تسجيل المبيعات")
    sale_window.geometry("600x600")
    
    # عنوان النافذة
    title_label = tb.Label(sale_window, text="💰 تسجيل المبيعات وحساب الأرباح", font=("Cairo", 16, "bold"), bootstyle="success")
    title_label.pack(pady=15)
    
    # إطار اختيار المنتج والكمية
    form_frame = ttk.Frame(sale_window)
    form_frame.pack(pady=10, padx=20, fill='x')
    
    # اختيار المنتج
    product_frame = ttk.Frame(form_frame)
    product_frame.pack(fill='x', pady=5)
    
    product_label = ttk.Label(product_frame, text="اختر المنتج:", font=("Cairo", 12))
    product_label.pack(side='left', padx=10)
    
    # الحصول على قائمة المنتجات المتاحة
    products = get_all_products()
    product_names = list(products.keys())
    
    product_var = tk.StringVar()
    product_combo = ttk.Combobox(product_frame, textvariable=product_var, values=product_names, font=("Cairo", 12), width=30)
    product_combo.pack(side='left', padx=10)
    
    # إدخال الكمية
    qty_frame = ttk.Frame(form_frame)
    qty_frame.pack(fill='x', pady=5)
    
    qty_label = ttk.Label(qty_frame, text="الكمية المباعة:", font=("Cairo", 12))
    qty_label.pack(side='left', padx=10)
    
    qty_var = tk.StringVar(value="1")
    qty_entry = ttk.Entry(qty_frame, textvariable=qty_var, font=("Cairo", 12), width=10)
    qty_entry.pack(side='left', padx=10)
    
    # إطار عرض معلومات المنتج
    info_frame = ttk.LabelFrame(sale_window, text="معلومات المنتج", bootstyle="info")
    info_frame.pack(pady=10, padx=20, fill='x')
    
    # متغيرات لعرض معلومات المنتج
    available_qty_var = tk.StringVar(value="-")
    purchase_price_var = tk.StringVar(value="-")
    sale_price_var = tk.StringVar(value="-")
    
    # عرض معلومات المنتج
    info_grid = ttk.Frame(info_frame)
    info_grid.pack(pady=10, padx=10, fill='x')
    
    ttk.Label(info_grid, text="الكمية المتاحة:", font=("Cairo", 11)).grid(row=0, column=0, sticky="w", padx=5, pady=2)
    ttk.Label(info_grid, textvariable=available_qty_var, font=("Cairo", 11)).grid(row=0, column=1, sticky="w", padx=5, pady=2)
    
    ttk.Label(info_grid, text="سعر الشراء:", font=("Cairo", 11)).grid(row=1, column=0, sticky="w", padx=5, pady=2)
    ttk.Label(info_grid, textvariable=purchase_price_var, font=("Cairo", 11)).grid(row=1, column=1, sticky="w", padx=5, pady=2)
    
    ttk.Label(info_grid, text="سعر البيع:", font=("Cairo", 11)).grid(row=2, column=0, sticky="w", padx=5, pady=2)
    ttk.Label(info_grid, textvariable=sale_price_var, font=("Cairo", 11)).grid(row=2, column=1, sticky="w", padx=5, pady=2)
    
    # إطار حساب الأرباح
    calc_frame = ttk.LabelFrame(sale_window, text="حساب المبيعات والأرباح", bootstyle="success")
    calc_frame.pack(pady=10, padx=20, fill='x')
    
    # متغيرات لحساب الأرباح
    total_sale_var = tk.StringVar(value="-")
    total_profit_var = tk.StringVar(value="-")
    
    # عرض حسابات الأرباح
    calc_grid = ttk.Frame(calc_frame)
    calc_grid.pack(pady=10, padx=10, fill='x')
    
    ttk.Label(calc_grid, text="إجمالي المبيعات:", font=("Cairo", 12, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
    ttk.Label(calc_grid, textvariable=total_sale_var, font=("Cairo", 12, "bold"), bootstyle="success").grid(row=0, column=1, sticky="w", padx=5, pady=5)
    
    ttk.Label(calc_grid, text="إجمالي الأرباح:", font=("Cairo", 12, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=5)
    ttk.Label(calc_grid, textvariable=total_profit_var, font=("Cairo", 12, "bold"), bootstyle="success").grid(row=1, column=1, sticky="w", padx=5, pady=5)
    
    # دالة تحديث معلومات المنتج عند اختياره
    def update_product_info(*args):
        selected_product = product_var.get()
        if selected_product in products:
            product_info = products[selected_product]
            available_qty_var.set(str(product_info["quantity"]))
            purchase_price_var.set(f"{product_info['purchase_price']} جنيه")
            sale_price_var.set(f"{product_info['sale_price']} جنيه")
            
            # تحديث حسابات الأرباح
            try:
                qty = int(qty_var.get())
                total_sale = qty * product_info["sale_price"]
                total_profit = qty * (product_info["sale_price"] - product_info["purchase_price"])
                
                total_sale_var.set(f"{total_sale} جنيه")
                total_profit_var.set(f"{total_profit} جنيه")
            except ValueError:
                total_sale_var.set("-")
                total_profit_var.set("-")
        else:
            available_qty_var.set("-")
            purchase_price_var.set("-")
            sale_price_var.set("-")
            total_sale_var.set("-")
            total_profit_var.set("-")
    
    # ربط دالة التحديث بتغيير المنتج أو الكمية
    product_var.trace_add("write", update_product_info)
    qty_var.trace_add("write", update_product_info)
    
    # دالة تسجيل عملية البيع
    def save_sale():
        selected_product = product_var.get()
        if not selected_product:
            messagebox.showwarning("تحذير", "يرجى اختيار منتج")
            return
            
        try:
            qty = int(qty_var.get())
            if qty <= 0:
                messagebox.showwarning("تحذير", "يرجى إدخال كمية صحيحة أكبر من صفر")
                return
        except ValueError:
            messagebox.showwarning("تحذير", "يرجى إدخال كمية صحيحة")
            return
        
        # تسجيل عملية البيع
        success, result = record_sale(selected_product, qty)
        
        if success:
            messagebox.showinfo("تم", f"تم تسجيل عملية البيع بنجاح\n\nالمنتج: {selected_product}\nالكمية: {qty}\nإجمالي المبيعات: {result['total_amount']} جنيه\nإجمالي الأرباح: {result['profit']} جنيه")
            # تحديث قائمة المنتجات
            refresh_list()
            # إعادة تحميل قائمة المنتجات لتحديث الكميات
            products = get_all_products()
            product_names = list(products.keys())
            product_combo['values'] = product_names
            # تحديث معلومات المنتج
            update_product_info()
        else:
            messagebox.showerror("خطأ", f"فشلت عملية البيع: {result}")
    
    # أزرار العمليات
    btn_frame = ttk.Frame(sale_window)
    btn_frame.pack(pady=15)
    
    tb.Button(btn_frame, text="تسجيل عملية البيع", bootstyle="success", width=20, command=save_sale).grid(row=0, column=0, padx=10)
    tb.Button(btn_frame, text="إلغاء", bootstyle="secondary", width=15, command=sale_window.destroy).grid(row=0, column=1, padx=10)

# الصف الثالث من الأزرار - الميزات الجديدة
tb.Button(btn_frame, text="💰 تسجيل مبيعات", bootstyle="success", width=20, command=record_sale_ui).grid(row=2, column=0, padx=10, pady=5)
tb.Button(btn_frame, text="📊 تقارير المبيعات", bootstyle="primary", width=20, command=show_sales_report).grid(row=2, column=1, padx=10, pady=5)
tb.Button(btn_frame, text="⚙️ الإعدادات", bootstyle="secondary", width=20, command=show_settings).grid(row=2, column=2, padx=10, pady=5)

# ===== جدول عرض المنتجات =====
columns = ("اسم المنتج", "الكمية", "سعر الشراء", "سعر البيع", "تاريخ الإضافة")
tree = ttk.Treeview(app, columns=columns, show="headings", height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=160)
tree.pack(padx=10, pady=10, fill='both')

# ===== قسم المنتجات التي على وشك النفاد =====
def show_low_stock_products():
    low_stock_window = tb.Toplevel(app)
    low_stock_window.title("⚠️ المنتجات على وشك النفاد")
    low_stock_window.geometry("800x400")
    low_stock_window.resizable(True, True)
    
    # عنوان النافذة
    title_label = tb.Label(low_stock_window, text="⚠️ المنتجات على وشك النفاد", font=("Cairo", 16, "bold"), bootstyle="warning")
    title_label.pack(pady=10)
    
    # إنشاء جدول لعرض المنتجات التي على وشك النفاد
    ls_columns = ("اسم المنتج", "الكمية", "سعر الشراء", "سعر البيع", "تاريخ الإضافة")
    ls_tree = ttk.Treeview(low_stock_window, columns=ls_columns, show="headings", height=10)
    for col in ls_columns:
        ls_tree.heading(col, text=col)
        ls_tree.column(col, anchor="center", width=130)
    ls_tree.pack(padx=10, pady=10, fill='both', expand=True)
    
    # تحديد الحد الأدنى للمخزون من الإعدادات أو استخدام القيمة الافتراضية
    # القيمة الافتراضية هي 5 وحدات
    LOW_STOCK_THRESHOLD = 5
    
    # عرض القيمة الحالية للحد الأدنى بشكل أكثر وضوحاً
    threshold_frame = ttk.Frame(low_stock_window)
    threshold_frame.pack(pady=10)
    
    threshold_label = tb.Label(threshold_frame, 
                             text=f"⚠️ الحد الأدنى للمخزون: {LOW_STOCK_THRESHOLD} وحدات", 
                             font=("Cairo", 14, "bold"), 
                             bootstyle="warning")
    threshold_label.pack(pady=5)
    
    # عرض المنتجات التي على وشك النفاد
    products = get_all_products()
    low_stock_count = 0
    for name, info in products.items():
        if info["quantity"] <= LOW_STOCK_THRESHOLD:
            ls_tree.insert('', 'end', values=(
                name,
                info["quantity"],
                f'{info["purchase_price"]} جنيه',
                f'{info["sale_price"]} جنيه',
                info["added"]
            ))
            low_stock_count += 1
    
    # عرض رسالة إذا لم تكن هناك منتجات على وشك النفاد
    if low_stock_count == 0:
        info_label = tb.Label(low_stock_window, text="لا توجد منتجات على وشك النفاد حالياً", font=("Cairo", 12), bootstyle="info")
        info_label.pack(pady=20)

# إضافة زر لعرض المنتجات التي على وشك النفاد
tb.Button(app, text="⚠️ المنتجات على وشك النفاد", bootstyle="warning-outline", width=25, command=show_low_stock_products).pack(pady=10)

# إضافة وظيفة النقر المزدوج لنسخ اسم المنتج
def on_tree_double_click(event):
    # الحصول على العنصر المحدد
    selected_item = tree.selection()
    if selected_item:  # إذا كان هناك عنصر محدد
        # الحصول على قيم العنصر المحدد
        item_values = tree.item(selected_item[0], 'values')
        # نسخ اسم المنتج (العمود الأول) إلى حقل اسم المنتج
        product_name = item_values[0]
        # مسح محتوى حقل الإدخال الحالي
        entry_name.delete(0, tk.END)
        # إدخال اسم المنتج في حقل الإدخال
        entry_name.insert(0, product_name)
        
        # عرض معلومات المنتج في نافذة منبثقة
        if messagebox.askyesno("معلومات المنتج", f"هل تريد عرض معلومات المنتج: {product_name}؟"):
            product_info_window = tb.Toplevel(app)
            product_info_window.title(f"معلومات المنتج: {product_name}")
            product_info_window.geometry("500x400")
            
            # عنوان النافذة
            info_title = tb.Label(product_info_window, text=f"معلومات المنتج: {product_name}", font=("Cairo", 16, "bold"), bootstyle="info")
            info_title.pack(pady=15)
            
            # إطار المعلومات
            info_frame = ttk.Frame(product_info_window)
            info_frame.pack(pady=10, fill='both', expand=True, padx=20)
            
            # عرض معلومات المنتج
            products = get_all_products()
            if product_name in products:
                info = products[product_name]
                
                labels = [
                    f"اسم المنتج: {product_name}",
                    f"الكمية المتاحة: {info['quantity']}",
                    f"سعر الشراء: {info['purchase_price']} جنيه",
                    f"سعر البيع: {info['sale_price']} جنيه",
                    f"تاريخ الإضافة: {info['added']}",
                    f"الربح لكل وحدة: {info['sale_price'] - info['purchase_price']} جنيه",
                    f"إجمالي قيمة المخزون: {info['quantity'] * info['sale_price']} جنيه"
                ]
                
                for i, text in enumerate(labels):
                    lbl = tb.Label(info_frame, text=text, font=("Cairo", 12), bootstyle="info")
                    lbl.pack(anchor="w", pady=5)
                
                # أزرار العمليات
                btn_info_frame = ttk.Frame(product_info_window)
                btn_info_frame.pack(pady=15)
                
                tb.Button(btn_info_frame, text="تعديل المنتج", bootstyle="warning", width=15, 
                          command=lambda: product_info_window.destroy()).grid(row=0, column=0, padx=10)
                tb.Button(btn_info_frame, text="إغلاق", bootstyle="primary", width=15, 
                          command=lambda: product_info_window.destroy()).grid(row=0, column=1, padx=10)

# ربط وظيفة النقر المزدوج بالشجرة
tree.bind('<Double-1>', on_tree_double_click)

# إضافة اختصارات لوحة المفاتيح
def add_shortcut(event):
    add_product_ui()

def update_shortcut(event):
    update_product_ui()

def delete_shortcut(event):
    delete_product_ui()

def search_shortcut(event):
    search_ui()

def undo_shortcut(event):
    undo_ui()

# ربط اختصارات لوحة المفاتيح
app.bind('<Control-a>', add_shortcut)  # Ctrl+A للإضافة
app.bind('<Control-u>', update_shortcut)  # Ctrl+U للتحديث
app.bind('<Control-d>', delete_shortcut)  # Ctrl+D للحذف
app.bind('<Control-f>', search_shortcut)  # Ctrl+F للبحث
app.bind('<Control-z>', undo_shortcut)  # Ctrl+Z للتراجع

# إضافة شريط الحالة
status_frame = ttk.Frame(app)
status_frame.pack(side='bottom', fill='x')

status_label = tb.Label(status_frame, text="جاهز", font=("Cairo", 10))
status_label.pack(side='left', padx=10, pady=5)

version_label = tb.Label(status_frame, text="الإصدار 1.1 | تم التطوير بواسطة مكتبة آيه", font=("Cairo", 10))
version_label.pack(side='right', padx=10, pady=5)

# عرض دليل المستخدم
def show_help():
    help_window = tb.Toplevel(app)
    help_window.title("دليل المستخدم")
    help_window.geometry("700x500")
    
    help_label = tb.Label(help_window, text="📚 دليل استخدام نظام إدارة مكتبة آيه", font=("Cairo", 16, "bold"))
    help_label.pack(pady=15)
    
    help_text = """
    📝 وصف النظام:
    نظام إدارة مكتبة آيه هو برنامج متكامل لإدارة المخزون والمبيعات في المكتبات ومحلات البيع. يوفر النظام واجهة سهلة الاستخدام باللغة العربية مع العديد من الميزات المتقدمة لمساعدتك في إدارة منتجاتك بكفاءة عالية.
    
    🔹 إضافة منتج: أدخل بيانات المنتج ثم اضغط على زر 'إضافة' أو اختصار Ctrl+A
    
    🔹 تحديث منتج: حدد المنتج من القائمة، عدل البيانات، ثم اضغط على زر 'تحديث' أو اختصار Ctrl+U
    
    🔹 حذف منتج: حدد المنتج من القائمة، ثم اضغط على زر 'حذف' أو اختصار Ctrl+D
    
    🔹 البحث عن منتج: أدخل اسم المنتج في حقل البحث، ثم اضغط على زر 'بحث' أو اختصار Ctrl+F
    
    🔹 التراجع عن آخر إجراء: اضغط على زر 'تراجع' أو اختصار Ctrl+Z
    
    🔹 استعادة الإجراء: اضغط على زر 'استعادة' لعكس وظيفة التراجع
    
    🔹 سلة المهملات: استعادة المنتجات المحذوفة أو حذفها نهائياً
      - يمكنك استعادة المنتجات المحذوفة بالضغط على زر 'استعادة'
      - يمكنك حذف المنتجات نهائياً بالضغط على زر 'حذف نهائي'
      - يمكنك إفراغ سلة المهملات بالكامل بالضغط على زر 'إفراغ السلة'
    
    🔹 تسجيل المبيعات: تسجيل عمليات البيع وحساب الأرباح تلقائياً
      - يمكنك اختيار المنتج وتحديد الكمية المباعة
      - يقوم النظام تلقائياً بحساب إجمالي المبيعات والأرباح
      - يتم تحديث المخزون تلقائياً بعد كل عملية بيع

    🔹 تقارير المبيعات: عرض تقارير المبيعات والمخزون والأرباح
      - يعرض النظام رسوم بيانية توضح المبيعات والأرباح
      - يمكنك الاطلاع على إحصائيات المخزون والمنتجات الأكثر مبيعاً
      - يمكنك تصفية التقارير حسب المنتج
    
    🔹 الإعدادات: تخصيص إعدادات النظام
      - يمكنك تعديل الحد الأدنى للمخزون (القيمة الافتراضية: 5 وحدات)
      - يمكنك تغيير العملة المستخدمة في النظام
    
    🔹 المنتجات على وشك النفاد: عرض المنتجات التي تحتاج إلى إعادة تخزين
      - يعرض النظام المنتجات التي تقل كميتها عن الحد الأدنى للمخزون (5 وحدات)
      - يمكنك معرفة الكميات المتبقية وأسعار الشراء والبيع
    
    🔹 معلومات المنتج: انقر نقراً مزدوجاً على أي منتج لعرض معلومات تفصيلية عنه
      - يعرض النظام معلومات كاملة عن المنتج مثل الكمية والأسعار وتاريخ الإضافة
      - يحسب النظام تلقائياً الربح لكل وحدة وإجمالي قيمة المخزون
    
    🔹 اختصارات لوحة المفاتيح:
      - Ctrl+A: إضافة منتج جديد
      - Ctrl+U: تحديث المنتج المحدد
      - Ctrl+D: حذف المنتج المحدد
      - Ctrl+F: البحث عن منتج
      - Ctrl+Z: التراجع عن آخر إجراء
      - F1: عرض دليل المستخدم
    """
    
    help_scroll = ScrolledText(help_window, font=("Cairo", 12), wrap=tk.WORD, height=20)
    help_scroll.pack(padx=20, pady=10, fill='both', expand=True)
    help_scroll.insert(tk.END, help_text)
    help_scroll.configure(state='disabled')
    
    # إضافة معلومات حول المكتبات المطلوبة
    libs_frame = ttk.Frame(help_window)
    libs_frame.pack(pady=10, fill='x')
    
    libs_label = tb.Label(libs_frame, text="المكتبات المطلوبة:", font=("Cairo", 12, "bold"))
    libs_label.pack(anchor="w", padx=20)
    
    libs_info = "ttkbootstrap, matplotlib (اختياري), arabic-reshaper (اختياري), python-bidi (اختياري)"
    libs_info_label = tb.Label(libs_frame, text=libs_info, font=("Cairo", 11))
    libs_info_label.pack(anchor="w", padx=20)
    
    note_label = tb.Label(libs_frame, 
                         text="ملاحظة: المكتبات الاختيارية مطلوبة فقط لعرض الرسوم البيانية وتحسين دعم اللغة العربية", 
                         font=("Cairo", 10), 
                         bootstyle="warning")
    note_label.pack(anchor="w", padx=20, pady=5)

# إضافة زر المساعدة
tb.Button(app, text="❓ دليل المستخدم", bootstyle="info", width=15, command=show_help).pack(side='bottom', pady=5)

refresh_list()
app.mainloop()

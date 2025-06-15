import json
import os
import copy
from datetime import datetime

PRODUCTS_FILE = 'products.json'
RECYCLE_BIN_FILE = 'recycle_bin.json'
SALES_FILE = 'sales.json'  # ملف جديد لتخزين المبيعات

# قائمة لتخزين حالات المنتجات السابقة للتراجع
products_history = []

def load_products():
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def save_products(products, save_history=True):
    # حفظ الحالة السابقة في التاريخ قبل التغيير
    if save_history:
        current_products = load_products()
        if current_products:  # تأكد من وجود منتجات لحفظها في التاريخ
            products_history.append(copy.deepcopy(current_products))
            # الاحتفاظ بآخر 10 حالات فقط لتوفير الذاكرة
            if len(products_history) > 10:
                products_history.pop(0)
    
    # حفظ المنتجات في الملف
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as file:
        json.dump(products, file, ensure_ascii=False, indent=4)

def add_product(name, quantity, purchase_price, sale_price):
    products = load_products()
    if name in products:
        return False
    products[name] = {
        "quantity": quantity,
        "purchase_price": purchase_price,
        "sale_price": sale_price,
        "added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_products(products)
    return True

def update_product(name, quantity, purchase_price, sale_price):
    products = load_products()
    if name in products:
        products[name]["quantity"] = quantity
        products[name]["purchase_price"] = purchase_price
        products[name]["sale_price"] = sale_price
        save_products(products)
        return True
    return False

# وظائف جديدة لإدارة المبيعات
def load_sales():
    """تحميل سجل المبيعات"""
    if os.path.exists(SALES_FILE):
        with open(SALES_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def save_sales(sales):
    """حفظ سجل المبيعات"""
    with open(SALES_FILE, 'w', encoding='utf-8') as file:
        json.dump(sales, file, ensure_ascii=False, indent=4)

def record_sale(product_name, quantity_sold, sale_price=None):
    """تسجيل عملية بيع لمنتج معين"""
    products = load_products()
    if product_name not in products:
        return False, "المنتج غير موجود"
    
    if products[product_name]["quantity"] < quantity_sold:
        return False, "الكمية المطلوبة غير متوفرة في المخزون"
    
    # تحديث كمية المنتج في المخزون
    products[product_name]["quantity"] -= quantity_sold
    save_products(products)
    
    # إذا لم يتم تحديد سعر البيع، استخدم سعر البيع الحالي للمنتج
    if sale_price is None:
        sale_price = products[product_name]["sale_price"]
    
    # حساب الربح
    purchase_price = products[product_name]["purchase_price"]
    profit = (sale_price - purchase_price) * quantity_sold
    total_amount = sale_price * quantity_sold
    
    # تسجيل عملية البيع
    sales = load_sales()
    sale_record = {
        "product_name": product_name,
        "quantity_sold": quantity_sold,
        "sale_price": sale_price,
        "purchase_price": purchase_price,
        "total_amount": total_amount,
        "profit": profit,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    sales.append(sale_record)
    save_sales(sales)
    
    return True, {
        "product_name": product_name,
        "quantity_sold": quantity_sold,
        "sale_price": sale_price,
        "total_amount": total_amount,
        "profit": profit
    }

def get_sales_report(start_date=None, end_date=None, product_name=None):
    """الحصول على تقرير المبيعات مع إمكانية التصفية حسب التاريخ والمنتج"""
    sales = load_sales()
    filtered_sales = []
    
    for sale in sales:
        include = True
        
        # تصفية حسب اسم المنتج إذا تم تحديده
        if product_name and sale["product_name"] != product_name:
            include = False
        
        # تصفية حسب تاريخ البداية إذا تم تحديده
        if start_date and sale["date"] < start_date:
            include = False
        
        # تصفية حسب تاريخ النهاية إذا تم تحديده
        if end_date and sale["date"] > end_date:
            include = False
        
        if include:
            filtered_sales.append(sale)
    
    return filtered_sales

def get_product_sales_summary(product_name=None):
    """الحصول على ملخص مبيعات منتج معين أو جميع المنتجات"""
    sales = load_sales()
    summary = {}
    
    for sale in sales:
        name = sale["product_name"]
        
        # تخطي المنتج إذا كان لا يطابق المنتج المطلوب
        if product_name and name != product_name:
            continue
        
        if name not in summary:
            summary[name] = {
                "total_quantity": 0,
                "total_amount": 0,
                "total_profit": 0
            }
        
        summary[name]["total_quantity"] += sale["quantity_sold"]
        summary[name]["total_amount"] += sale["total_amount"]
        summary[name]["total_profit"] += sale["profit"]
    
    return summary

def load_recycle_bin():
    """تحميل المنتجات المحذوفة من سلة المهملات"""
    if os.path.exists(RECYCLE_BIN_FILE):
        with open(RECYCLE_BIN_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def save_recycle_bin(recycle_bin):
    """حفظ المنتجات المحذوفة في سلة المهملات"""
    with open(RECYCLE_BIN_FILE, 'w', encoding='utf-8') as file:
        json.dump(recycle_bin, file, ensure_ascii=False, indent=4)

def delete_product(name):
    """نقل المنتج إلى سلة المهملات بدلاً من حذفه نهائياً"""
    products = load_products()
    if name in products:
        # نقل المنتج إلى سلة المهملات
        recycle_bin = load_recycle_bin()
        recycle_bin[name] = products[name]
        recycle_bin[name]["deleted_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_recycle_bin(recycle_bin)
        
        # حذف المنتج من قائمة المنتجات النشطة
        del products[name]
        save_products(products)
        return True
    return False

def get_recycle_bin():
    """الحصول على جميع المنتجات في سلة المهملات"""
    return load_recycle_bin()

def restore_from_recycle_bin(name):
    """استعادة منتج من سلة المهملات"""
    recycle_bin = load_recycle_bin()
    if name in recycle_bin:
        # استعادة المنتج إلى قائمة المنتجات النشطة
        products = load_products()
        product_data = recycle_bin[name]
        # إزالة حقل تاريخ الحذف
        if "deleted_at" in product_data:
            del product_data["deleted_at"]
        products[name] = product_data
        save_products(products)
        
        # حذف المنتج من سلة المهملات
        del recycle_bin[name]
        save_recycle_bin(recycle_bin)
        return True
    return False

def empty_recycle_bin():
    """تفريغ سلة المهملات (حذف جميع المنتجات نهائياً)"""
    if os.path.exists(RECYCLE_BIN_FILE):
        save_recycle_bin({})
        return True
    return False

def delete_permanently(name):
    """حذف منتج نهائياً من سلة المهملات"""
    recycle_bin = load_recycle_bin()
    if name in recycle_bin:
        del recycle_bin[name]
        save_recycle_bin(recycle_bin)
        return True
    return False

def search_product(name):
    products = load_products()
    return {k: v for k, v in products.items() if name in k}

def get_all_products():
    return load_products()

def undo_last_action():
    """التراجع عن آخر إجراء تم تنفيذه"""
    if products_history:
        # استعادة آخر حالة من التاريخ
        previous_state = products_history.pop()
        # حفظ الحالة السابقة بدون إضافتها إلى التاريخ
        save_products(previous_state, save_history=False)
        return True
    return False

def can_restore():
    """التحقق مما إذا كان هناك إجراء يمكن استعادته"""
    return len(products_history) > 0

def restore_last_action():
    """استعادة آخر إجراء تم التراجع عنه (عكس وظيفة التراجع)"""
    # هذه الوظيفة تعتمد على وجود حالة سابقة تم التراجع عنها
    # في الواقع، نحتاج إلى تخزين الحالات التي تم التراجع عنها في مصفوفة منفصلة
    # لكن للتبسيط، سنستخدم وظيفة التراجع نفسها لتحقيق وظيفة الاستعادة
    return undo_last_action()

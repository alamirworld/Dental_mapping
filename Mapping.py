import streamlit as st
import pandas as pd

# إعداد الصفحة بدون توسيع
st.set_page_config(layout="wide")  # الحفاظ على 'wide' كما هو الآن

# تنسيق العنوان ليكون في المنتصف
st.markdown("<h1 style='text-align: center;'>🔍 Dental Mapping     </h1>", unsafe_allow_html=True)

# تحديد مسار ملف الإكسل
FILE_PATH = "Dental Final UL V1.xlsx"

# تعديل CSS لتوسيع الحاوية الرئيسية وعرض الجدول
st.markdown("""
    <style>
        /* توسيع الحاوية الرئيسية للصفحة المركزية */
        .main .block-container {
            max-width: 95% !important;  /* توسيع الحاوية الرئيسية لتشغل 95% من عرض الصفحة */
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        /* تخصيص عرض الجدول */
        div[data-testid="stDataFrame"] {
            width: 100% !important;  /* جعل الجدول يأخذ كامل عرض الحاوية */
        }
    </style>
    """, unsafe_allow_html=True)

# استخدام session state لتتبع قيمة البحث
if 'search_text' not in st.session_state:
    st.session_state['search_text'] = ""

# دالة لتحديث قيمة البحث
def update_search_text():
    st.session_state['search_text'] = st.session_state['search_box']

# إنشاء مربع بحث أصغر مع تحديث تلقائي
st.text_input(
    "🔎 Enter Keyword Search  :",
    value=st.session_state['search_text'],
    key="search_box",
    help="اكتب كلمة البحث وسيتم التحديث تلقائيًا",
    on_change=update_search_text
)

# دالة البحث وعرض البيانات
def search_and_display_all_columns(file_path, search_text):
    try:
        # تحميل البيانات
        df = pd.read_excel(file_path)

        # التحقق من وجود بيانات في الملف
        if df.empty:
            st.error("❌ خطأ: الملف فارغ!")
            return

        # البحث في جميع الأعمدة النصية
        mask = pd.Series(False, index=df.index)
        for column in df.columns:
            if df[column].dtype == 'object':  # التركيز على الأعمدة النصية فقط
                mask |= df[column].str.contains(search_text, case=False, na=False)

        results = df[mask]

        if not results.empty:
            st.success(f"✅ Results founded   {len(results)}   Contain: '{search_text}'")
            st.dataframe(results, use_container_width=True, height=600)  # استخدام عرض الحاوية الكامل
        else:
            st.warning(f"⚠️ No data found     : '{search_text}'")
    except Exception as e:
        st.error(f"❌ خطأ: {e}")

# تنفيذ البحث تلقائيًا عند تغيير النص
search_text = st.session_state['search_text']
if search_text:
    search_and_display_all_columns(FILE_PATH, search_text)
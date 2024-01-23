from wagtail_modeladmin.options import (
    ModelAdmin, modeladmin_register)
from wagtail.contrib.forms.models import FormSubmission

class FormSubmissionAdmin(ModelAdmin):
    model = FormSubmission
    menu_label = 'Form Submissions'  # ชื่อที่จะแสดงในเมนู
    menu_icon = 'form'  # ไอคอนที่จะใช้ (ดูเอกสาร Wagtail เพื่อหาไอคอนที่ใช้ได้)
    add_to_settings_menu = False  # ไม่จำเป็นต้องเพิ่มในเมนูการตั้งค่า
    exclude_from_explorer = False  # ไม่จำเป็นต้องซ่อนจาก explorer
    list_display = ('page', 'submit_time')  # ระบุ fields ที่ต้องการแสดง
    search_fields = ('form_data',)

# ลงทะเบียน FormSubmissionAdmin กับ wagtail
modeladmin_register(FormSubmissionAdmin)

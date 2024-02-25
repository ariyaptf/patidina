import datetime
import pyotp
import requests
import os

from django import forms
from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import DetailView

from .models import SupportPublication, PanDhamBook
from .forms import (
    SupportPublicationStepOneForm, SupportPublicationStepTwoForm,
    SupportPublicationStepThreeForm, SupportPublicationStepFourForm
)
from coderedcms.models import ReusableContent
from formtools.wizard.views import SessionWizardView
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("API_KEY")
client_id = os.getenv("CLIENT_ID")
send_sms_url = os.getenv("SEND_SMS_URL")

class SupportPublicationView(SessionWizardView):
    # form list
    form_list = [
        SupportPublicationStepOneForm,
        SupportPublicationStepTwoForm,
        SupportPublicationStepThreeForm,
        SupportPublicationStepFourForm
    ]
    template_name = 'pandham/support.html'

    # get context data
    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        all_data = {}
        for step in self.get_form_list():
            step_data = self.get_cleaned_data_for_step(step)
            if step_data:
                all_data[step] = step_data
        context['all_data'] = all_data

        return context

    # get form
    def get_form(self, step=None, data=None, files=None):
        form = super(SupportPublicationView, self).get_form(step, data, files)
        # ขั้นตอนที่ 1
        if step == '1':
            step_one_data = self.get_cleaned_data_for_step('0')  # '0' คือขั้นตอนแรก
            if step_one_data is not None:
                book_id = step_one_data.get('book').id
                book = PanDhamBook.objects.get(pk=book_id)
                # กำหนดรูปแบบของฟิลด์ใหม่
                self.adjust_form_fields(form, book)
        # ขั้นตอนที่ 2
        elif step == '2':
            step_two_data = self.get_cleaned_data_for_step('1')  # '1' คือขั้นตอนที่สอง
            if step_two_data is not None:
                distribution_preference = step_two_data.get('distribution_preference')
                quantity = step_two_data.get('quantity')
                if distribution_preference == 'no_book_request':
                    # requested_books
                    form.fields['requested_books'].widget.attrs['hidden'] = True
                    form.fields['requested_books'].label = False
                    form.fields['requested_books'].help_text = False
                    form.fields['requested_books'].initial = 0
                    # shipping_address
                    form.fields['shipping_address'].widget.attrs['hidden'] = True
                    form.fields['shipping_address'].label = False
                    form.fields['shipping_address'].help_text = False
                    # for_PanDham
                    form.fields['for_PanDham'].initial = quantity
                elif distribution_preference == 'request_book':
                    # requested_books
                    form.fields['requested_books'].widget.attrs['hidden'] = False
                    form.fields['requested_books'].label = _("Requested Books")
                    form.fields['requested_books'].help_text = _("Enter the number of books you want to request.")
                    form.fields['requested_books'].initial = 0
                    # shipping_address
                    form.fields['shipping_address'].widget.attrs['hidden'] = False
                    form.fields['shipping_address'].label = _("Shipping Address")
                    form.fields['shipping_address'].help_text = _("Enter the shipping address for the requested books.")
                    # for_PanDham
                    form.fields['for_PanDham'].initial = quantity - form.fields['requested_books'].initial
        # ขั้นตอนที่ 3
        elif step == '3':
            step_three_data = self.get_cleaned_data_for_step('2') # '2' คือขั้นตอนที่สาม
            if step_three_data is not None:
                step_one_data = self.get_cleaned_data_for_step('0')
                phone_number = step_one_data.get('phone_number')
                # ทำการส่ง OTP
                self.send_otp(phone_number)

        # ขั้นตอนที่ 4
        elif step == '4':
            step_four_data = self.get_cleaned_data_for_step('3') # '3' คือขั้นตอนที่สี่
            if step_four_data is not None:
                otp = step_four_data.get('otp')
                print(otp)

                # otp_secret_key = self.request.session.get('otp_secret_key')
                # opt_valid_date = self.request.session.get('otp_valid_date')

                # if otp_secret_key and opt_valid_date is not None:
                #     valid_date = datetime.fromisoformat(opt_valid_date)

                #     if valid_date > datetime.now():
                #         totp = pyotp.TOTP(otp_secret_key, interval=300)
                #         if totp.verify(otp):
                #             del self.request.session['otp_secret_key']
                #             del self.request.session['otp_valid_date']
                #             # ทำการค้นหา แสดงผล และบันทึกข้อมูล
                #             form.add_error('OTP is verified')
                #         else:
                #             form.add_error('otp', _('Invalid OTP'))
                #     else:
                #         form.add_error('otp', _('OTP has expired'))
                # else:
                #     form.add_error('otp', _('Something went wrong'))

        return form

    # done
    def done(self, form_list, **kwargs):
        all_data = {}
        for form in form_list:
            all_data.update(form.cleaned_data)

        support_publication = SupportPublication()
        support_publication.book_id = all_data['book'].id
        support_publication.name = all_data['name']
        support_publication.phone_number = all_data['phone_number']
        support_publication.amount_contributed = all_data['amount_contributed']
        support_publication.quantity = all_data['quantity']
        support_publication.distribution_preference = all_data['distribution_preference']
        support_publication.requested_books = all_data['requested_books']
        support_publication.shipping_address = all_data['shipping_address']
        support_publication.for_PanDham = all_data['for_PanDham']
        support_publication.target_address = all_data['target_address']
        support_publication.note = all_data['note']
        support_publication.otp = all_data['otp']

        support_publication.save()
        record_id = support_publication.id

        support_publication.target_groups.set(all_data['target_groups'])

        return HttpResponseRedirect(reverse_lazy('pandhamm_success', args=[record_id]))

    # functions
    def adjust_form_fields(self, form, book):
        form.fields['amount_contributed'] = forms.IntegerField(
            widget=forms.NumberInput(
                attrs={
                    'id': 'amount_contributed_range',
                    'type': 'range',
                    'class': 'form-range',
                    'oninput': f'showRangeValue(this.value, {book.price})',
                    'step': book.price,
                    'value': book.price
                }
            ),
            min_value=0,
            max_value=book.price * book.stock,
            label=_("Contribute funds"),
            help_text=_("...."),
        )
        form.fields['amount_contributed'].initial = book.price
        form.fields['quantity'].initial = 1

    # send otp
    def send_otp(self, phone_number):
        phone_number = "66" + phone_number[1:]
        print(phone_number)

        totp = pyotp.TOTP(pyotp.random_base32(), interval=300)
        otp = totp.now()
        self.request.session['otp_secret_key'] = totp.secret  # Save the OTP in the session
        valid_date = datetime.datetime.now() + datetime.timedelta(minutes=5)  # Save the OTP valid date in the session
        self.request.session['otp_valid_date'] = str(valid_date)

        message = """รหัส OTP สำหรับปันธรรมคือ: {otp} กรุณากรอกลงแบบฟอร์มภายใน 5 นาที
        อนุโมทนาครับ/ค่ะ
        """.format(otp=otp)

        url = send_sms_url
        params = {
            "SenderId": "PTF",
            "Is_Unicode": "true",
            "Is_Flash": "false",
            "Message": message,
            "MobileNumbers": phone_number,
            "apiKey": api_key,
            "clientId": client_id
        }
        response = requests.get(url, params=params)
        print(response.json())
        return JsonResponse(response.json())


class SuccessView(DetailView):
    model = SupportPublication
    template_name = ''
    context_object_name = 'support_publication'
    pk_url_kwarg = 'pk'



from django.forms import ModelForm, CharField, forms

from .models import Order, Complaint, Comment


class OrderForm(ModelForm):
    Discount_code = CharField(max_length=50)

    class Meta:
        model = Order
        fields = ['first_name',  'surname', 'address', 'send', 'Discount_code']
        exclude = ('discount_code',)


class ComplaintForm(ModelForm):
    class Meta:
        model = Complaint
        fields = ['name', 'message']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['nickname', 'grade', 'comment']

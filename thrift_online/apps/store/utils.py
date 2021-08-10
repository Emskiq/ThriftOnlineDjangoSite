from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from apps.order.views import render_pdf


def decrement_product_quantity(order):
    for item in order.item.all():
        product = item.product
        product.num_available = product.num_available - item.quantity
        product.super_save()

def send_order_conf_mail(order):
    subject = 'Order confirmation'
    from_email = 'noreply@thriftonline.com'
    to = ['emilski4@gmail.com', order.email]
    text_content = 'Твоята поръчка е приета!'
    html_content = render_to_string('order_confirmation.html', {'order': order})

    pdf = render_pdf('order_pdf.html', {'order' : order})

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content,'text/html')

    print("msg first:", msg)

    if pdf:
        name = "order_%s.pdf" % (order.id)
        msg.attach(name, pdf, 'application/pdf')

    print("msg second:", msg)

    msg.send()
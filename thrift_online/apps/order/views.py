from io import BytesIO

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.http import HttpResponse

from xhtml2pdf import pisa

from .models import Order

def render_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)

    if not pdf.err:
        return result.getvalue()

    return None

@login_required
def admin_order_pdf(request, order_id):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, pk=order_id)
        pdf = render_pdf('order_pdf.html', {'order' : order})

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            content = "attaachment; filename=%s.pdf" % (order_id)
            response['Content-Disposition'] = content

            return response
    
    return HttpResponse("Not found")
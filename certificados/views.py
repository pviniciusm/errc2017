from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import HttpResponse
from weasyprint import HTML
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json

tipos = {
    "OG" : "Organizador",
    "POG" : "Participante de Minicurso",
    "PA" : "Palestrante",
    "AU" : "Autor",
    "PC" : "Participante",
    "PR" : "Premio",
}

def certificados(request):
    ctf_1 = Certificado.objects.filter(tipo__in=('PC', 'POG', 'OG'))
    ctf_2 = Certificado.objects.filter(tipo__in=('AU', 'PA'))
    return render(request, 'certificados/certificados.html', {'ctf_1':ctf_1, 'ctf_2':ctf_2})

def render_to_pdf(request, template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context_dict)

    try:
        pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf()
        return HttpResponse(pdf, content_type='application/pdf')
    except:
        return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

def get_certificado(request, part_id):
    part = get_object_or_404(Certificado, id=part_id)
    if part.tipo in ['PC', 'OG']:
        return render_to_pdf(request, 'certificados/base_certificado.html', {'part': part, 'tipo':tipos[part.tipo]})
    elif part.tipo == 'PA':
        return render_to_pdf(request, 'certificados/base_certificado_palestra.html', {'part': part})
    elif part.tipo == 'POG':
        return render_to_pdf(request, 'certificados/base_certificado_hack.html', {'part': part})
    elif part.tipo == 'PR':
        return render_to_pdf(request, 'certificados/base_certificado_premio.html', {'part': part})
    else:
        return render_to_pdf(request, 'certificados/base_certificado_autor.html', {'part': part})

def busca(request):
    return render(request, 'certificados/busca.html', {})

def bsc(request):
    if request.method == 'POST':

        if request.POST.get('nome') == "":
            return HttpResponse(
                json.dumps({}),
                content_type="application/json"
            )

        response_data = {}
        nome = request.POST.get('nome')
        certi = Certificado.objects.filter(participante__contains=nome).order_by('participante')

        if certi.__len__ == 0:
            return HttpResponse(
                json.dumps({}),
                content_type="application/json"
            )

        rp = {}
        js = {}

        for ct in certi:
            rp = {'%d'%(ct.id): {'nome':ct.participante, 'tipo':tipos[ct.tipo], 'id_c':ct.id}}
            js.update(rp)

        return HttpResponse(json.dumps(js), content_type="application/json")

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

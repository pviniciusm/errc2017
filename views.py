import json
from io import StringIO
from weasyprint import HTML
from xml.sax.saxutils import escape

from django.template import Context

from django.template.loader import get_template
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import render, get_object_or_404

from .models import *
from django.http import HttpResponse


# Create your views here.
@csrf_protect
def minicursos(request):
    ano_corrente = datetime.now().year
    dia_corrente = datetime.now()
    minic = Atividade.objects.filter(tipo='MN', data_inicial__year=ano_corrente).order_by('data_inicial')
    insc = Atividade.objects.filter(tipo__in=['MN', 'OU'], data_inicial__year=ano_corrente, data_inicial__gt=dia_corrente)
    minic_ant = Atividade.objects.filter(tipo='MN').exclude(data_inicial__year=ano_corrente).order_by('data_inicial').reverse()[:2]
    return render(request, 'atividade/minicursos.html', {'minic' : minic, 'minic_ant':minic_ant, 'insc':insc})

cursos = {
    "cc" : "Ciência da Computação",
    "si" : "Sistemas de Informação",
    "sint" : "Sistemas para Internet",
    "rc" : "Redes de Computadores",
    "ec" : "Engenharia de Computação",
    "ou" : "Outro",
}

meses = {
    "1":"Janeiro",
    "2":"Fevereiro",
    "3":"Março",
    "4":"Abril",
    "5":"Maio",
    "6":"Junho",
    "7":"Julho",
    "8":"Agosto",
    "9":"Setembro",
    "10":"Outubro",
    "11":"Novembro",
    "12":"Dezembro",
}


@csrf_protect
def createparticipacao(request):
    if request.method == 'POST':
        response_data = {}

        if request.POST.get('matricula'):
            matricula = int(request.POST.get('matricula'))
        elif not request.POST.get('email'):
#	    print('erro11')
            response_data['result'] = 'ERR'
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            matricula = -1

        if request.POST.get('email'):
            email = request.POST.get('email')
        elif not request.POST.get('matricula'):
            response_data['result'] = 'ERR2'
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            email = ""
        minic = int(request.POST.get('minicurso'))

        try:
            usuario = Aluno.objects.get(matricula=matricula)
            if not usuario.participante:
                usuario.participante = True
            if not usuario.curso == cursos[request.POST.get('curso')]:
                usuario.curso = request.POST.get('curso')

            if not request.POST.get('nome') == "" and not request.POST.get('sobrenome') == "":
                usuario.first_name = request.POST.get('nome')
                usuario.last_name = request.POST.get('sobrenome')

            if email != "":
                usuario.email = email

            usuario.save()

        except:
            try:
                if email != "":
                    usuario = Aluno.objects.get(email=email)
                else:
                    usuario = Aluno.objects.get(email="hsafddsdavalor_nunca_encontrado@gmail.com")

                if not usuario.participante:
                    usuario.participante = True
                if not usuario.curso == cursos[request.POST.get('curso')]:
                    usuario.curso = request.POST.get('curso')
                if not request.POST.get('nome') == "" and not request.POST.get('sobrenome') == "":
                    usuario.first_name = request.POST.get('nome')
                    usuario.last_name = request.POST.get('sobrenome')
                if matricula != -1:
                    usuario.matricula = matricula

                usuario.save()
            except:
                if matricula != -1:
                    username = matricula
                    usuario = Aluno(matricula=matricula, username=username, first_name=request.POST.get('nome'),
                                    last_name=request.POST.get('sobrenome'), email=request.POST.get('email'),
                                    participante=True, curso=cursos[request.POST.get('curso')])
                else:
                    username = email
                    usuario = Aluno(username=username, first_name=request.POST.get('nome'),
                                    last_name=request.POST.get('sobrenome'), email=request.POST.get('email'),
                                    participante=True, curso=cursos[request.POST.get('curso')])

                usuario.save()

        try:
            minicurso = Atividade.objects.get(id=minic, inscricao_aberta=True)
            participacoes = Participacao.objects.filter(atividade=minicurso).count()

            if participacoes < minicurso.maximo_inscritos:
                    try:
                        participacao = Participacao.objects.get(atividade=minicurso, usuario=usuario)
                        response_data['result'] = 'JI'
                    except:
                        participacao = Participacao(atividade=minicurso, usuario=usuario, valido=True)
                        participacao.save()
                        response_data['result'] = 'IC'
            else:
                response_data['result'] = 'LE'

        except:
            response_data['result'] = 'MI'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def minicursos_antigos(request):
    ano_corrente = datetime.now()
    minic_ant = Atividade.objects.filter(tipo='MN').exclude(data_final__gt=ano_corrente).order_by('data_inicial').reverse()
    return render(request, 'atividade/antigos.html', {'minic_ant':minic_ant})


def certificados(request):
    atv = Atividade.objects.filter(certificado_disponivel=True)
    ano = Atividade.objects.dates('data_inicial', 'year').distinct().reverse()
    return render(request, 'atividade/certificados.html', {'anos':ano, 'atv': atv})


def buscacertificados(request):
    if request.method == 'POST':

        if request.POST.get('matricula') == "" or request.POST.get('atividade') == "":
            return HttpResponse(
                json.dumps({}),
                content_type="application/json"
            )

        response_data = {}

        matricula = request.POST.get('matricula')
        atividadeid = int(request.POST.get('atividade'))

        try:
            usuario = Aluno.objects.defer('first_name', 'email', 'id').get(email=matricula)
        except:
            usuario = Aluno.objects.defer('first_name', 'matricula', 'id').get(matricula=matricula)
        atividade = Atividade.objects.defer('nome', 'carga', 'local', 'data_inicial', 'data_final', 'aviso').get(id=atividadeid)
        certificado = Participacao.objects.filter(usuario=usuario, atividade=atividade)

        if certificado.__len__ == 0:
            return HttpResponse(
                json.dumps({}),
                content_type="application/json"
            )

        rp = {}
        js = {}
        for ct in certificado:
            if ct.valido:
                if ct.horas_validas == 0:
                    carga = atividade.carga
                else:
                    carga = ct.horas_validas

                if ct.papel:
                    tipo = ct.papel
                else:
                    tipo = ""

                rp = {'atividade%d'%(ct.id): {'nome':usuario.first_name, 'atividade':atividade.nome, 'tipo':tipo, 'horas':carga, 'data_inicial':'%d/%d/%d'%(atividade.data_inicial.day, atividade.data_inicial.month, atividade.data_inicial.year), 'data_final':'%d/%d/%d'%(atividade.data_final.day, atividade.data_final.month, atividade.data_final.year), 'id': ct.id}}
                js.update(rp)

        return HttpResponse(
            json.dumps(js),
            content_type="application/json"
        )

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def render_to_pdf(request, template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)

    try:
        pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf()
        return HttpResponse(pdf, content_type='application/pdf')
    except:
        return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


def get_certificado(request, part_id):
    part = get_object_or_404(Participacao, id=part_id)
    return render_to_pdf(request, 'certificados/template_pdf.html', {'participacao': part})
ncc@coming:~/portalpetcc/portalpetcc/atividades$ Connection to portal.inf.ufsm.br closed by remote host.

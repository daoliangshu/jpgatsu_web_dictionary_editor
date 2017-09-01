import json

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import login as django_login_view
from django.contrib.auth.views import logout as django_logout_view
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.template import loader, Context
from django.views.generic import FormView

from db_editor.forms import DictionaryEntryForm
from db_editor.forms import SearchEntryForm
from db_editor.models import DictionaryBackUpEntry
from db_editor.models import DictionaryEntry


def home_view(request):
    show_header = True
    username = None
    if request.user.is_authenticated():
        username = request.user.username

    if request.POST.get('fr_1'):
        kargs = {}
        for key, value in request.POST.items():
            if key == 'search_column' or key == 'value':
                continue
            elif key == 'lesson' and int(value) <= 0:
                continue
            elif key == 'thematic' and int(value) < 0:
                continue
            elif key == 'lv' and int(value) <= 0:
                continue
            elif key == 'csrfmiddlewaretoken':
                continue
            else:
                kargs[key + '__contains'] = value
        entries = DictionaryEntry.objects.filter(**kargs)[:30]

    elif request.POST.get('search_column') is not None and request.POST.get('value') is not None:
        col = request.POST['search_column']
        value = request.POST['value']
        if col == 'entry_id' or col == 'lesson' or col == 'lv':
            karg = {col + '__isexact': value}
            entries = DictionaryEntry.objects.filter(karg)[:30]
        else:
            karg = {col + '__contains': value}
            entries = DictionaryEntry.objects.filter(**karg)[:30]
    else:
        entries = DictionaryEntry.objects.all().order_by("entry_id")[:30]

    thematic_choices = DictionaryEntry.thematic_choices
    lv_choices = DictionaryEntry.lv_choices
    form_search = SearchEntryForm()

    data = serializers.serialize('python', entries, fields=('fr_1', 'jp_1', 'jp_2', 'zh_1', 'thematic', 'lesson', 'lv'))
    form = DictionaryEntryForm()
    if form.is_valid():
        print('IS_VALID_FORM')
    return render(request, 'db_editor/interface.html', locals())

def post_new(request):
    form = DictionaryEntryForm()
    return render(request, 'db_editor/post_edit.html', {'form': form})


def ajax_entries_request(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    if request.is_ajax() and request.method == 'POST':
        thematics_selected = request.POST.getlist('thematics[]')
        levels_selected = request.POST.getlist('levels[]')
        fields_selected = request.POST.getlist('search_fields[]')
        search_pattern = request.POST.get('search_pattern')
        print('TEXT: ' + request.POST.get('text', ''))
        print('THEMATICS: ' + str(thematics_selected))
        print('LEVELS: ' + str(levels_selected))
        print('PATTERN: ' + str(search_pattern))
        print('FIELDS: ' + str(fields_selected))
        kargs = {}
        if len(fields_selected) > 0:
            for value in fields_selected:
                kargs[value + '__' + search_pattern] = request.POST.get('text', '')
        else:
            kargs['fr_1' + '__' + search_pattern] = request.POST.get('text', '')
        if len(levels_selected) > 0:
            kargs['lv__in'] = levels_selected
        if len(thematics_selected) > 1:
            kargs['thematic__in'] = thematics_selected
        elif len(thematics_selected) == 1 and thematics_selected != -1:
            kargs['thematic__exact'] = thematics_selected[0]


        entries = DictionaryEntry.objects.filter(**kargs)[:400]
        data = serializers.serialize('python', entries,
                                     fields=('fr_1', 'jp_1', 'jp_2', 'zh_1', 'thematic', 'lesson', 'lv'))
        lv_choices = DictionaryEntry.lv_choices
        thematic_choices = DictionaryEntry.thematic_choices
    return render_to_response('db_editor/populate_entries.html', locals())


def ajax_update_request(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    if request.is_ajax() and request.method == 'POST':
        my_data = {
            'entry_id': request.POST.get('entry_id', ''),
            'fr_1': request.POST.get('fr_1', ''),
            'jp_1': request.POST.get('jp_1', ''),
            'jp_2': request.POST.get('jp_2', ''),
            'zh_1': request.POST.get('zh_1', ''),
            'thematic': request.POST.get('thematic', -1),
            'lv': request.POST.get('lv', 0)
        }

        if len(my_data['entry_id']) <= 0:
            my_data.pop('entry_id', '')

        if 'entry_id' in my_data.keys():
            my_entry_id = my_data.pop('entry_id')
            print('my_data: ' + str(my_data))
            print('entri+id: ' + my_entry_id)
            print('thematic : ' + str(my_data['thematic']))
            DictionaryEntry.objects.filter(entry_id=int(my_entry_id)).update(**my_data)
        else:
            DictionaryEntry.objects.create(my_data)
        lv_choices = DictionaryEntry.lv_choices
        thematic_choices = DictionaryEntry.thematic_choices
        kargs = {'fr_1__exact': my_data['fr_1'],
                 'jp_1__contains': my_data['jp_1'],
                 'jp_2__contains': my_data['jp_2']}
        entries = DictionaryEntry.objects.filter(**kargs)[:4]
        data = serializers.serialize('python', entries,
                                     fields=('jp_1', 'jp_2', 'zh_1', 'fr_1', 'lesson', 'lv', 'thematic'),
                                     )
        return render_to_response('db_editor/populate_entries.html', locals())

    return HttpResponse(json.dumps(my_data['fr_1']), content_type='application/javascript')


def ajax_remove_request(request):
    if request.is_ajax() and request.method == 'POST':
        my_data = {
            'entry_id': request.POST.get('entry_id', ''),
            'fr_1': request.POST.get('fr_1', ''),
            'jp_1': request.POST.get('jp_1', ''),
            'jp_2': request.POST.get('jp_2', ''),
            'zh_1': request.POST.get('zh_1', ''),
            'thematic': request.POST.get('thematic', -1),
            'lv': request.POST.get('lv', -1)
        }

        if 'entry_id' in my_data.keys():
            my_entry = DictionaryEntry.objects.filter(entry_id=my_data['entry_id']).delete()
            DictionaryBackUpEntry.objects.create(**my_data)
    return HttpResponse(json.dumps(my_data['fr_1']), content_type='application/javascript')


def get_dictionary_as_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=jpgatsu_dic.csv'

    entries = DictionaryEntry.objects.all()
    data = []
    for entry in entries:
        data.append((entry.entry_id,
                     entry.fr_1,
                     entry.jp_1,
                     entry.jp_2,
                     entry.zh_1,
                     entry.en_1,
                     entry.lesson,
                     entry.thematic,
                     entry.lv,
                     entry.date)
                    )

    t = loader.get_template('db_editor/csv_template.txt')
    c = Context({
        'data': data,
    })

    csv_from_html = t.render(c)
    print('out:  ' + csv_from_html)
    print('out length: ' + str(len(csv_from_html)))
    response['Content-Length'] = len(csv_from_html)
    response.write(csv_from_html)
    return response


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'db_editor/login.html'

    def form_valid(self, form):
        usuario = form.get_user()

        django_login_view(self.request, usuario)
        return redirect('/editor/home')
        # return super(LoginView, self).form_valid(form)


def logout_view(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    django_logout_view(request)
    return render_to_response('registration/logged_out.html', locals())


def register(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()

    return render_to_response('registration/register.html', locals())

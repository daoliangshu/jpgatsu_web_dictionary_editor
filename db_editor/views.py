import json

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import login as django_login_view
from django.contrib.auth.views import logout as django_logout_view
from django.core import serializers
from django.db.models import Q
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
        current_page = 0
        request.session['current_page'] = 0

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
        # entries = DictionaryEntry.objects.filter(**kargs)[:30]

        and_filter, or_filter = get_search_filters(request)
        res_count = get_entry_count_by_filters(and_filter, or_filter)
        entries = get_entries_by_filters(and_filter, or_filter, 0)
        # res_count =int(DictionaryEntry.objects.filter(**kargs).count())
        last_page = res_count // 30

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
        res_count = int(DictionaryEntry.objects.all().order_by("entry_id").count())
        last_page = res_count // 30
    request.session['last_page'] = last_page
    thematic_choices = DictionaryEntry.thematic_choices
    lv_choices = DictionaryEntry.lv_choices
    form_search = SearchEntryForm()

    data = serializers.serialize('python', entries,
                                 fields=('fr_1', 'fr_2', 'jp_1', 'jp_2', 'zh_1', 'thematic', 'lesson', 'lv'))
    form = DictionaryEntryForm()
    if form.is_valid():
        print('IS_VALID_FORM')
    return render(request, 'db_editor/interface.html', locals())

def post_new(request):
    form = DictionaryEntryForm()
    return render(request, 'db_editor/post_edit.html', {'form': form})


def ajax_next_page(request):
    if request.user.is_authenticated():
        current_page = request.session['current_page']
    else:
        current_page = 0
    current_page = current_page + 1
    request.session['current_page'] = current_page
    return ajax_get_page(request, current_page)


def ajax_previous_page(request):
    if request.user.is_authenticated():
        current_page = request.session['current_page']
    else:
        current_page = 0
    if current_page > 0:
        current_page = current_page - 1
    request.session['current_page'] = current_page
    return ajax_get_page(request, current_page)


def get_entries_by_filters(and_filter, or_filter, which_page):
    if len(and_filter) > 0:
        entries = DictionaryEntry.objects.filter(**and_filter)
        return entries.filter(or_filter)[30 * which_page:30 * which_page + 30]
    else:
        return DictionaryEntry.objects.filter(or_filter)[30 * which_page:30 * which_page + 30]


def get_entry_count_by_filters(and_filter, or_filter):
    if len(and_filter) > 0:
        return DictionaryEntry.objects.filter(**and_filter).filter(or_filter).count()
    else:
        return DictionaryEntry.objects.filter(or_filter).count()


def ajax_get_page(request, which_page):
    if request.user.is_authenticated():
        username = request.user.username
        field_args = request.session['filter1']
        and_filter = request.session['filter2']
        entry_per_page = request.session['entry_per_page']
        last_page = request.session['last_page']
        current_page = which_page
        field_filter = Q()
        for item in field_args:
            field_filter |= Q(**{item: field_args[item]})

        entries = get_entries_by_filters(and_filter, field_filter, which_page)
        data = serializers.serialize('python', entries,
                                     fields=(
                                     'fr_2', 'fr_1', 'jp_1', 'jp_2', 'zh_1', 'thematic', 'lesson', 'lv', 'date'))
        lv_choices = DictionaryEntry.lv_choices
        thematic_choices = DictionaryEntry.thematic_choices

        return render_to_response('db_editor/populate_entries.html', locals())


def get_search_filters(request):
    thematics_selected = request.POST.getlist('thematics[]', [])
    levels_selected = request.POST.getlist('levels[]', [])
    fields_selected = request.POST.getlist('search_fields[]', [])
    search_pattern = request.POST.get('search_pattern', 'starts_with')
    field_args = {}
    and_filter = {}


        if len(fields_selected) > 0:
            for value in fields_selected:
                field_args[value + '__' + search_pattern] = request.POST.get('text', '')
        else:
            field_args['fr_1' + '__' + search_pattern] = request.POST.get('text', '')
        if len(levels_selected) > 0:
            and_filter['lv__in'] = levels_selected
        if len(thematics_selected) > 1:
            and_filter['thematic__in'] = thematics_selected
        elif len(thematics_selected) == 1 and thematics_selected != -1:
            and_filter['thematic__exact'] = thematics_selected[0]

    field_filter = Q()
    for item in field_args:
        if 'thematic' not in item and 'level' not in item:
            field_filter |= Q(**{item: field_args[item]})

    request.session['filter1'] = field_args
    request.session['filter2'] = and_filter
    return and_filter, field_filter


def ajax_entries_request(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    if request.is_ajax() and request.method == 'POST':
        and_filter, or_filter = get_search_filters(request)

        if len(and_filter) > 0:
            entries = DictionaryEntry.objects.filter(**and_filter)
            entries = entries.filter(or_filter)
        else:
            entries = DictionaryEntry.objects.filter(or_filter)
        entry_count = len(entries)
        data = serializers.serialize('python', entries[0:30],
                                     fields=(
                                     'fr_1', 'fr_2', 'jp_1', 'jp_2', 'zh_1', 'thematic', 'lesson', 'lv', 'date'))
        current_page = 0
        entry_per_page = 30
        request.session['current_page'] = current_page
        request.session['entry_per_page'] = entry_per_page
        last_page = get_entry_count_by_filters(and_filter, or_filter) // entry_per_page
        request.session['last_page'] = last_page
        if len(entries) == 31:
            request.session['has_next'] = True
        else:
            request.session['has_next'] = False

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
            'fr_2': request.POST.get('fr_2', ''),
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
            DictionaryEntry.objects.create(**my_data)
        lv_choices = DictionaryEntry.lv_choices
        thematic_choices = DictionaryEntry.thematic_choices
        kargs = {'fr_1__exact': my_data['fr_1'],
                 'jp_1__contains': my_data['jp_1'],
                 'jp_2__contains': my_data['jp_2']}
        entries = DictionaryEntry.objects.filter(**kargs)[:4]
        data = serializers.serialize('python', entries,
                                     fields=('jp_1', 'jp_2', 'zh_1', 'fr_1', 'fr_2', 'lesson', 'lv', 'thematic'),
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
    print('Number Entries Passed: ' + str(len(entries)))
    # Data passed information at first line
    data.append((str(len(entries)),
                 None,
                 None,
                 None,
                 None,
                 None,
                 None,
                 None,
                 None,
                 None
                 ))

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
    # print('out length: ' + str(len(csv_from_html)))
    #response['Content-Length'] = len(csv_from_html)
    response.write(csv_from_html)
    response['Content-Length'] = len(response.content)
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

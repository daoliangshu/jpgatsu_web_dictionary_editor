import json
from datetime import datetime

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response

from db_editor.forms import DictionaryEntryForm
from db_editor.forms import SearchEntryForm
from db_editor.models import DictionaryEntry


def getCurrentDate(request):
    data = datetime.now()
    print(str(request.POST))
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
            print(karg)
            entries = DictionaryEntry.objects.filter(**karg)[:30]
    else:
        entries = DictionaryEntry.objects.all().order_by("entry_id")[:30]

    thematic_choices = DictionaryEntry.thematic_choices
    form_search = SearchEntryForm()
    data = serializers.serialize('python', entries, fields=('fr_1', 'jp_1', 'jp_2', 'zh_1', 'thematic', 'lesson', 'lv'))
    form = DictionaryEntryForm()
    if form.is_valid():
        print('IS_VALID_FORM')
    return render(request, 'db_editor/date.html', locals())


def home(request):
    mutable = request.POST._mutable
    request.POST._mutable = True
    request.POST['search_column'] = 'fr_1'
    request.POST['value'] = 'vi'
    request.POST._mutable = mutable
    return getCurrentDate(request)


def post_new(request):
    form = DictionaryEntryForm()
    return render(request, 'db_editor/post_edit.html', {'form': form})


def ajax_entries_request(request):
    if request.is_ajax() and request.method == 'POST':
        print('TEXT_RECEIVED: ' + request.POST.get('text', ''))
        entries = DictionaryEntry.objects.filter(fr_1__startswith=request.POST.get('text', ''))[:30]
        data = serializers.serialize('python', entries,
                                     fields=('jp_1', 'jp_2', 'zh_1', 'fr_1', 'lesson', 'lv', 'thematic'),
                                     use_natural_primary_keys=True)
        lv_choices = DictionaryEntry.lv_choices
        thematic_choices = DictionaryEntry.thematic_choices
    return render_to_response('db_editor/populate_entries.html', locals())


def ajax_update_request(request):
    if request.is_ajax() and request.method == 'POST':
        my_data = request.POST.get('entry_id', '')
        print("UPDATE : " + str(my_data))
    return HttpResponse(json.dumps(my_data), content_type='application/javascript')

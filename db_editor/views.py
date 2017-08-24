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
        thematics_selected = request.POST.getlist('thematics[]')
        levels_selected = request.POST.getlist('levels[]')
        print('TEXT: ' + request.POST.get('text', ''))
        print('THEMATICS: ' + str(thematics_selected))
        print('LEVELS: ' + str(levels_selected))
        kargs = {'fr_1__startswith': request.POST.get('text', '')
                 }
        if len(levels_selected) > 0:
            kargs['lv__in'] = levels_selected
        if len(thematics_selected) > 0:
            kargs['thematic__in'] = thematics_selected

        entries = DictionaryEntry.objects.filter(**kargs)[:400]



        data = serializers.serialize('python', entries,
                                     fields=('jp_1', 'jp_2', 'zh_1', 'fr_1', 'lesson', 'lv', 'thematic'),
                                     use_natural_primary_keys=True)
        lv_choices = DictionaryEntry.lv_choices
        thematic_choices = DictionaryEntry.thematic_choices
    return render_to_response('db_editor/populate_entries.html', locals())


def ajax_update_request(request):
    if request.is_ajax() and request.method == 'POST':
        my_data = {
            'entry_id': request.POST.get('entry_id', ''),
            'fr_1': request.POST.get('fr_1', ''),
            'jp_1': request.POST.get('jp_1', ''),
            'jp_2': request.POST.get('jp_2', ''),
            'zh_1': request.POST.get('zh_1', ''),
            'thematic': request.POST.get('thematic', ''),
            'lv': request.POST.get('lv', '')
        }
        print(str(my_data))
        if len(my_data['entry_id']) <= 0:
            my_data.pop('entry_id', '')
            lv = 0
            lv_as_str = my_data.get('lv', '')
            for i in range(len(DictionaryEntry.lv_choices)):
                print('value: ' + DictionaryEntry.lv_choices[i][1] + " vs " + lv_as_str)
                if DictionaryEntry.lv_choices[i][1] == lv_as_str:
                    lv = i
                    break
            thematic_as_str = my_data.get('thematic', '')
            thematic = -1
            for i in range(len(DictionaryEntry.thematic_choices)):
                print('value: ' + DictionaryEntry.thematic_choices[i][1] + " vs " + thematic_as_str)
                if DictionaryEntry.thematic_choices[i][1] == thematic_as_str:
                    thematic = i
                    break

            print(str(lv))
            DictionaryEntry.objects.create(fr_1=my_data['fr_1'],
                                           zh_1=my_data['zh_1'],
                                           jp_1=my_data['jp_1'],
                                           jp_2=my_data['jp_2'],
                                           lv=lv,
                                           thematic=thematic
                                           )
            lv_choices = DictionaryEntry.lv_choices
            thematic_choices = DictionaryEntry.thematic_choices
            kargs = {'fr_1__exact': my_data['fr_1'],
                     'jp_1__contains': my_data['jp_1'],
                     'jp_2__contains': my_data['jp_2']}
            entries = DictionaryEntry.objects.filter(**kargs)[:400]
            data = serializers.serialize('python', entries,
                                         fields=('jp_1', 'jp_2', 'zh_1', 'fr_1', 'lesson', 'lv', 'thematic'),
                                         use_natural_primary_keys=True)
            return render_to_response('db_editor/populate_entries.html', locals())

    return HttpResponse(json.dumps(my_data['fr_1']), content_type='application/javascript')

from django import forms

from .models import DictionaryEntry


class DictionaryEntryForm(forms.ModelForm):
    class Meta:
        model = DictionaryEntry
        fields = ('jp_1', 'jp_2', 'zh_1', 'fr_1', 'fr_2', 'thematic', 'lesson', 'lv')


class SearchEntryForm(forms.Form):
    text = forms.CharField(max_length=50,
                           widget=forms.Textarea(attrs={'onkeyup': 'get_entries();', 'rows': 1}))

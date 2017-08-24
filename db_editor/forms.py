from django import forms

from .models import DictionaryEntry


class DictionaryEntryForm(forms.ModelForm):
    class Meta:
        model = DictionaryEntry
        fields = ('jp_1', 'jp_2', 'zh_1', 'fr_1', 'fr_2', 'thematic', 'lesson', 'lv')


class SearchEntryForm(forms.Form):
    text = forms.CharField(max_length=50,
                           widget=forms.Textarea(
                               attrs={'onkeypress': 'enterSearchBarKeyPress(event)',
                                      'rows': 1}))
    lv_choices = DictionaryEntry.lv_choices
    my_level = forms.MultipleChoiceField(widget=forms.SelectMultiple(), choices=lv_choices)
    thematic_choices = DictionaryEntry.thematic_choices
    my_thematic = forms.MultipleChoiceField(widget=forms.SelectMultiple(), choices=thematic_choices)

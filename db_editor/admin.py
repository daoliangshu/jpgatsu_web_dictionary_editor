from django.contrib import admin

from .models import DictionaryEntry


# Register your models here.



class DictionaryEntryAdmin(admin.ModelAdmin):
    list_display = ('fr_1', 'jp_1', 'zh_1', 'thematic')


admin.site.register(DictionaryEntry, DictionaryEntryAdmin)

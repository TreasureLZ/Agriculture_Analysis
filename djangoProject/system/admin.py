from django.contrib import admin
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Agriculture, Meteorology


class ExportExcelMixin(object):
    def export_as_excel(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields][1:]
        field_verbose_names = [field.verbose_name for field in meta.fields][1:]
        response = HttpResponse(content_type='application/msexcel')
        filename = self.model._meta.verbose_name
        response['Content-Disposition'] = f'attachment; filename={filename.encode("utf-8").decode("ISO-8859-1")}.xlsx'
        wb = Workbook()
        ws = wb.active
        ws.append(field_verbose_names)
        for obj in queryset:
            data = []
            for field in field_names:
                if hasattr(obj, f'get_{field}_display'):
                    value = getattr(obj, f'get_{field}_display')()
                else:
                    value = getattr(obj, field)
                data.append(f'{value}')
            ws.append(data)
        wb.save(response)
        return response

    export_as_excel.short_description = '导出Excel'
    export_as_excel.type = 'success'


class ControlAgriculture(admin.ModelAdmin, ExportExcelMixin):
    list_display = ['area', 'value', 'unit', 'zb', 'updateTime']
    ordering = ['area']
    list_filter = ['area','zb']
    list_per_page = 20
    actions = ['export_as_excel']


class ControlMeteorology(admin.ModelAdmin, ExportExcelMixin):
    list_display = ['city', 'month', 'avg_max_temperature', 'avg_min_temperature', 'avg_precipitation',
                    'histroy_max_temperature',
                    'histroy_min_temperature']
    ordering = ['city']
    list_filter = ['city']
    list_per_page = 20
    actions = ['export_as_excel']


admin.site.register(Agriculture, ControlAgriculture)
admin.site.register(Meteorology, ControlMeteorology)
admin.site.site_header = '农业生产可视化系统'
admin.site.site_title = '农业生产可视化系统'
admin.site.index_title = '农业生产可视化系统'

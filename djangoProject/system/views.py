from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from .models import Agriculture,Meteorology

@login_required(login_url='/login/')
def index(request):
    zb_results = Agriculture.objects.values_list('zb', flat=True).distinct()
    zb = request.GET.get('zb')
    qh = request.GET.get('qh')
    selectTime = request.GET.get('selectTime')
    if not selectTime:
        selectTime = '近5年'
    qh_data = {'avg_max_temperature': {}, 'avg_min_temperature': {},'avg_precipitation':{}}
    context = {'direction':'','zb_results':zb_results,'zb':zb,'qh':qh,'year_results':[],'year_data':[],'area_results':[],'area_data':[],'unit':'','qh_data':qh_data}
    if zb:
        context['direction'] = 'zb'
        all_results = Agriculture.objects.all().filter(zb=zb)
        unit = Agriculture.objects.all().filter(zb=zb).values_list('unit', flat=True).distinct()[0]
        year_results = list(all_results.values_list('updateTime', flat=True).distinct())
        if selectTime:
            selectTime_dict = {'近5年': 5, '近10年': 10, '近20年': 20}
            year_results = year_results[0:selectTime_dict[selectTime]]
        year_data = {}
        flag = 0
        for year in year_results:
            total_value = Agriculture.objects.all().filter(zb=zb).filter(updateTime=year).aggregate(value_sum=Sum('value'))
            value_sum = round(total_value['value_sum'],2)
            if value_sum == 0:
                flag += 1
                continue
            year_data[year] = value_sum
        year_results = year_results[flag:selectTime_dict[selectTime]]
        area_results = list(all_results.values_list('area',flat=True).distinct())
        area_data = {}
        for area in area_results:
            temp = [round(eval(_),2) for _ in list(all_results.filter(area=area).values_list('value',flat=True))]
            temp = temp[flag:selectTime_dict[selectTime]]
            area_data[area] = temp
        context['year_results'] = year_results
        context['year_data'] = year_data
        context['area_results'] = area_results
        context['area_data'] = area_data
        context['unit'] = unit
    elif qh:
        context['direction'] = 'qh'
        provincial = {'北京': '北京', '天津': '天津', '上海': '上海', '重庆': '重庆', '沈阳': '辽宁', '哈尔滨': '黑龙江', '长春': '吉林', '南京': '江苏', '杭州': '浙江', '合肥': '安徽', '福州': '福建', '南昌': '江西', '济南': '山东', '郑州': '河南', '武汉': '湖北', '长沙': '湖南', '广州': '广东', '南宁': '广西', '海口': '海南', '成都': '四川', '贵阳': '贵州', '昆明': '云南', '西安': '陕西', '兰州': '甘肃', '西宁': '青海', '银川': '宁夏', '太原': '山西', '呼和浩特': '内蒙古', '拉萨': '西藏', '台北': '台湾', '香港': '香港', '澳门': '澳门', '石家庄': '河北','乌鲁木齐':'新疆'}
        month_list = list(Meteorology.objects.all().values_list('month', flat=True).distinct())
        for month in month_list:
            qh_data['avg_max_temperature'][month] = []
            qh_data['avg_min_temperature'][month] = []
            qh_data['avg_precipitation'][month] = []
            city_precipitation = ['北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '上海', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州', '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆']
            for city in provincial.keys():
                results = Meteorology.objects.all().filter(city=city).filter(month=month).values('avg_max_temperature','avg_min_temperature', 'avg_precipitation')[0]
                city = provincial[city]
                if city in city_precipitation:
                    qh_data['avg_precipitation'][month].append({'name':city,'value':results['avg_precipitation'].replace('mm','')})
                qh_data['avg_max_temperature'][month].append({'name':city,'value':results['avg_max_temperature'].replace('℃','')})
                qh_data['avg_min_temperature'][month].append({'name': city, 'value': results['avg_min_temperature'].replace('℃', '')})
    return render(request,'index.html',context=context)

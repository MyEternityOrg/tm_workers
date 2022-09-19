from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from extworkers.models import *
from outsourcing.models import *
from datetime import date, datetime, timedelta, time


# Create your views here.

@login_required
def report_act_service(request):
    dts_begin = request.GET.get('dts_begin')
    dts_end = request.GET.get('dts_end')
    contractor = request.GET.get('contractor')

    if dts_begin is None or dts_end is None:
        contex = {'dts_begin': date.today(),
                  'dts_end': date.today()}
        return render(request, 'act_service/act_service.html', contex)

    extwork = ExtWorkerRecord.objects.filter(dts__gte=dts_begin, dts__lte=dts_end)

    list_price = OutsourcingPrices.objects.raw("select * from [get_outsourcing_prices_offset] (%s)", [dts_end])

    init = list(
        map(lambda i: {'enterprise': i, 'price': list(filter(lambda t: t.enterprise == i, list(list_price)))[0].price,
                       'f_h': sum(list(map(lambda y: (datetime.strptime(str(y.t_time), "%H:%M:%S") - datetime.strptime(
                           str(y.f_time), "%H:%M:%S")).seconds / 60 / 60,
                                           list(filter(lambda t: t.enterprise == i, list(extwork))))))},
            sorted(set(map(lambda x: x.enterprise, list(filter(lambda x: x.contractor_id == contractor, list(list_price))))),key=lambda s:s.enterprise_code)))

    total = 0
    for i in init:
        i['sum'] = i['price']*i['f_h']
        i['total'] = i['sum']
        total += i['sum']


    contex = {'init': init,
              'contractor': OutsourcingContractors.objects.get(guid=contractor),
              'dts_end': dts_end,
              'total': total}

    return render(request, 'act_service/part_act_service.html', contex)


def select_contractor(request):
    TYPE_PRR = '99C0A151-0D85-439E-81B4-8BE403554DD9'

    list_contr = OutsourcingContractors.objects.filter(outsourcing_type=TYPE_PRR)

    return render(request, 'outsourcing_select_contractors.html', {'object_list': list_contr,})
# coding=utf-8
from django.http import Http404
from django.shortcuts import render_to_response
from django.db.models import Q
from ytenx.helpers.paginator import Paginator
from django.core.paginator import InvalidPage, EmptyPage
from models import SieuxYonh, CjengMux, YonhMux, YonhMiukDzip, CjengLyih, DrakDzuonDang, YonhMiuk, DciangxDzih, GhraxDzih, Dzih, YonhCjep, YonhGheh

def index_page(request):
  return render_to_response('kyonh/index.html')

def intro_page(request):
  return render_to_response('kyonh/intro.html')

def sieux_yonh_page(request, ziox):
  try:
    sieux_yonh = SieuxYonh.objects.get(ziox=ziox)
  except:
    raise Http404()

  return render_to_response('kyonh/sieux_yonh.html', {
    'sieux_yonh': sieux_yonh,
  })

def sieux_yonh_list_page(request):
  cjeng = request.GET.get('cjeng')
  yonh = request.GET.get('yonh')
  deuh = request.GET.get('deuh')
  tongx = request.GET.get('tongx')
  ho = request.GET.get('ho')
  
  query = Q()
  if cjeng:
    query &= Q(cjeng = CjengMux.objects.get(dzih=cjeng))
  if yonh:
    query &= Q(yonhMiuk__in = YonhMiuk.objects.filter(
      gheh = YonhGheh.objects.get(dzih=yonh)
    ))
  if deuh:
    query &= Q(yonhMiuk__in = YonhMiuk.objects.filter(
      deuh = deuh
    ))
  if tongx:
    query &= Q(yonh__in = YonhMux.objects.filter(
      tongx = tongx
    ))
  if ho:
    query &= Q(yonh__in = YonhMux.objects.filter(
      ho = ho
    ))
  
  sieux_yonh_pieux = SieuxYonh.objects.filter(query).order_by('ziox')
  paginator = Paginator(sieux_yonh_pieux, 15)
  try:
    sieux_yonh_pieux = paginator.page(request.GET)
  except (EmptyPage, InvalidPage):
    raise Http404()
  
  cjeng_pieux = []
  for lyih in CjengLyih.objects.all():
    cjeng_pieux.append(lyih)
    cjeng_pieux += lyih.cjengmux_set.all()
  
  yonh_pieux = []
  for cjep in YonhCjep.objects.all():
    yonh_pieux.append(cjep)
    yonh_pieux += cjep.yonhgheh_set.all()
  
  return render_to_response('kyonh/sieux_yonh_pieux.html', {
    'sieux_yonh_pieux': sieux_yonh_pieux,
    'cjeng_pieux': cjeng_pieux,
    'yonh_pieux': yonh_pieux,
    'p_cjeng': cjeng,
    'p_yonh': yonh,
    'p_deuh': deuh,
    'p_tongx': tongx,
    'p_ho': ho,
  })

def dzih(request, ziox):
  try:
    dzih = Dzih.objects.get(ziox=ziox)
  except:
    raise Http404()

  return render_to_response('kyonh/dzih.html', {
    'dzih': dzih,
  })

def dzih_pieux(request):
  dzih_pieux = Dzih.objects.all()
  paginator = Paginator(dzih_pieux, 15)
  try:
    dzih_pieux = paginator.page(request.GET)
  except (EmptyPage, InvalidPage):
    raise Http404()
  return render_to_response('kyonh/dzih_pieux.html', {
    'dzih_pieux': dzih_pieux,
  })

def cjeng_mux_list_page(request):
  return render_to_response('kyonh/cjeng_mux_list.html', {
    'cjeng_mux_list': CjengMux.objects.all(),
  })

def yonh_mux_list_page(request):
  return render_to_response('kyonh/yonh_mux_list.html', {
    'yonh_mux_list': YonhMux.objects.get_pairs(),
  })

def yonh_miuk_list_page(request):
  return render_to_response('kyonh/yonh_miuk_list.html', {
    'yonh_miuk_list': YonhMiukDzip.objects.all(),
  })

def cjeng_ngix_list_page(request):
  return render_to_response('kyonh/cjeng_ngix_list.html', {
    'cjeng_mux_list': CjengMux.objects.all(),
  })

def yonh_ngix_list_page(request):
  return render_to_response('kyonh/yonh_ngix_list.html', {
    'yonh_mux_list': YonhMux.objects.get_pairs(),
  })

def yonh_do_page(request):
  page = int(request.GET.get('page', '1'))
  paginator = Paginator(YonhMiukDzip.objects.all(), 1)
  try:
    dzip_list = paginator.page(page)
  except (EmptyPage, InvalidPage):
    raise Http404()

  dzip = dzip_list[0]
  yonh_do = SieuxYonh.objects.get_yonh_do(dzip)

  return render_to_response('kyonh/yonh_do.html', {
    'yonh_do': yonh_do,
    'cjeng_lyih_list': CjengLyih.objects.all(),
    'dzip': dzip,
    'dzip_list': dzip_list,
  })

def cio_page(request, kyenh, jep):
  cio = DrakDzuonDang.objects.get(
    kyenh = kyenh,
    jep = jep,
  )
  
  return render_to_response('kyonh/cio.html', {
    'cio': cio,
  })

def cjeng_mux_page(request, dzih):
  try:
    cjeng = CjengMux.objects.get(dzih = dzih)
  except:
    raise Http404()

  return render_to_response('kyonh/cjeng_mux.html', {
    'cjeng': cjeng,
  })

def yonh_mux_page(request, mjeng):
  try:
    yonh = YonhMux.objects.get(mjeng = mjeng)
  except:
    raise Http404()

  return render_to_response('kyonh/yonh_mux.html', {
    'yonh': yonh,
  })

def yonh_miuk_page(request, dzih):
  try:
    yonh_miuk = YonhMiuk.objects.get(dzih = dzih)
  except:
    raise Http404()

  return render_to_response('kyonh/yonh_miuk.html', {
    'yonh_miuk': yonh_miuk,
  })

def pyanx_dciangx_page(request, dzih):
  try:
    dciangx = DciangxDzih.objects.get(dzih = dzih)
  except:
    raise Http404()

  return render_to_response('kyonh/pyanx_dciangx.html', {
    'dciangx': dciangx,
  })

def pyanx_ghrax_page(request, dzih):
  try:
    ghrax = GhraxDzih.objects.get(dzih = dzih)
  except:
    raise Http404()

  return render_to_response('kyonh/pyanx_ghrax.html', {
    'ghrax': ghrax,
  })

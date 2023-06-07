from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect

from ..forms import RegionForm
from ..models import Region, District


@login_required(login_url='/')
def location(request):
    get_region = Region.objects.annotate(num_districts=Count('region_districts')).values('name', 'num_districts', 'id')
    get_district = District.objects.all().order_by('name')

    context = {
        'regions': get_region,
        'districts': get_district
    }

    return render(request, 'pages/location.html', context)


@login_required(login_url='/')
def save_district(request):
    if request.method == 'POST':
        name = request.POST['name']
        region_id = request.POST['region_id']
        region = Region.objects.filter(id=region_id).first()

        district_instance = District(name=name, region=region)
        district_instance.save()

        return redirect('location')


@login_required(login_url='/')
def save_region(request):
    if request.method == 'POST':
        form = RegionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('location')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Medicines
# Create your views here.
def home(request):
    med = Medicines.objects.all()
    context = {'medicines':med}
    return render(request,"index.html", context)

    
def add_prod(request):
    if request.method == 'POST':
        name = request.POST.get('m_name')
        description =request.POST.get('m_dec')
        price = request.POST.get('m_price')
        image = request.POST.get('m_img')

        Medicines.objects.create(
            name = name,
            description = description,
            price = price,
            image = image,
        )
        return redirect('home')

    return render(request, 'add_prod.html')

   
def update_prod(request,pk):
    dawai = get_object_or_404(Medicines, pk = pk )
    if request.method == 'POST':
        name = request.POST.get('m_name')
        description =request.POST.get('m_dec')
        price = request.POST.get('m_price')
        image = request.POST.get('m_img')

        dawai.name = name
        dawai.description = description
        dawai.price = price
        dawai.image = image

        dawai.update()

        return redirect('home')

    context = {'dawai':dawai}
    return render(request, 'update_prod.html', context)

from urllib import response

from django.shortcuts import redirect, render,HttpResponse
from PIL import Image
import io
from django.contrib.auth.decorators import login_required
from .forms import CompressImageForm

# Create your views here.
@login_required(login_url='login')
def compress(request):
    user = request.user
    if request.method == 'POST':
        form = CompressImageForm(request.POST,request.FILES)
        if form.is_valid():
            original_image = form.cleaned_data['original_image']
            quality = form.cleaned_data['quality']
            compressed_image = form.save(commit=False)
            compressed_image.user = user

            # Compress the image using Pillow
            img = Image.open(original_image)
            output_format = img.format
            buffer = io.BytesIO()
            
            img.save(buffer,format=output_format, quality=quality)
            buffer.seek(0)
            # Save the compressed image to the model
            compressed_image.compressed_image.save(
                f'compressed_{original_image}',
                buffer
            )
            # automatically download the compressed image
            responce = HttpResponse(buffer.getvalue(),content_type=f'image/{output_format.lower()}')
            responce['content-disposition'] = f"attachment; filename=compressed_{original_image}"
            return responce
            #return redirect('compress')

    form = CompressImageForm()
    context={
        'form' : form
    }
    return render(request, 'image_compression/compress.html',context)
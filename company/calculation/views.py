# from django.shortcuts import render
# from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from calculation.models import Document
from calculation.forms import DocumentForm
from django.shortcuts import render
import pandas as pd
import os


def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            
            docfile = request.FILES['docfile']
            newdoc=Document(docfile = request.FILES['docfile'])
            newdoc.save()
            p=os.path.abspath(docfile.name)
            k=str(docfile.name)
            
            df = pd.read_csv(p, header=0,encoding = "ISO-8859-1")
            numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
            newdf = df.select_dtypes(include=numerics)
            df1=newdf.mean(axis=0)
            df2=newdf.append(df1,ignore_index=True)
            a=df2.to_string(buf=None, columns=None, col_space=None, header=True, index=True, na_rep='NaN', formatters=None, float_format=None, sparsify=None, index_names=True, justify=None, line_width=None, max_rows=None, max_cols=None, show_dimensions=False)
            b = bytes(a, 'utf-8')
            ss='/company/media/documents/'+str(k)
            with open(ss, 'wb+') as f:
                f.write(b)
            
            
            
            

            # Redirect to the document list after POST
            # return HttpResponseRedirect(reverse('myapp.views.list'))
    else:
        form = DocumentForm()
        

    # Load documents for the list page
    documents = Document.objects.all()
    
    

    # Render list page with the documents and the form
    return render(request,'list1.html',
        {'documents': documents, 'form': form})          
			

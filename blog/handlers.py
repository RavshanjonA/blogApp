from django.shortcuts import render


def handler_404(request, exception):
    return render(request, "blog/404.html")

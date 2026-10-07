from django.shortcuts import render

from .processing import FILTERS, process_image


def home(request):
    context = {"filters": FILTERS, "selected_filter": "gaussian", "kernel_size": 5, "low_threshold": 50, "high_threshold": 150}
    if request.method == "POST":
        upload = request.FILES.get("image")
        context.update({
            "selected_filter": request.POST.get("filter", "gaussian"),
            "kernel_size": request.POST.get("kernel_size", "5"),
            "low_threshold": request.POST.get("low_threshold", "50"),
            "high_threshold": request.POST.get("high_threshold", "150"),
        })
        if not upload:
            context["error"] = "Choose an image to process."
        elif upload.size > 10 * 1024 * 1024:
            context["error"] = "Image must be 10 MB or smaller."
        else:
            try:
                kernel = int(context["kernel_size"])
                low, high = int(context["low_threshold"]), int(context["high_threshold"])
                if context["selected_filter"] not in FILTERS:
                    raise ValueError("Choose one of the available filters.")
                if kernel < 3 or kernel > 31 or kernel % 2 == 0:
                    raise ValueError("Kernel size must be an odd number from 3 to 31.")
                if not (0 <= low < high <= 255):
                    raise ValueError("Thresholds must satisfy 0 ≤ low < high ≤ 255.")
                context["stages"] = process_image(upload.read(), context["selected_filter"], kernel, low, high)
                context["filter_label"] = FILTERS[context["selected_filter"]]
            except (ValueError, TypeError) as exc:
                context["error"] = str(exc)
    return render(request, "pipeline/index.html", context)

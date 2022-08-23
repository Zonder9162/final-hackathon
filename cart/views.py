# from django.shortcuts import render, redirect, get_object_or_404
# from django.views.decorators.http import require_POST
# from toys.models import Toy
# from .cart import Cart
# from .forms import CartAddProductForm


# @require_POST
# def cart_add(request, t_id):
#     cart = Cart(request)
#     toys = get_object_or_404(Toy, id=t_id)
#     form = CartAddProductForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(toys=toys,
#                  quantity=cd['quantity'],
#                  update_quantity=cd['update'])
#     return redirect('cart:cart_detail')


# def cart_remove(request, t_id):
#     cart = Cart(request)
#     toys = get_object_or_404(Toy, id=t_id)
#     cart.remove(toys)
#     return redirect('cart:cart_detail')


# def cart_detail(request):
#     cart = Cart(request)
#     return render(request, {'cart': cart})  #'cart/detail.html',
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from rest_framework import generics,permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.models import Profile
from outfit.models import ClothingItem,Outfit
from outfit.serializers import ClothingItemSerializer,OutfitSerializer

def home(request):
    return render(request,'home.html')

@login_required
def wardrobe(request):

    clothing_items=ClothingItem.objects.filter(
        user=request.user
    )

    category=request.GET.get('category')
    color=request.GET.get('color')
    season=request.GET.get('season')
    occasion=request.GET.get('occasion')

    if category:
       clothing_items=clothing_items.filter(
        category=category
    )

    if color:
        clothing_items=clothing_items.filter(
        color__icontains=color
    )

    if season:
       clothing_items=clothing_items.filter(
        season__icontains=season
    )

    if occasion:
      clothing_items=clothing_items.filter(
        occasion__icontains=occasion
    )

    return render(request,'wardrobe.html', {
        'clothing_items':clothing_items
    })

@login_required
def add_clothing(request):

    if request.method=='POST':

        seasons=request.POST.getlist('season')
        occasions=request.POST.getlist('occasion')

        ClothingItem.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            category=request.POST.get('category'),
            color=request.POST.get('color'),
            size=request.POST.get('size'),
            brand=request.POST.get('brand'),
            season=','.join(seasons),
            occasion=','.join(occasions),

            image=request.FILES.get('image')
        )

        return redirect('/wardrobe/')

    return render(request,'add_clothing.html')


def register(request):

    if request.method=='POST':

        username=request.POST.get('username')
        password=request.POST.get('password')

        user=User.objects.create_user(
            username=username,
            password=password
        )

        Profile.objects.create(
            user=user
        )

        return redirect('/login/')

    return render(request,'register.html')


@login_required
def profile(request):

    profile=Profile.objects.get_or_create(
        user=request.user
    )

    return render(request,'profile.html',{
        'profile': profile
    })

@login_required
def edit_profile(request):

    profile = Profile.objects.get(
        user=request.user
    )

    if request.method=='POST':

        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES.get('profile_picture')

        profile.save()

        return redirect('/profile/')

    return render(request,'edit_profile.html', {
        'profile': profile
    })

def user_login(request):

    if request.method=='POST':

        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('/wardrobe/')

        return render(request,'login.html', {
            'error':'Invalid username or password'
        })

    return render(request,'login.html')

def edit_clothing(request,id):

    clothing=ClothingItem.objects.get(
        id=id,
        user=request.user
    )

    if request.method=='POST':

        clothing.name=request.POST.get('name')
        clothing.category=request.POST.get('category')
        clothing.color=request.POST.get('color')
        clothing.size=request.POST.get('size')
        clothing.brand=request.POST.get('brand')

        seasons=request.POST.getlist('season')
        occasions=request.POST.getlist('occasion')

        clothing.season=','.join(seasons)
        clothing.occasion=','.join(occasions)

        clothing.save()

        return redirect('/wardrobe/')

    return render(request,'edit_clothing.html',{
        'clothing':clothing
    })


def delete_clothing(request,id):

    clothing=ClothingItem.objects.get(
        id=id,
        user=request.user
    )

    clothing.delete()

    return redirect('/wardrobe/')



@login_required
def outfit_planner(request):
    outfits=Outfit.objects.filter(user=request.user)

    return render(request,'outfit_planner.html',{
        'outfits': outfits
    })

@login_required
def create_outfit(request):

    clothing_items=ClothingItem.objects.filter(user=request.user)

    if request.method=='POST':

        name=request.POST.get('name')
        description=request.POST.get('description')

        selected_items=request.POST.getlist('clothing_items')

        outfit=Outfit.objects.create(
            user=request.user,
            name=name,
            description=description
        )

        outfit.clothing_items.set(selected_items)

        return redirect('/outfit-planner/')

    return render(request,'create_outfit.html',{
        'clothing_items': clothing_items
    })

@login_required
def edit_outfit(request,id):

    outfit=Outfit.objects.get(
        id=id,
        user=request.user
    )

    clothing_items=ClothingItem.objects.filter(
        user=request.user
    )

    if request.method=='POST':

        outfit.name = request.POST.get('name')
        outfit.description=request.POST.get('description')

        selected_items=request.POST.getlist('clothing_items')

        outfit.clothing_items.set(selected_items)

        outfit.save()

        return redirect('/outfit-planner/')

    return render(request,'edit_outfit.html',{
        'outfit': outfit,
        'clothing_items':clothing_items
    })

@login_required
def delete_outfit(request,id):

    outfit=Outfit.objects.get(
        id=id,
        user=request.user
    )

    outfit.delete()

    return redirect('/outfit-planner/')

class ClothingListCreateView(generics.ListCreateAPIView):

    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=ClothingItemSerializer

    def get_queryset(self):
        return ClothingItem.objects.filter(user=self.request.user)

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)


class ClothingDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=ClothingItemSerializer

    def get_queryset(self):
        return ClothingItem.objects.filter(user=self.request.user)
    

class OutfitListCreateView(generics.ListCreateAPIView):

    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=OutfitSerializer

    def get_queryset(self):
        return Outfit.objects.filter(user=self.request.user)
    

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)


class OutfitDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=OutfitSerializer

    def get_queryset(self):
        return Outfit.objects.filter(user=self.request.user)
from rest_framework import serializers
from outfit.models import ClothingItem, Outfit


class ClothingItemSerializer(serializers.ModelSerializer):

    class Meta:
        model=ClothingItem
        fields='__all__'
        read_only_fields=['id','user','created_at']


class OutfitSerializer(serializers.ModelSerializer):

    clothing_items=serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=ClothingItem.objects.all()
    )

    class Meta:
        model=Outfit
        fields='__all__'
        read_only_fields=['id','user','created_at']

    def to_representation(self, instance):

        data=super().to_representation(instance)

        category_order={
            'Top': 1,
            'Bottom': 2,
            'Dress': 3,
            'Outerwear': 4,
            'Footwear': 5,
            'Accessory': 6,
        }

        items=instance.clothing_items.all()

        sorted_items=sorted(
            items,
            key=lambda item:category_order.get(item.category, 99)
        )

        data['clothing_items']=[
            item.id for item in sorted_items
        ]

        return data
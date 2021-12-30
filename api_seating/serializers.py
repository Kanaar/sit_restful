from rest_framework import serializers
from .models import Order, Rank, Row, Seat, Section, Ticket

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('name', 'is_balcony')

class RankSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rank
        fields = ('name',)

class RowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Row
        fields = ('number', 'is_front', 'is_curved')
        section = SectionSerializer()

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        rank = RankSerializer()
        row = RowSerializer()
        fields = ('number', 'is_aisle')

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        seat = SeatSerializer()
        fields = ('seat')

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        # tickets = serializers.StringRelatedField(many=True)
        model = Order
        fields = ('name', 'email', 'amount_of_tickets', 'pref_aisle')
        rank = RankSerializer()

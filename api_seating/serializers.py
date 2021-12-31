from rest_framework import serializers
from .models import Order, Rank, Row, Seat, Section, Ticket

class SectionSerializer(serializers.ModelSerializer):
    # TODO: add verbose_name
    class Meta:
        model = Section
        fields = ('name', 'position',)

class RankSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rank
        fields = ('name',)

class RowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Row
        fields = ('number',)
        section = SectionSerializer()

class SeatSerializer(serializers.ModelSerializer):
    row = RowSerializer()["number"]
    rank = RankSerializer()["name"]

    class Meta:
        model = Seat
        fields = ('rank', 'row', 'number', )

class TicketSerializer(serializers.ModelSerializer):
    seat = SeatSerializer()

    class Meta:
        model = Ticket
        fields = ('seat', )

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    section = SectionSerializer()
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Order
        fields = ('name',
                  'email',
                  'n_tickets',
                  'section',
                  'tickets')


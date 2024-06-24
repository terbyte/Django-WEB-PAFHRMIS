# management/commands/update_placements.py

from django.core.management.base import BaseCommand
from myapp.models import Placement, PersonnelItem

class Command(BaseCommand):
    help = 'Update placements based on category'

    def handle(self, *args, **kwargs):
        # Get placements with category "Assign"
        assign_placements = Placement.objects.filter(ASSIGNMENT_CATEGORY='Assign')

        # Process Assign placements
        for placement in assign_placements:
            MOTHER_UNIT = placement.MOTHER_UNIT  # Adjust based on your model structure
            # Update PersonnelItem or perform necessary actions
            personnel_item = PersonnelItem.objects.get(id=placement.MOTHER_UNIT)
            personnel_item.UNIT = MOTHER_UNIT
            personnel_item.save()

            # Delete placement entry
            placement.delete()

        # Remove placements with other categories
        other_placements = Placement.objects.exclude(category='Assign')
        other_placements.delete()

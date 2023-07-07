from django.contrib import admin
from .models import Exercise, ImageExercise


@admin.register(ImageExercise)
class ImageExerciseAdmin(admin.ModelAdmin):

    def has_module_permission(self, request):
        return False

    # fields = ('id', 'image')
    # list_display = ()


class ExerciseAdmin(admin.ModelAdmin):
    filter_horizontal = ('image_exercises', 'add_to_favorites')


admin.site.register(Exercise, ExerciseAdmin)

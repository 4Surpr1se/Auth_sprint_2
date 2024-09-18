from abc import abstractmethod, ABCMeta

from django.contrib import admin
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.db.models import Model
from django.forms import MediaDefiningClass
from django.urls.base import reverse
from .models import Genre, GenreFilmwork, Filmwork, PersonFilmwork, Person


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_filter = ('name',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',)


def singleton(class_):
    # todo получше понять
    # todo сделать нормальный кэш
    instances = {}

    def getinstance(*args, **kwargs):
        if not instances.get(class_):
            instances[class_] = {}
        if not kwargs.get('obj'):
            instances[class_][''] = class_(*args[1:], **kwargs)
            return instances[class_]['']
        obj_id = kwargs['obj'].id
        if not instances.get(class_).get(kwargs['obj'].id):
            # todo args[1:] --- ??????
            instances[class_][obj_id] = class_(*args[1:], **kwargs)
        return instances[class_][obj_id]

    return getinstance


class CombinedMetaclassMixin(ABCMeta, MediaDefiningClass):
    pass


class CustomForeignKeyRawIdWidget(ForeignKeyRawIdWidget):
    __metaclass__ = CombinedMetaclassMixin
    init_name = ''

    def __init__(self, rel, admin_site, **kwargs):
        self.parent_obj = kwargs['obj']
        self._cache = self._generate_cache()
        del kwargs['obj']
        super().__init__(rel, admin_site, **kwargs)

    def label_and_url_for_value(self, value):
        value = str(value)
        obj = self._cache.get(value)
        if not obj:
            self._cache = self._generate_cache()
            obj = self._cache.get(value)
        url = reverse(
            "%s:%s_%s_change"
            % (
                self.admin_site.name,
                obj._meta.app_label,
                obj._meta.model_name,
            ),
            args=(obj.pk,),
        )
        return getattr(obj, self.init_name), url

    @abstractmethod
    def _generate_cache(self):
        pass


@singleton
class GenreForeignKeyRawIdWidget(CustomForeignKeyRawIdWidget):
    init_name = 'name'

    def _generate_cache(self):
        return {str(obj.genre.id): obj.genre for obj in
                GenreFilmwork.objects.filter(film_work=self.parent_obj).select_related('genre').all()}


@singleton
class PersonForeignKeyRawIdWidget(CustomForeignKeyRawIdWidget):
    init_name = 'full_name'

    def _generate_cache(self):
        return {str(obj.person.id): obj.person for obj in
                PersonFilmwork.objects.filter(film_work=self.parent_obj).select_related('person').all()}


class CustomFilmworkInline(admin.TabularInline):
    model: Model = Filmwork.genres.through
    raw_id_fields_custom: tuple[str] = ('',)
    extra = 0
    parent_obj = None
    custom_raw_id_widget: CustomForeignKeyRawIdWidget = CustomForeignKeyRawIdWidget

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in self.raw_id_fields_custom:
            kwargs["widget"] = self.custom_raw_id_widget(
                db_field.remote_field, self.admin_site, using=kwargs.get("using"), obj=self.parent_obj
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        formset = super().get_formset(request, obj, **kwargs)
        return formset


class GenreFilmworkInline(CustomFilmworkInline):
    model: Model = Filmwork.genres.through
    raw_id_fields_custom = ('genre',)
    custom_raw_id_widget: CustomForeignKeyRawIdWidget = GenreForeignKeyRawIdWidget


class PersonFilmworkInline(CustomFilmworkInline):
    model: Model = Filmwork.person.through
    raw_id_fields_custom = ('person',)
    custom_raw_id_widget: CustomForeignKeyRawIdWidget = PersonForeignKeyRawIdWidget


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = ('title', 'type', 'creation_date', 'rating', 'genres_list')
    list_filter = ('type', 'genres')
    search_fields = ('title', 'description', 'id')
    exclude = ('genres',)

    def get_queryset(self, request):
        res = super().get_queryset(request)
        return res.prefetch_related('genres')

    @admin.display()
    def genres_list(self, obj):
        return ', '.join(genre.name for genre in obj.genres.all())

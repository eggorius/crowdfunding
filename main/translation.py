from modeltranslation.translator import register, TranslationOptions
from .models import Company, Comment


@register(Company)
class CompanyTranslationOptions(TranslationOptions):
    fields = ['title', 'description', 'theme']


@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ['title', 'content']


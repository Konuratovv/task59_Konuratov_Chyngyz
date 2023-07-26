from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class Project(models.Model):
    start_date = models.DateField(verbose_name="Дата начала", null=False, blank=False)
    end_date = models.DateField(blank=True, null=True, verbose_name="Дата окончания")
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Название")
    description = models.TextField(max_length=2000, null=False, blank=False, verbose_name="Описание")
    user = models.ManyToManyField(User, related_name="projects", blank=True)
    author = models.ForeignKey(get_user_model(), related_name='project', on_delete=models.SET_DEFAULT, default=1,
                               verbose_name="Автор")


class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        abstract = True


class Status(AbstractModel):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Статус")

    def __str__(self):
        return f"{self.title}"


class Type(AbstractModel):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Тип")

    def __str__(self):
        return f"{self.title}"


class Issue(AbstractModel):
    summary = models.CharField(max_length=100, null=False, blank=False, verbose_name="Краткое описание")
    description = models.TextField(max_length=2000, null=False, blank=False, verbose_name="Полное описание")
    status = models.ForeignKey("webapp.Status", related_name="issues", on_delete=models.RESTRICT,
                               verbose_name="Статус")
    type = models.ManyToManyField("webapp.Type", related_name="issues", through="webapp.IssueType",
                                  through_fields=('issue', 'type'), blank=True)
    project = models.ForeignKey("webapp.Project", related_name="issues", on_delete=models.CASCADE, default=1,
                                verbose_name="Проект")


class IssueType(AbstractModel):
    issue = models.ForeignKey("webapp.Issue", related_name="issue_type", on_delete=models.CASCADE,
                              verbose_name="Задача")
    type = models.ForeignKey("webapp.Type", related_name="type_issue", on_delete=models.CASCADE, verbose_name="Типы")

    def __str__(self):
        return "{} | {}".format(self.issue, self.type)

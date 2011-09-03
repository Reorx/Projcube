#coding=utf8
from django import forms
from models import Proj, ProjMembership,\
        Task, Daysum

class ProjForm(forms.ModelForm):
    class Meta:
        model = Proj
        fields = ('name', 'description', )
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'textarea',
                'placeholder': 'description'
            })
        }

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(ProjForm, self).__init__(*args, **kwargs)

    def save(self):
        data = self.cleaned_data

        # create project
        p = Proj(**data)
        p.creator = self.user
        p.save()

        # add creator as member
        pm = ProjMembership(
            user = self.user,
            proj = p
        )
        pm.save()

        return p

class TaskForm(forms.ModelForm):
    proj_id = forms.IntegerField()
    class Meta:
        model = Task
        fields = ('content', )

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(TaskForm, self).__init__(*args, **kwargs)

    def clean_proj_id(self):
        proj_id = self.cleaned_data['proj_id']
        try:
            self.proj = self.user.projs.get(id=proj_id)
            if not self.proj.judge_membership(self.user):
                raise forms.ValidationError('not project member')
        except:
            raise forms.ValidationError('no project pointed')
        return proj_id

    def save(self):
        data = self.cleaned_data

        # create task
        t = Task(
            creator = self.user,
            proj = self.proj,
            content = data['content']
        )
        t.save()

        return t

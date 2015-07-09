from django.views.generic import View, TemplateView
from django.template.response import TemplateResponse
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpResponseRedirect
import json

import pprint

class TemplateResponseMixin(object):
    """
    A mixin that can be used to render a template.
    """
    template_name = None
    template_engine = None
    response_class = TemplateResponse
    content_type = None

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response, using the `response_class` for this
        view, with a template rendered with the given context.

        If any keyword arguments are provided, they will be
        passed to the constructor of the response class.
        """
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )

    def get_template_names(self):
        """
        Returns a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        if self.template_name is None:
            raise ImproperlyConfigured(
                "TemplateResponseMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'")
        else:
            return [self.template_name]

class ContextMixin(object):
    """
    A default context mixin that passes the keyword arguments received by
    get_context_data as the template context.
    """

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        return kwargs

class IndexTemplateView(TemplateResponseMixin, ContextMixin, View):


    template_name = 'angular/index.html'


    """
    A view that renders a template.  This view will also pass into the context
    any keyword arguments passed by the url conf.
    """
    def get(self, request, *args, **kwargs):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(request.META['HTTP_USER_AGENT'])

        #print(request.META)

        #if ('ANDROID' in str(request.META['HTTP_USER_AGENT']).upper()):
        if ('SATAN' in str(request.META['HTTP_USER_AGENT']).upper()):
            #return HttpResponseRedirect('https://play.google.com/store/apps/details?id=com.jotto.got_spoilers')
            #
            response = HttpResponse("", status=302)
            response['Location'] = 'market://details?id=com.jotto.got_spoilers'
            return response
        else:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
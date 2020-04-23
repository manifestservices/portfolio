from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from django.http import HttpResponseRedirect
import logging,datetime,random
log=logging.getLogger(__name__)

# def error_404(request,exception,template_name='404.html'):
#         data = {}
#         return render(request,'404.html', data)
#
# def error_500(request,exception,template_name='500.html'):
#         data = {}
#         return render(request,'500.html', data)

class BaseView(View):
    """
    :Brief: Custom base class for django's class based views
    """

    def __init__(self, **kwargs):
        """ Initializes the base view object
        """
        self.context_dict={}
        super(BaseView, self).__init__(**kwargs)
    
    
    def __set_visit_cookie(self,cookie):
        """
        :brief: This method generates and sets the cookie if not present
        value
        Note: String None is checked to reset the existing erroneous cookies being set as string NONE
        """
        if cookie and str(cookie).lower().strip()!='none':
            log.info('Cookie already exists cookie::%s'%cookie)
            return cookie
        datetime_val = datetime.datetime.now()
        visit_cookie_id = datetime_val.strftime('%Y%m%d%H%M%S') \
                                       + str(random.randint(0,1000))
        log.info('Exiting __set_visit_cookie cookie::%s'%visit_cookie_id)
        return visit_cookie_id

    def dispatch(self, request, *args, **kwargs):
        """ Customized dispatch method
        """
        visit_cookie_id=self.__set_visit_cookie(request.COOKIES.get('visit_cookie_id'))
        response = super(BaseView, self).dispatch(request, *args, **kwargs)
        if request.method.lower()=='get':
            response.set_cookie('visit_cookie_id',visit_cookie_id,
                                        max_age=365*24*60*60)
        return response
    
class LoginView(BaseView):

    def get(self, request):
        """ 
            Render the login page
        """
        if request.GET.get('next'):
            self.context_dict['next']=request.GET.get('next')
        return render(request, 'login.html',self.context_dict)
    def post(self, request):
        """
            Post of login authentication.
            Redirect to the page where the client logged in
        """
        username=request.POST.get('username')
        password=request.POST.get('password')
        next_=request.GET.get('next')
        next_post=request.POST.get('next')
        redirect_path=next_ or next_post
        user=authenticate(request,username=username,password=password)
        if user is not None:
            log.info('Authenticated user')
            login(request,user)
            request.session['name']=username.split("@")[0]
            log.info('user %s logged in'%request.user.username)
            if is_safe_url(redirect_path,request.get_host()):
                log.info('Redirecting to %s'%redirect_path)
                return redirect(redirect_path)
            else:
                return redirect('/'+'?login_success=1')
        else:
            return HttpResponseRedirect(reverse('login'))

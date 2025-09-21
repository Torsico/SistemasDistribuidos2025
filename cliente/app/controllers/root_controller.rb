require 'clases' # no es necesario gracias a Rails, pero permite recargar

require 'grpc'
require 'session_pb'
require 'session_services_pb'
require 'google/protobuf/empty_pb'

class RootController < ApplicationController
    
    @@stub = nil
    
    before_action do
        unless @@stub # reusar stub en vez de crear uno nuevo
            @@stub = Session::LoginService::Stub.new('localhost:50051', :this_channel_is_insecure)
        end
    end
    
    def root
        # cosas
    end
    
    def loginpost
        
        rq = Session::LoginRequest.new
        rq.usuario_email = params[:user]
        rq.clave = params[:pass]
        
        #rp = @@stub.login( rq )
        # TODO esperar que funcione, despues:
        # hacer algo con la respuesta
        
        flash[:noticetext] = ":)"
        flash[:noticecolor] = @@color_info
        redirect_to "/"
    end
    
    def logoutpost
        
        # TODO logout
        
        flash[:noticetext] = ":()"
        flash[:noticecolor] = @@color_info
        redirect_to "/"
    end
end
  
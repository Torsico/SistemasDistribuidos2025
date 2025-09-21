class RootController < ApplicationController
    def root
        # cosas
    end
    
    def loginpost
        
        #rq = Usuarios::ModUsuarioRequest.new
        #rq.usuario = u
        
        
        flash[:noticetext] = ":)"
        flash[:noticecolor] = @@color_info
        redirect_to "/"
    end
    
    def logoutpost
        
        
        
        flash[:noticetext] = ":()"
        flash[:noticecolor] = @@color_info
        redirect_to "/"
    end
end
  
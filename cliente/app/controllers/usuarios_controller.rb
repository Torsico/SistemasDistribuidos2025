require 'clases' # no es necesario gracias a Rails, pero permite recargar

require 'grpc'
require 'usuarios_pb'
require 'usuarios_services_pb'
require 'rol_pb'
require 'rol_services_pb'
require 'google/protobuf/empty_pb'

class UsuariosController < ApplicationController
    
    @@lasttodos = nil
    @@stub = nil
    
    before_action do
        unless @@stub # reusar stub en vez de crear uno nuevo
            @@stub = Usuarios::UsuarioService::Stub.new('localhost:50051', :this_channel_is_insecure)
        end
    end
    
    def index
        # Al cargar la pagina, se muestran los usuarios.
        # Tambien se muestran los botones de accion.
        
        todos = {}
        
        #stub = Usuarios::UsuarioService::Stub.new('localhost:50051', :this_channel_is_insecure)
        
        begin
            @badlist = false
            response = @@stub.get_usuarios(Google::Protobuf::Empty.new)
            
            response.usuarios.each do |user|
                #puts user
                u = Usuario.new(user)
                todos[u.idusuario] = u
            end
            
        rescue GRPC::Unavailable => exception
            #u = Usuario.new
            #u.nombre = 503
            #lista.push u
            
            @badlist = true # hace que index no ponga elementos de lista
            
            # colores en application_controller.rb
            flash[:noticecolor] = @@color_error
            flash[:noticetext] = "503: El servidor no esta disponible"
            
            
            #redirect_to controller: :root, action: :root
        rescue => exception
            puts exception
            flash[:noticecolor] = @@color_supererror
            flash[:noticetext] = exception
        end
        
        @usuarios = todos
        @@lasttodos = todos
    end
    
    def altaform
        @make = true
        @id = nil
        form
    end
    def modform
        @make = false
        @id = params[:id]
        form
    end
    
    def form
        #flash[:noticetext] = "make? '#{@make}' id? '#{@id}' gog? #{@@lasttodos}"
        #flash[:noticetext] = "!!!"
        if @make
            #flash.now[:noticetext] = "Creando nuevo usuario..."
        else
            @editee = @@lasttodos[@id.to_i]
            #flash.now[:noticetext] = "Editando usuario #{@editee.nombreUsuario}..."
        end
        
        render :form
    end
    
    def grpc_user_from_params
        u = Usuarios::Usuario.new
        u.idusuario		= params[:idusuario]&.to_i || params[:id]&.to_i || 0
        u.nombre		= params[:nombre]
        u.apellido		= params[:apellido]
        u.nombreUsuario	= params[:nombreUsuario]
        u.telefono		= params[:telefono]
        u.clave			= params[:clave] || ""
        u.email			= params[:email]
        u.rol			= params[:rol].to_i
        u.activo		= !!params[:activo]
        
        u.clear_idusuario if u.idusuario == 0
        u.clear_clave if u.clave == ""
        
        return u
    end
    
    def altapost
        flash[:noticetext] = "Usuario \"#{params[:nombreUsuario]}\" creado!"
        flash[:noticecolor] = @@color_success
        u = grpc_user_from_params
        p u
        rq = Usuarios::AltaUsuarioRequest.new
        rq.usuario = u
        
        rp = @@stub.alta_usuario( rq )
        
        if rp.suceso then
            flash[:noticetext] = "Usuario creado!"
            flash[:noticecolor] = @@color_success
        else
            flash[:noticetext] = "Error: no se puede usar nombre de usuario ya existente"
            flash[:noticecolor] = @@color_error
        end
        
        redirect_to "/usuarios"
    end
    def modpost
        u = grpc_user_from_params
        p u
        rq = Usuarios::ModUsuarioRequest.new
        rq.usuario = u
        
        rp = @@stub.mod_usuario( rq )
        
        if rp.suceso then
            flash[:noticetext] = "Usuario \"#{params[:nombreUsuario]}\" editado!"
            flash[:noticecolor] = @@color_success
            redirect_to "/usuarios"
        else
            flash[:noticetext] = "Error: no se puede usar nombre de usuario ya existente"
            flash[:noticecolor] = @@color_error
            redirect_to "/usuarios/mod/#{params[:id]}"
        end
        
        
    end
    
end

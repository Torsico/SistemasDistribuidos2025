require 'clases' # no es necesario gracias a Rails, pero permite recargar

require 'grpc'
require 'usuarios_pb'
require 'usuarios_services_pb'
require 'rol_pb'
require 'rol_services_pb'
require 'google/protobuf/empty_pb'

class UsuariosController < ApplicationController
    
    @@lastlista = nil
    
    def index
        # Al cargar la pagina, se muestran los usuarios.
        # Tambien se muestran los botones de accion.
        
        lista = []
        
        stub = Usuarios::UsuarioService::Stub.new('localhost:50051', :this_channel_is_insecure)
        
        begin
            @badlist = false
            response = stub.get_usuarios(Google::Protobuf::Empty.new)
            
            response.usuarios.each do |user|
                #puts user
                u = Usuario.new(user)
                lista.push u
            end
            
        rescue GRPC::Unavailable => exception
            u = Usuario.new
            u.nombre = 503
            lista.push u
            
            @badlist = true
            
            # colores en application_controller.rb
            flash[:noticecolor] = @@color_error
            flash[:noticetext] = "503: El servidor no esta disponible"
            
            
            #redirect_to controller: :root, action: :root
        rescue => exception
            puts exception
            flash[:noticecolor] = @@color_supererror
            flash[:noticetext] = exception
        end
        
        @usuarios = lista
        @@lastlista = lista
        #flash[:list] = lista
        #flash.keep :list
        #render locals: {ntext: notiftext, ncolor: notifcolor}
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
        #flash[:noticetext] = "make? '#{@make}' id? '#{@id}' gog? #{@@lastlista}"
        flash[:noticetext] = "!!!"
        if @make
            flash.now[:noticetext] = "Creando nuevo usuario..."
        else
            @editee = @@lastlista[@id.to_i-1] # off by 1
            # id usuarios nunca va a tener un espacio en blanco
            flash.now[:noticetext] = "Editando usuario #{@editee.nombreUsuario}..."
        end
        render :form
    end
    
    
    def altapost
        flash[:noticetext] = "Usuario \"#{params[:nombreUsuario]}\" creado! TODO"
        
        redirect_to "/usuarios"
    end
    def modpost
        flash[:noticetext] = "Usuario \"#{params[:nombreUsuario]}\" editado! TODO"
        
        redirect_to "/usuarios"
    end
    
end
  
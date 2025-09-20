require 'clases' # no es necesario gracias a Rails, pero permite recargar

require 'grpc'
require 'usuarios_pb'
require 'usuarios_services_pb'
require 'rol_pb'
require 'rol_services_pb'
require 'google/protobuf/empty_pb'

class UsuariosController < ApplicationController
    
    def index
        # Al cargar la pagina, se muestran los usuarios.
        # Tambien se muestran los botones de accion.
        
        lista = []
        
        stub = Usuarios::UsuarioService::Stub.new('localhost:50051', :this_channel_is_insecure)
        
        begin
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
        #render locals: {ntext: notiftext, ncolor: notifcolor}
    end
    
    def show # no usamos show
        redirect_to "usuarios"
    end
    
    def new
        @make = true
        @id = nil
        form
    end
    def edit
        @make = false
        @id = params[:id]
        form
    end
    
    def form
        flash[:noticetext] = "make? '#{@make}' id? '#{@id}'"
        render :form
    end
end
  
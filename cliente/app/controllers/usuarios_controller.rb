require 'clases' # no es necesario gracias a Rails, pero permite recargar

require 'grpc'
require 'usuarios_pb'
require 'usuarios_services_pb'
require 'rol_pb'
require 'rol_services_pb'
require 'google/protobuf/empty_pb'

class UsuariosController < ApplicationController
    
    def root
        lista = []
        #lista.push Usuario.new.scramble!
        #lista.push Usuario.new.scramble!
        #lista.push Usuario.new.scramble!
        
        stub = Usuarios::UsuarioService::Stub.new('localhost:50051', :this_channel_is_insecure)
        
        begin
            response = stub.get_usuarios(Google::Protobuf::Empty.new)
            
            response.usuarios.each do |xd|
                u = Usuario.new
                u.nombre = xd.nombre
                u.apellido = xd.apellido
                u.nombreusuario = xd.nombreUsuario
                lista.push u
            end
            
        rescue GRPC::Unavailable => exception
            u = Usuario.new
            u.nombre = 503
            lista.push u
            
            #redirect_to controller: :root, action: :root
        rescue => exception
            puts exception
        end
        
        @usuarios = lista
    end
end
  
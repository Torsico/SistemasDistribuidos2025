require 'clases' # no es necesario gracias a Rails, pero permite recargar

require 'grpc'
require 'usuarios_pb'
require 'usuarios_services_pb'
require 'rol_pb'
require 'rol_services_pb'
require 'donaciones_pb'
require 'donaciones_services_pb'
require 'google/protobuf/empty_pb'
require 'google/protobuf/well_known_types'

class InventariosController < ApplicationController
	
	@@stub = nil
	@@stubuser = nil
	
	before_action do
		unless @@stub # reusar stub en vez de crear uno nuevo
			@@stub = Donaciones::DonacionesService::Stub.new('localhost:50051', :this_channel_is_insecure)
			@@stubuser = Usuarios::UsuarioService::Stub.new('localhost:50051', :this_channel_is_insecure)
		end
	end
	
	def index
		
		todos = {}
		
		begin
			@badlist = false
			
			rp = @@stub.get_donaciones(Google::Protobuf::Empty.new)
			
			rp.donaciones.each do |item|
				todos[item.iddonaciones] = item
			end
			
			todouser = {}
			rpu = @@stubuser.get_usuarios(Google::Protobuf::Empty.new)
			rpu.usuarios.each do |user|
				u = Usuario.new(user)
				todouser[u.idusuario] = u
			end
			
			@users = todouser
			
		rescue GRPC::Unavailable => exception
			@badlist = true
			
			flash[:noticecolor] = @@color_error
			flash[:noticetext] = "503: El servidor no esta disponible"
		rescue => exception
			@badlist = true
			
			puts exception
			flash[:noticecolor] = @@color_supererror
			flash[:noticetext] = exception
		end
		
		@items = todos
		@@lasttodos = todos
	end
	
	def altaform
        @style = :alta
        form
	end
    def modform
        @style = :mod
        @id = params[:id]
        form
    end
    def bajaform
        @style = :baja
		@id = params[:id]
        form
    end
    
    def form
        #flash[:noticetext] = "make? '#{@make}' id? '#{@id}' gog? #{@@lasttodos}"
        #flash[:noticetext] = "!!!"
        if @style == :alta
            #flash.now[:noticetext] = "Creando nuevo usuario..."
        else
            @editee = @@lasttodos[@id.to_i]
            #flash.now[:noticetext] = "Editando usuario #{@editee.nombreUsuario}..."
        end
        
        render :form
    end
    
    def altapost
        flash[:noticetext] = "donasion"
        flash[:noticecolor] = @@color_success
		
		don = {
			categoria: params[:categoria],
			descripcion: params[:descripcion],
			cantidad: params[:cantidad],
		}
		don = Donaciones::Donaciones.new
		don.iddonaciones = params[:iddonaciones] || 0
		don.categoria = params[:categoria]
		don.descripcion = params[:descripcion]
		don.cantidad = params[:cantidad].to_i || -1
		don.eliminado = params[:eliminado]=="1" ? true : false
		
		don.clear_iddonaciones if don.iddonaciones == 0
		don.clear_cantidad if don.cantidad < 0
		
        rq = Donaciones::AltaDonacionesRequest.new
        rq.donaciones = don
        
        rp = @@stub.alta_donaciones( rq )
        
        if rp.suceso then
            flash[:noticetext] = "Donacion de \"#{params[:descripcion]}\" creada!"
            flash[:noticecolor] = @@color_success
        else
            flash[:noticetext] = "Error: ???"
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
	
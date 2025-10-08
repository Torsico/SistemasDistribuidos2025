require 'clases' # no es necesario gracias a Rails, pero permite recargar

require 'grpc'
require 'usuarios_pb'
require 'usuarios_services_pb'
require 'rol_pb'
require 'rol_services_pb'
require 'eventos_pb'
require 'eventos_services_pb'
require 'donaciones_pb'
require 'donaciones_services_pb'
require 'google/protobuf/empty_pb'
require 'google/protobuf/well_known_types'

class EventosController < ApplicationController
	
	@@stub = nil
	@@stubuser = nil
	
	before_action do
		unless @@stub # reusar stub en vez de crear uno nuevo
			@@stub = Eventos::EventosService::Stub.new('localhost:50051', :this_channel_is_insecure)
			@@stubuser = Usuarios::UsuarioService::Stub.new('localhost:50051', :this_channel_is_insecure)
		end
	end
	
	def index
		
		todos = {}
		
		begin
			@badlist = false
			
			rp = @@stub.get_eventos(Google::Protobuf::Empty.new)
			
			rp.evento.each do |item|
				todos[item.ideventos] = item
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
end
  
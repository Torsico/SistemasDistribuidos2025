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

class EventosController < ApplicationController
	
	@@stub = nil
	
	before_action do
		unless @@stub # reusar stub en vez de crear uno nuevo
			#@@stub = Session::LoginService::Stub.new('localhost:50051', :this_channel_is_insecure)
		end
	end
	
	def index
		
		todos = {}
		
		begin
			@badlist = false
			
			#rp = @@stub.get_usuarios(Google::Protobuf::Empty.new)
			
			#rp.usuarios.each do |item|
			#end
			
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
end
  
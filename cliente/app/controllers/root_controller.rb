require 'clases' # no es necesario gracias a Rails, pero permite recargar

require 'grpc'
require 'session_pb'
require 'session_services_pb'
require 'usuarios_pb'
require 'usuarios_services_pb'
require 'rol_pb'
require 'rol_services_pb'
require 'google/protobuf/empty_pb'

class RootController < ApplicationController
	
	@@stub = nil
	
	before_action do
		unless @@stub # reusar stub en vez de crear uno nuevo
			@@stub = Session::LoginService::Stub.new('localhost:50051', :this_channel_is_insecure)
			@@stubuser = Usuarios::UsuarioService::Stub.new('localhost:50051', :this_channel_is_insecure)
		end
	end
	
	def root
		# cosas
	end
	
	def loginpost
		# Horrible!
		# Descubro mientras realizo este archivo que
		# la implementacion gRPC Ruby esta incompleta:
		# No hay funcionalidad metadata!
		# Vamos a tener que saltarnos la autenticacion por token.
		
		rq = Session::LoginRequest.new
		rq.usuario_email = params[:user]
		rq.clave = params[:pass]
		
		flash[:noticetext] = ":)"
		flash[:noticecolor] = @@color_info
		
		begin
			@bad = false
			rp = @@stub.login( rq )
		
			if rp.suceso
				p({suc: rp.suceso, us: rp.usuario })
				u = rp.usuario
				$session.user = u
				flash[:noticetext] = "Bienvenido, #{u.nombreUsuario}!"
			else
				flash[:noticetext] = "¿ :( ?"
				# este error no se vera normalmente
				# por que el servidor python tira una excepcion
			end
			
		rescue GRPC::Unavailable => exception
			@bad = true
            flash[:noticecolor] = @@color_error
            flash[:noticetext] = "503: El servidor no esta disponible"
			
		rescue GRPC::Unknown => exception
			@bad = true
			# aparentemente, errores lanzados manualmente
			# caen en esta categoria
            flash[:noticecolor] = @@color_error
            flash[:noticetext] = exception
			
			# FIXME: por alguna razon no puedo atrapar este error
			
		rescue => exception
			@bad = true
            puts exception
            flash[:noticecolor] = @@color_supererror
            flash[:noticetext] = exception
		
		end
		
		if @bad
			redirect_to "/login"
		else
			redirect_to "/"
		end
		
		#rp.usuario
		
		# TODO esperar que funcione, despues:
		# hacer algo con la respuesta
		
	end
	
	def logout
		
		$session.forget_user!
		
		flash[:noticetext] = "chau :("
		flash[:noticecolor] = @@color_info
		redirect_to "/"
	end
end
  
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
require 'google/protobuf/timestamp_pb'

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
	
	# assign item field
	# no me gusta asignar algo y despues llamar clear (dos lineas al pepe), asi que...
	# (esto iria mejor en un importable, estilo "utils.rb")
	def aif_string(item, field, value)
		if value.nil? || value == ""
			item.public_send("clear_#{field}")
		else
			item.public_send("#{field}=", value)
		end
	end
	def aif_number(item, field, value)
		if value.nil? || value == 0
			item.public_send("clear_#{field}")
		else
			item.public_send("#{field}=", value)
		end
	end
	def aif_bool(item, field, value)
		if value.nil?
			item.public_send("clear_#{field}")
		else
			value = !!value # cast, por si acaso
			item.public_send("#{field}=", value)
		end
	end
	
	def grpc_item_from_params(writealta)
		d = Donaciones::Donaciones.new
		
		aif_number(d, :iddonaciones, params[:iddonaciones]&.to_i || params[:id]&.to_i)
		aif_string(d, :categoria, params[:categoria])
		aif_string(d, :descripcion, params[:descripcion])
		aif_number(d, :cantidad, params[:cantidad]&.to_i)
		aif_bool(d, :eliminado, writealta ? false : !!params[:eliminado])
		# la version indeterminada de esto es estrictamente javascript
		# la pagina no tiene scripts
		
		p d.eliminado
		
		d.clear_cantidad if d.cantidad < 0
		
		# los timestamps son mas complicados, pero no por mucho
		# en alta: cambiar alta y mod a "hoy, por mi"
		# en mod: solo cambiar mod
		# 
		# el servidor maneja esta parte
		
		#rightnow = Google::Protobuf::Timestamp.new
		#rightnow.from_time(Time.now)
		#		
		#if writealta
			#d.fecha_alta = rightnow
			#d.usuario_alta = $session.user.idusuario
		#end
		#d.fecha_mod = rightnow
		#d.usuario_mod = $session.user.idusuario
		
		return d
	end
	
	def altapost
		flash[:noticetext] = "donasion"
		flash[:noticecolor] = @@color_success
		
		don = grpc_item_from_params(true)
		
		rq = Donaciones::AltaDonacionesRequest.new
		rq.donaciones = don
		
		metadata = { "authorization" => $session.token }
		rp = @@stub.alta_donaciones(rq, metadata: metadata)
		
		
		if rp.suceso then
			flash[:noticetext] = "Donacion de \"#{params[:descripcion]}\" creada!"
			flash[:noticecolor] = @@color_success
		else
			flash[:noticetext] = "Error: ???"
			flash[:noticecolor] = @@color_error
		end
		
		redirect_to "/inventarios"
	end
	def modpost
		p "MODPOST: RQ"
		don = grpc_item_from_params(false)
		
		rq = Donaciones::ModDonacionesRequest.new
		rq.donaciones = don
		
		metadata = { "authorization" => $session.token }
		rp = @@stub.mod_donaciones(rq, metadata: metadata)
		
		p rp
		p "MODPOST: END"
		
		if rp.suceso then
			flash[:noticetext] = "Donacion de \"#{params[:descripcion]}\" modificada!"
			flash[:noticecolor] = @@color_success
			redirect_to "/inventarios"
		else
			flash[:noticetext] = "Error desconocido"
			flash[:noticecolor] = @@color_error
			redirect_to "/inventarios/mod/#{params[:id]}"
		end
	end
	
	def bajapost
		rq = Donaciones::BajaDonacionesRequest.new
		rq.iddonaciones = params[:id]&.to_i
		
		metadata = { "authorization" => $session.token }
		rp = @@stub.baja_donaciones(rq, metadata: metadata)
		
		if rp.suceso then
			flash[:noticetext] = "Donacion dada de baja."
			flash[:noticecolor] = @@color_success
			redirect_to "/inventarios"
		else
			flash[:noticetext] = "Error desconocido"
			flash[:noticecolor] = @@color_error
			redirect_to "/inventarios/baja/#{params[:id]}"
		end
	end
	
end
	